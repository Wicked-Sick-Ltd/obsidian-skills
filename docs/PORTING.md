# Porting Obsidian skills

One directory is the source for every tool. The other layouts are symlinks, plus two generated files. `scripts/sync_layouts.py` writes them, and CI rejects a checkout that has drifted.

## Verdicts

Review lives in [REVIEW.md](../REVIEW.md). A skill is linked only when that review says it passed.

| State | Skills | Where the files are |
| --- | --- | --- |
| Passed | `json-canvas`, `obsidian-bases`, `obsidian-markdown` | `plugins/obsidian/skills/<name>/` |
| Held | `defuddle`, `knap`, `obsidian-cli`, `obsidian-headless` | `held/<name>/` |

Edit a passing skill in `plugins/obsidian/skills/<name>/`. That directory is real files, including any `references/` next to `SKILL.md`. Do not edit a symlink target's copy under `.cursor/`, `.claude/`, `.agents/skills/`, or `.grok/`. Those paths point back here.

Held skills stay in the repository so the review can be checked. They are not installed by the plugin and they are not linked into any tool layout.

## Layouts

| Tool | Path | What it is |
| --- | --- | --- |
| Canonical source | `plugins/obsidian/skills/<name>/` | Real skill directory. Claude Code, Cursor, and Codex plugin installs read this through `plugins/obsidian`. |
| Cursor project skills | `.cursor/skills/<name>` | Symlink to the canonical directory. |
| Claude Code project skills | `.claude/skills/<name>` | Symlink to the canonical directory. The marketplace plugin also exposes the same files. |
| Codex | `.agents/skills/<name>` and `AGENTS.md` | Symlink per skill, plus a generated index. The Codex marketplace entry remains `.agents/plugins/marketplace.json`. |
| Gemini CLI | `gemini-extension.json` and `skills` | The manifest is generated. `skills` is a symlink to `plugins/obsidian/skills`, which is the directory Gemini discovers. |
| Grok Bot shared library | `.grok/skills/<name>` | Symlink to the canonical `SKILL.md`. The file already has Agent Skills frontmatter (`name`, `description`). |

`AGENTS.md` and `gemini-extension.json` are generated. The Gemini manifest's `version` is copied from `plugins/obsidian/plugin.json`.

Install one route per tool. A checkout of this repository contains both the plugin and the project-skill links, and loading both in one session shows the same three skills twice.

Cursor's local plugin folder skips a symlink whose target sits outside that folder. The plugin directory itself holds the real files, so copying `plugins/obsidian` is enough for Cursor and Claude Code. The project links assume the whole checkout is present.

## Refresh

```sh
python3 scripts/sync_layouts.py
python3 scripts/sync_layouts.py check
python3 -m unittest tests/test_sync_layouts.py
```

`check` fails when:

- `plugins/obsidian/skills/` is not exactly the passing set, or a passing skill's frontmatter `name` does not match its directory
- `held/` is not exactly the held set, or a held skill is linked from a layout
- a layout entry is missing, extra, or not the expected relative symlink
- `AGENTS.md` or `gemini-extension.json` differs from the generator output

CI runs the same check on pull requests and on pushes to `wicked-main` (`.github/workflows/layouts.yml`).

After `./scripts/bump.sh`, run `python3 scripts/sync_layouts.py` so the Gemini manifest picks up the new version.
