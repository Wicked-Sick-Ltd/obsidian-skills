#!/usr/bin/env python3
"""Drift checks for the generated skill layouts."""

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_layouts", ROOT / "scripts" / "sync_layouts.py")
sync_layouts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_layouts)


def write_skill(directory: Path, name: str, description: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    references = directory / "references"
    references.mkdir()
    (references / "NOTE.md").write_text("reference\n", encoding="utf-8")


class LayoutDriftTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.original_passing = sync_layouts.PASSING
        self.original_held = sync_layouts.HELD
        sync_layouts.PASSING = ("alpha", "beta")
        sync_layouts.HELD = ("secret",)
        canonical = self.root / sync_layouts.CANONICAL
        write_skill(canonical / "alpha", "alpha", "Write alpha files.")
        write_skill(canonical / "beta", "beta", "Write beta files.")
        write_skill(self.root / "held" / "secret", "secret", "Do not load this.")
        plugin = self.root / "plugins" / "obsidian"
        plugin.mkdir(parents=True, exist_ok=True)
        (plugin / "plugin.json").write_text(json.dumps({"version": "9.9.9"}) + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        sync_layouts.PASSING = self.original_passing
        sync_layouts.HELD = self.original_held
        self._tmp.cleanup()

    def test_sync_then_check_passes_and_resolves_references(self) -> None:
        sync_layouts.sync(self.root)
        self.assertEqual(sync_layouts.check(self.root), [])
        linked = self.root / ".cursor" / "skills" / "alpha" / "references" / "NOTE.md"
        self.assertEqual(linked.read_text(encoding="utf-8"), "reference\n")
        self.assertTrue((self.root / "skills").is_symlink())
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Write alpha files.", agents)
        self.assertNotIn("secret", agents)

    def test_check_fails_when_a_layout_is_a_copy(self) -> None:
        sync_layouts.sync(self.root)
        copied = self.root / ".grok" / "skills" / "beta"
        target = copied.resolve()
        copied.unlink()
        shutil.copytree(target, copied)
        errors = sync_layouts.check(self.root)
        self.assertTrue(any("not a symlink" in item for item in errors))

    def test_sync_removes_an_obsolete_held_symlink(self) -> None:
        sync_layouts.sync(self.root)
        extra = self.root / ".claude" / "skills" / "secret"
        extra.symlink_to(os.path.relpath(self.root / "held" / "secret", extra.parent))
        sync_layouts.sync(self.root)
        self.assertFalse(extra.exists())
        self.assertEqual(sync_layouts.check(self.root), [])

    def test_sync_refuses_to_delete_a_real_extra_directory(self) -> None:
        sync_layouts.sync(self.root)
        extra = self.root / ".cursor" / "skills" / "notes"
        extra.mkdir()
        (extra / "SKILL.md").write_text("keep\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            sync_layouts.sync(self.root)
        self.assertEqual((extra / "SKILL.md").read_text(encoding="utf-8"), "keep\n")

    def test_check_fails_when_a_held_skill_is_linked(self) -> None:
        sync_layouts.sync(self.root)
        extra = self.root / ".claude" / "skills" / "secret"
        extra.symlink_to(os.path.relpath(self.root / "held" / "secret", extra.parent))
        errors = sync_layouts.check(self.root)
        self.assertTrue(any("secret" in item for item in errors))

    def test_quoted_frontmatter_matches_the_directory_name(self) -> None:
        sync_layouts.sync(self.root)
        skill = self.root / sync_layouts.CANONICAL / "alpha" / "SKILL.md"
        skill.write_text(
            '---\nname: "alpha"\ndescription: "Write alpha files."\n---\n\n# alpha\n',
            encoding="utf-8",
        )
        self.assertEqual(sync_layouts.check(self.root), [])

    def test_block_description_is_rejected(self) -> None:
        sync_layouts.sync(self.root)
        skill = self.root / sync_layouts.CANONICAL / "alpha" / "SKILL.md"
        skill.write_text(
            "---\nname: alpha\ndescription: >-\n  Write alpha files.\n---\n\n# alpha\n",
            encoding="utf-8",
        )
        errors = sync_layouts.check(self.root)
        self.assertTrue(any("block scalar" in item for item in errors))

    def test_check_reports_a_missing_description_without_raising(self) -> None:
        sync_layouts.sync(self.root)
        skill = self.root / sync_layouts.CANONICAL / "alpha" / "SKILL.md"
        skill.write_text("---\nname: alpha\n---\n\n# alpha\n", encoding="utf-8")
        errors = sync_layouts.check(self.root)
        self.assertTrue(any("description" in item for item in errors))

    def test_check_fails_when_frontmatter_name_drifts(self) -> None:
        skill = self.root / sync_layouts.CANONICAL / "alpha" / "SKILL.md"
        skill.write_text("---\nname: wrong\ndescription: Write alpha files.\n---\n\n# alpha\n", encoding="utf-8")
        errors = sync_layouts.validate(self.root, layouts_ready=False)
        self.assertTrue(any("frontmatter name" in item for item in errors))


class RepositoryLayoutTest(unittest.TestCase):
    def test_repository_layouts_match_the_source(self) -> None:
        errors = sync_layouts.check(ROOT)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
