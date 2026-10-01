# personal-plugins

[![validate](https://github.com/JosephSearle/personal-claude-plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/JosephSearle/personal-claude-plugins/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A personal Claude Code plugin marketplace: a core plugin plus development and SDLC workflows, versioned in Git and usable in Claude and Microsoft 365 Copilot.

My own skills for day-to-day development and SDLC work, kept in one marketplace so I can install the same set wherever I use Claude Code.

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
/plugin install dev-review@personal-plugins
```

Also usable in Microsoft 365 Copilot — see [Microsoft 365 Copilot](#microsoft-365-copilot) — and can be synced org-wide via Claude Enterprise (Organization settings > Plugins & skills > Add > Sync from GitHub; the repo must be private or internal, public repos are rejected).

## Usage

Install `core` plus `dev-review`. Then ask in plain language. Skills load when the request matches their description.

| Say | Skill | Plugin |
| --- | --- | --- |
| "Review this pull request" | `pr-review` | `dev-review` |
| "Write the PR description" | `pr-description` | `dev-review` |
| "Redact this document" | `data-handling` | `core` |

## Structure

```mermaid
flowchart TB
    subgraph repo["Git repo: one marketplace"]
        core["core<br/>data-handling"]
        dev["dev-review<br/>pr-review, pr-description"]
    end
    all(["Every session"]) -->|Required| core
    all -->|Installed| dev
```

- **Core** holds what every session needs. It is required.
- **dev-review** holds development and SDLC workflows.
- Plugins do not import each other. All installed skills load into one session.
- Put shared rules in core. Put workflow knowledge in the dev-focused plugin.
- Keep each plugin to 3-10 skills. Copilot allows 20 per package.

```
.claude-plugin/marketplace.json     catalogue
plugins/<name>/
  .claude-plugin/plugin.json        name, version, description
  skills/<skill>/SKILL.md           the skills
scripts/validate.py                 repo checks
scripts/build-m365.sh               Copilot packages
.github/CODEOWNERS                  who approves what
.github/workflows/validate.yml      CI
```

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

Verified: both plugins build and pass `atk validate`.
Not verified: upload and deployment in a Microsoft 365 tenant.

Notes:
- Core and `dev-review` are separate packages. Deploy core to every tenant user and `dev-review` to whoever needs it.
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
