Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code, Codex, and Open Code.

## Wicked Sick fork

This fork reviews every upstream skill and links only the ones that passed into Cursor, Claude Code, Codex, Gemini CLI, and the Grok Bot skill library. The canonical files stay in `plugins/obsidian/skills/`. Generated layouts are symlinks. `python3 scripts/sync_layouts.py check` fails when they drift.

Passed and linked: `obsidian-markdown`, `obsidian-bases`, `json-canvas`.

Held in `held/` and not linked: `obsidian-cli`, `obsidian-headless`, `defuddle`, `knap`.

Details: [REVIEW.md](REVIEW.md) and [docs/PORTING.md](docs/PORTING.md).

Install a checkout of `wicked-main`. The repository default branch is `main`, which still has every upstream skill, so `owner/repo` marketplace commands install the held skills.

```sh
git clone --branch wicked-main --single-branch https://github.com/Wicked-Sick-Ltd/obsidian-skills.git
cd obsidian-skills
claude --plugin-dir "$PWD"
codex plugin marketplace add "$PWD"
gemini extensions install "$PWD"
```

Gemini can also install the branch directly: `gemini extensions install https://github.com/Wicked-Sick-Ltd/obsidian-skills --ref wicked-main`.

The upstream install commands are kept below so the fork can be compared with `obsidianmd/obsidian-skills`.

## Installation

### Claude Code marketplace

From terminal:

```sh
claude plugin marketplace add obsidianmd/obsidian-skills
claude plugin install obsidian@obsidian-skills
```

From within a Claude Code session:

```sh
/plugin marketplace add obsidianmd/obsidian-skills
/plugin install obsidian@obsidian-skills
```

To get new skills later, run `claude plugin update obsidian@obsidian-skills`.

### Codex marketplace

```sh
codex plugin marketplace add obsidianmd/obsidian-skills
```

Then install Obsidian from the plugin directory in Codex or the ChatGPT desktop app.

### Cursor

Install Obsidian from the [Cursor Marketplace](https://cursor.com/marketplace).

### npx skills

```sh
npx skills add https://github.com/obsidianmd/obsidian-skills
```

To use ssh instead, if you have a GitHub SSH key set up:

```sh
npx skills add git@github.com:obsidianmd/obsidian-skills.git
```

### Manually

#### Claude Code

Copy the `plugins/obsidian/skills/` directory to `.claude/skills/` in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex

Copy the `plugins/obsidian/skills/` directory into your Codex skills path (typically `~/.agents/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

#### OpenCode

Copy the three passing skill directories from `plugins/obsidian/skills/` into `~/.opencode/skills/`. OpenCode loads every `SKILL.md` it finds, so do not clone this whole repository into that folder: `held/` still contains the four skills that failed review, and a full clone would load them.

```sh
git clone --depth 1 --branch wicked-main https://github.com/Wicked-Sick-Ltd/obsidian-skills.git /tmp/obsidian-skills
cp -R /tmp/obsidian-skills/plugins/obsidian/skills/* ~/.opencode/skills/
```

The `cp` follows the real directories. Skills become available after restarting OpenCode.

## Release maintenance

Update the plugin version in every manifest with:

```sh
./scripts/bump.sh patch
```

The script also accepts `major`, `minor`, or an explicit version like `1.1.0`. After a version bump, run `python3 scripts/sync_layouts.py` so `gemini-extension.json` matches.

## Skills

| Skill                                                          | Description                                                                                                                                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [obsidian-markdown](plugins/obsidian/skills/obsidian-markdown) | Create and edit [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) (`.md`) with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax |
| [obsidian-bases](plugins/obsidian/skills/obsidian-bases)       | Create and edit [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`) with views, filters, formulas, and summaries                                                             |
| [json-canvas](plugins/obsidian/skills/json-canvas)             | Create and edit [JSON Canvas](https://jsoncanvas.org/) files (`.canvas`) with nodes, edges, groups, and connections                                                                        |
| [obsidian-cli](held/obsidian-cli) (held)                      | Interact with Obsidian vaults via the [Obsidian CLI](https://help.obsidian.md/cli) including plugin and theme development                                                                  |
| [obsidian-headless](held/obsidian-headless) (held)             | Sync and publish vaults from the command line with [Obsidian Headless](https://help.obsidian.md/headless), without the desktop app                                                         |
| [defuddle](held/defuddle) (held)                               | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle), removing clutter to save tokens                                                                |
| [knap](held/knap) (held)                                       | Render Markdown templates from JSON or CSV data using [Knap](https://github.com/obsidianmd/knap), including batch file generation                                                          |
