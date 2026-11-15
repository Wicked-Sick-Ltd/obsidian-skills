# Obsidian

Skills for Obsidian Flavored Markdown, Bases, and JSON Canvas.

## Install

In Claude Code, from this fork:

```
/plugin marketplace add Wicked-Sick-Ltd/obsidian-skills
/plugin install obsidian@obsidian-skills
```

In Codex, run `codex plugin marketplace add Wicked-Sick-Ltd/obsidian-skills`, then install Obsidian from the plugin directory.

In Cursor, install from a checkout of this repository. Project skills are also linked at `.cursor/skills/`. See [docs/PORTING.md](../../docs/PORTING.md).

## Included skills

- obsidian-markdown: Obsidian links, properties, callouts, and embeds.
- obsidian-bases: Bases files, views, filters, formulas, and summaries.
- json-canvas: Canvas files with nodes, edges, groups, and connections.

These skills describe file formats. They do not run shell commands.

## Held back

Upstream also ships `obsidian-cli`, `obsidian-headless`, `defuddle`, and `knap`. This fork keeps that text in `held/` and does not link it into the plugin. The reasons are in [REVIEW.md](../../REVIEW.md).

## Scope

This plugin contains skills only, with no MCP server, hooks, or background processes.

Upstream: https://github.com/obsidianmd/obsidian-skills
