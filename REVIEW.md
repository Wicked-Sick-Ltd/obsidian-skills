# Review of obsidianmd/obsidian-skills

Reviewed on 15 November 2026 from Wicked-Sick-Ltd/obsidian-skills at upstream commit `3981277` (`1.2.0`, pushed 11 November 2026). Seven skills. Three pass and are linked into the tool layouts. Four fail and stay in `held/`. Nothing here was opened upstream.

## How a skill passes

A skill passes only when all of the following are true:

1. It does not instruct the agent to run shell commands, make network calls, execute code, or handle credentials.
2. It does not contain prompt-injection-style instructions.
3. It does not duplicate or clash with a skill Wicked Sick already ships.

Anything else fails. Failing skills are not linked into Cursor, Claude Code, Codex, Gemini CLI, or the Grok Bot library. Their upstream text is unchanged under `held/<name>/`.

## Overlap with skills we already ship

No skill here duplicates or clashes with one we already ship.

Checked sources:

- [Wicked-Sick-Ltd/awesome-copilot](https://github.com/Wicked-Sick-Ltd/awesome-copilot) branch `wicked-main` at `8d28b361` (7 November 2026). The tree has 460 `SKILL.md` files. No path contains `obsidian`, `defuddle`, `knap`, `json-canvas`, or `bases`. A content search for those names, plus `wikilink` and `json canvas`, in that repository returned nothing.
- Organisation code search for `obsidian` inside `filename:SKILL.md` returned 0 hits, including private repositories visible to this token. That search covers default branches. `awesome-copilot`'s default branch is `wicked-main`.
- `public-universe` skills (`tonight-sky`, `lesson-builder`, `space-fact-check`, `object-explainer`, `close-approach-watch`, `sky-this-week`, `publicuniverse-data-audit`) are astronomy workflows.
- `semrush-dashboard` `.cursor/skills/` is `pest-testing`, `fluxui-development`, `fortify-development`, `livewire-development`, `laravel-best-practices`, and `tailwindcss-development`.
- Other organisation skill directories found in the same search (`pr-flow`, `token-usage`, `network-probe`, `wicked-repo-inventory`, and the project skills under `wicked-brier`, `wickedprints-site`, `wicked-dashboard`, `knightwatch-intel`, `osint-stack`, `wicked-kids-safe-ai`) are product or engineering workflows, not Obsidian formats.

Nearby skills in `awesome-copilot`, and why they are not a clash:

| Existing skill | Why it is not the same job |
| --- | --- |
| `markdown-to-html` | Converts Markdown to HTML with marked.js, pandoc, Hugo, or Jekyll. `obsidian-markdown` writes Obsidian Flavored Markdown and does not render HTML. |
| `convert-plaintext-to-md`, `convert-word-to-md`, `convert-pdf-to-md`, `convert-excel-to-md`, `md-to-docx` | Turn office or plain documents into or out of Markdown. They do not describe wikilinks, callouts, or properties. |
| `content-management-systems` | WordPress, Shopify, Drupal, Webflow, and similar. The description does not name Obsidian. |
| `excalidraw-diagram-generator`, `draw-io-diagram-generator`, `drawio` | Other diagram files. `json-canvas` writes Obsidian `.canvas` JSON (spec 1.0) and says so in its description. |

## Verdicts

| Skill | Verdict | Why |
| --- | --- | --- |
| `obsidian-markdown` | Pass | Format instructions for Obsidian Flavored Markdown. No shell, network, code execution, credentials, or injection. No shipped duplicate. |
| `obsidian-bases` | Pass | Format instructions for `.base` files. Same security result. No shipped duplicate. |
| `json-canvas` | Pass | Format instructions for JSON Canvas. Link nodes store a URL as data. The skill tells the agent to write the file, not to fetch the URL. |
| `obsidian-cli` | Fail | Tells the agent to run the `obsidian` shell command, including `obsidian eval`, which runs JavaScript inside the Obsidian app. |
| `obsidian-headless` | Fail | Tells the agent to run `ob`, to sync and publish over the network, and to drive login that takes an email, password, 2FA code, and an encryption password. |
| `defuddle` | Fail | Tells the agent to run `defuddle parse <url>`, which fetches an arbitrary page into the conversation, and offers `npm install -g defuddle`. |
| `knap` | Fail | Tells the agent to run `knap` via a global install or `npx`, and includes a pipeline that feeds a fetched page into a template. |

## Security flags

No skill contains prompt-injection-style instructions. None tell the agent to ignore earlier rules, to prefer untrusted text over the user, or to reveal secrets. `defuddle` and the Knap pipeline can still place remote page text into context. That is an indirect injection path, and it is part of why those two fail.

| Skill | Shell | Network | Code execution | Credentials | Prompt injection |
| --- | --- | --- | --- | --- | --- |
| `obsidian-markdown` | No | No | No | No | No |
| `obsidian-bases` | No | No | No | No | No |
| `json-canvas` | No | No | No | No | No |
| `obsidian-cli` | Yes, `obsidian` | No | Yes, `obsidian eval` runs JavaScript in the app. The skill says not to install the unrelated npm package `obsidian-cli`. | No | No |
| `obsidian-headless` | Yes, `ob` | Yes, Sync and Publish, plus `npm install -g obsidian-headless` | The npm install runs a registry package | Yes. Login uses email, password, and 2FA. Encrypted vaults ask for the encryption password. The skill says not to ask for the password or pass `--password`, and to let the user type it in their own terminal. `ob logout` and `sync-unlink` clear stored credentials. | No |
| `defuddle` | Yes, `defuddle` | Yes, fetches the URL it is given. `npm install -g defuddle` pulls a registry package | The npm install runs that package | No | No instruction of that kind. Fetched pages become model context. |
| `knap` | Yes, `knap` / `npx knap` | `npm install -g knap` and `npx` pull a registry package. The documented Defuddle pipe fetches a page first | The npm or npx install runs that package | No | No instruction of that kind. Rendered page content becomes model context. |

`obsidian-headless` also documents `ob publish --yes` and `--all`. `--all` publishes every file, not only notes marked `publish: true`. The skill says to confirm first. The capability is still a vault upload, so the skill fails the port gate.

`obsidian-cli` documents `delete` (trash) and says not to pass `permanent` unless the user asks. It also documents developer commands: plugin reload, console capture, screenshots, and DOM inspection. Those are further shell and app-control instructions.

## What each skill does, and its quality

### `obsidian-markdown` (pass)

Creates and edits Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties, tags, comments, highlights, math, Mermaid, and footnotes. Standard CommonMark is treated as known. Reference files cover callouts, embeds, and property types.

Quality is high. The workflow is ordered, the examples are valid, and the pitfalls are specific: alias pipes inside tables, a blank line before a table, aliases that do not resolve as `[[Alias]]`, and tags that must contain a non-numeric character. Links point at help.obsidian.md. Frontmatter `name` matches the directory. The description is specific enough that a general Markdown-to-HTML skill should not be selected for an Obsidian note.

### `obsidian-bases` (pass)

Creates and edits `.base` YAML: filters, formulas, properties, summaries, and table, card, list, map, and kanban views. `references/FUNCTIONS_REFERENCE.md` is the function catalog.

Quality is high. It records the rules that are easy to get wrong: `note.` prefixes on display names, duration math through `.days` before rounding, uppercase `ASC`/`DESC`, and YAML quoting. Kanban matches the current help text (Obsidian 1.14+, `groupOrder`, which cards can move). The skill is long, and the function list is a catalog rather than a tutorial, which is the right shape for this format.

Upstream pull request [#116](https://github.com/obsidianmd/obsidian-skills/pull/116) fixed a loader footgun where a backtick after `!` could be read as a shell command. This tree has that fix: the `!` example sits inside a code span and is not followed by a backtick.

### `json-canvas` (pass)

Creates and edits `.canvas` files to JSON Canvas spec 1.0: text, file, link, and group nodes, edges, colours, and ids. `references/EXAMPLES.md` holds full canvases.

Quality is high. The workflows say to validate ids and edge endpoints. It calls out JSON escaping, real newlines versus `\n`, and CJK width. It says to write the file directly and not to use `obsidian create content=`, which would break the JSON. That warning does not tell this fork's agents to run the CLI. The skill does not tell the agent to open link-node URLs.

### `obsidian-cli` (fail)

Drives a running Obsidian app through the `obsidian` command: read, create, search, rename, move, delete, properties, tasks, and plugin or theme debugging.

Quality of the writing is high, and the guardrails are real: quote arguments, pass note text as data, do not install the npm package named `obsidian-cli`, ask which vault when several exist, prefer `rename` and `move` over filesystem `mv`, and prefer dedicated commands over `eval` for note bodies. It still teaches `obsidian eval code=...` and a shell workflow, so it fails.

Open upstream issue [#141](https://github.com/obsidianmd/obsidian-skills/issues/141) (6 September 2026) reports that `base:query` and `base:views` do not follow the skill's `file` / `path` rules. The issue already asks for a doc note. Do not refile it.

### `obsidian-headless` (fail)

Runs Obsidian Sync and Publish with the `ob` command, without the desktop app. It requires Node.js 22 and a subscription.

Quality is high. The credential section is the careful kind: do not ask for the password, do not pass `--password`, let the user complete `ob login` and the encryption prompt in their own terminal. It also says to confirm the vault before changing remote state, to back up before the first sync, and not to mix desktop Sync with Headless Sync on the same vault. The skill still handles credentials and uploads vault contents, so it fails.

### `defuddle` (fail)

Extracts readable Markdown from a web page with `defuddle parse <url> --md`.

Quality is adequate and short. It says not to claim success when the tool is missing or errors. It is a network fetch of a caller-supplied URL plus a global npm install, so it fails.

### `knap` (fail)

Renders Markdown templates from JSON or CSV with the Knap CLI, including batch output and a Defuddle-to-note pipeline.

Quality is good. It separates template source from data source, describes `--dry-run` and `--overwrite`, and says filename templates must not contain directories. It is still a shell tool reached through npm or npx, and the pipeline pulls a remote page into the template, so it fails.

## Licence

[MIT](LICENSE). Copyright (c) 2026 Steph Ango (@kepano). The notice is in `LICENSE` and is kept on this fork. MIT allows use, modification, and distribution when that notice stays with the software.

## Contributing upstream

Upstream is [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). It is active, and small pull requests are being merged. There is no written contribution guide.

Facts checked on 15 November 2026:

- Created 2 January 2026. Default branch `main`. Last push 11 November 2026, commit `3981277`, message `1.2.0`, author kepano. About 52,679 stars and 3,750 forks. Not archived. Issues and pull requests are open (`pull_request_creation_policy: all`).
- Root contains `LICENSE`, `README.md`, `plugins/`, `scripts/`, and the Claude, Cursor, and Codex marketplace manifests. There is no `CONTRIBUTING.md`, no pull request template, and no `.github/` directory.
- On 11 November 2026 kepano merged outside work, including [#75](https://github.com/obsidianmd/obsidian-skills/pull/75) (Headless skill), [#84](https://github.com/obsidianmd/obsidian-skills/pull/84) and [#96](https://github.com/obsidianmd/obsidian-skills/pull/96) (docs), [#116](https://github.com/obsidianmd/obsidian-skills/pull/116) (Bases loader fix), and [#153](https://github.com/obsidianmd/obsidian-skills/pull/153) (property types and kanban). The same day he closed other pull requests without merging them.
- Open issues at review time: [#159](https://github.com/obsidianmd/obsidian-skills/issues/159) (what a future MCP would add, opened 15 November 2026), [#141](https://github.com/obsidianmd/obsidian-skills/issues/141) (CLI base targeting), [#50](https://github.com/obsidianmd/obsidian-skills/issues/50) (read `.obsidian` settings). No maintainer reply on those three yet.

**Verdict: contributing a narrow fix back is viable. This port is not that fix.** Recent merges are short documentation and skill corrections in the existing voice. There is no contribution document to follow beyond that pattern. The multi-tool layout and the decision to hold four skills are Wicked Sick policy for `wicked-main`. Sending that policy upstream would fight the plugin upstream already publishes, which intentionally includes the CLI, Headless, Defuddle, and Knap skills.

### Candidate, not opened

**Gemini CLI manifest aimed at `plugins/obsidian/skills/`.**

Upstream pull request [#56](https://github.com/obsidianmd/obsidian-skills/pull/56) added `gemini-extension.json` and was closed on 11 November 2026 by kepano without a merge. The stated reason: "The skills moved to `plugins/obsidian/skills/` in 1.1.0, so this manifest no longer finds them. Closing this for now." That is a stale path, not a rejection of Gemini support. A replacement that keeps the manifest at the repository root and points Gemini at the current `plugins/obsidian/skills/` directory (a `skills` symlink is enough, which is what Gemini discovers) would match the reason the last attempt was closed. It should list every upstream skill, not this fork's passing subset.

Do not open that pull request from here. Craig decides whether to send it. Do not refile [#141](https://github.com/obsidianmd/obsidian-skills/issues/141); it is already open, and `obsidian-cli` is held on this fork.
