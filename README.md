# personal-plugins

[![validate](https://github.com/JosephSearle/personal-claude-plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/JosephSearle/personal-claude-plugins/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A personal Claude Code plugin marketplace: my SDLC, docs, security, prompt and incident skills in eight plugins, versioned in Git and usable in Claude and Microsoft 365 Copilot.

My own skills for day-to-day AI engineering and SDLC work, kept in one marketplace so I can install the same set wherever I use Claude Code. Skills are authored in the plugins here; each plugin is one on/off switch for a kind of work.

<details>
<summary>Table of Contents</summary>

- [Install](#install)
- [Usage](#usage)
- [Structure](#structure)
- [Skills only](#skills-only)
- [Governance](#governance)
- [Versioning](#versioning)
- [Microsoft 365 Copilot](#microsoft-365-copilot)
- [Limits](#limits)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

</details>

## Install

```
/plugin marketplace add JosephSearle/personal-claude-plugins
/plugin install core@personal-plugins
/plugin install sdlc@personal-plugins
```

Install `core` everywhere, then add the plugins that match the work in front of you (see [Usage](#usage)).

Also usable in Microsoft 365 Copilot — see [Microsoft 365 Copilot](#microsoft-365-copilot) — and can be synced org-wide via Claude Enterprise (Organization settings > Plugins & skills > Add > Sync from GitHub; the repo must be private or internal, public repos are rejected).

## Usage

Ask in plain language. Skills load when the request matches their description.

| Plugin | Skills | Install when |
| --- | --- | --- |
| `core` | `data-handling` | Always. Keeps secrets and personal data out of outputs. |
| `dev-review` | `pr-review`, `pr-description`, `pr-template`, `conventional-commits` | Working through branches, commits and pull requests. |
| `sdlc` | `sdlc-plan`, `sdlc-design`, `playbook`, `gh-issue-filing`, `gh-issue-template`, `architectural-decision-record`, `spike` | Taking an idea from intent to spec, or recording a decision or spike. |
| `repo-docs` | `tech-doc-readme`, `tech-doc-changelog`, `tech-doc-contributing`, `tech-doc-governance`, `tech-doc-codeowners`, `tech-doc-security`, `tech-doc-support`, `tech-doc-code-of-conduct` | Creating or auditing repository documents. |
| `security-policy` | `security-baseline`, `security-api`, `security-llm`, `security-mcp`, `security-agent`, `compliance-gdpr`, `compliance-eu-ai-act` | Designing a project or spec that needs a security or compliance review. |
| `ai-engineering` | `prompt-engineering`, `prompt-evaluation` | Writing prompts for Claude and measuring them. |
| `ops-incident` | `runbook`, `post-incident-calibration`, `post-incident-report` | Writing runbooks or running a post-incident review. |
| `personal-standards` | `brand-personal`, `ux-personal` | My own projects only: voice, naming, UX and accessibility. |

`brand-personal`, `ux-personal` and the `security-policy` skills state they apply to my own projects, not an employer's. They live in their own plugins so they stay off in work contexts.

Example requests:

| Say | Skill |
| --- | --- |
| "Write the PR description for this branch" | `pr-description` |
| "Capture this idea as an intent.md" | `sdlc-plan` |
| "Audit my README" | `tech-doc-readme` |
| "Harden this system prompt" | `prompt-engineering` |
| "Review the security of this MCP server design" | `security-mcp` |

## Structure

```mermaid
flowchart TB
    subgraph repo["Git repo: one marketplace"]
        core["core<br/>data-handling"]
        dev["dev-review<br/>PR workflow"]
        sdlc["sdlc<br/>intent to spec"]
        docs["repo-docs<br/>repository documents"]
        sec["security-policy<br/>security and compliance"]
        ai["ai-engineering<br/>prompts and evals"]
        ops["ops-incident<br/>runbooks and reviews"]
        std["personal-standards<br/>brand and UX"]
    end
    all(["Every session"]) -->|Always| core
    all -->|As needed| dev
    all -->|As needed| sdlc
    all -->|As needed| docs
    all -->|As needed| sec
    all -->|As needed| ai
    all -->|As needed| ops
    all -->|Own projects only| std
```

- **Skills live inside the plugin that owns them.** A plugin installs as a cached copy of its own folder, so a skill outside it would not ship.
- **Group by shared use.** `sdlc-design` links to `../sdlc-plan/SKILL.md`, so those two stay in the same plugin. Skills that assume another skill by name (for example `security-*` assume `security-baseline`) sit together.
- **Core** holds what every session needs.
- Plugins do not import each other. All installed skills load into one session.
- Keep each plugin to 10 skills or fewer. Copilot allows 20 per package.

```
.claude-plugin/marketplace.json     catalogue
plugins/<name>/
  .claude-plugin/plugin.json        name, version, description
  skills/<skill>/SKILL.md           the skills (plus references/, assets/, scripts/)
scripts/validate.py                 repo checks
scripts/build-m365.sh               Copilot packages
.github/CODEOWNERS                  who approves what
.github/workflows/validate.yml      CI
```

Skills were imported from [JosephSearle/skills](https://github.com/JosephSearle/skills) `catalog/`. Their `evals/` folders are left behind in that repo, so test fixtures are not shipped to installs.

## Skills only

This release has skills only: no commands, sub-agents, hooks or connectors.

- Copilot does not load commands, sub-agents or hooks. Anything essential lives in skills so both products behave the same.
- Connectors come later, once a specific tool needs one.
- No secrets or personal data in any skill. The `data-handling` skill enforces placeholders, and CI scans for emails, API keys, tokens and National Insurance numbers.

## Governance

Every change goes through a pull request and must pass CI before merging.

1. CI runs `scripts/validate.py --base <target branch>`. It checks:
   - marketplace and plugin manifests, kebab-case names, semver
   - each skill's name matches its folder and has a description of 1-1024 characters
   - skill count against the Copilot limit
   - no top-level `bin/`
   - every plugin has a CODEOWNERS entry
   - no secrets or personal data
   - the plugin version is bumped when its files change
2. Try the change in a live Claude Code session before merging.

See [Contributing](#contributing) for how to run these checks locally before opening a pull request.

## Versioning

- Semantic versioning, set in `plugin.json` only. Never in `marketplace.json`.
- Bump on every change to a plugin. Claude Code updates only when the version changes.
- MAJOR: skill renamed or removed. MINOR: skill added. PATCH: wording fix.
- Record each release in [CHANGELOG.md](CHANGELOG.md), newest first.
- Claude organisation sync reads the default branch only. A tag alone releases nothing. Merge the pull request to release.
- For a beta channel, sync a second marketplace from a `beta` branch to a pilot group.
- Never rename a plugin. The name is the install identifier.

## Microsoft 365 Copilot

Skills use the open Agent Skills format, so the same files work in Copilot Cowork. Copilot needs a zip per plugin.

```
npm install -g @microsoft/m365agentstoolkit-cli
PRIVACY_URL=https://example.com/privacy \
TERMS_URL=https://example.com/terms \
WEBSITE_URL=https://example.com \
  scripts/build-m365.sh
```

Output: `build/m365/<plugin>.zip`. The script imports each plugin with `atk`, sets manifest schema v1.28 and the display name, validates, and packages.

Verified: all eight plugins build and pass `atk validate`.
Not verified: upload and deployment in a Microsoft 365 tenant.

Notes:
- Each plugin is a separate package. Deploy `core` to every tenant user and the others to whoever needs them.
- An admin sets which users or groups see each package.
- Users need a Microsoft 365 Copilot licence.
- Copilot does not load `commands/`, `agents/` or `hooks/`.

## Limits

- No plugin declares a dependency on core. Core is made present by convention (install it first). Claude Code plugin dependencies could express this; not used here.
- Org-wide Enterprise sync and Microsoft 365 group assignment both need the respective admin plans. Not needed for personal, single-user use.

## Maintainers

Maintained by [Joseph Searle](https://github.com/JosephSearle). See [CODEOWNERS](.github/CODEOWNERS).

## Contributing

Open a pull request against `main`. See [Governance](#governance) for the review and rollout process. Before submitting, run the same checks CI runs:

```bash
pip install pyyaml
python scripts/validate.py
claude plugin validate .
```

## License

MIT © 2026 Joseph Searle. See [LICENSE](LICENSE).
