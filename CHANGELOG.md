# Changelog

## Unreleased

Added:
- `hr-recruiting` 0.1.0: `job-advert`, `interview-scorecard`. Example department plugin.
- `sales-deal-desk` 0.1.0: `deal-summary`, `proposal-draft`. Example department plugin.
- `mktg-content` 0.1.0: `content-brief`, `campaign-plan`. Example department plugin.
- `enterprise/plugin-access.yaml`: per-group plugin access for Claude Enterprise.
- `scripts/access.py`: checks the access policy, renders the access matrix and resolves what a member of given groups gets.
- `docs/enterprise/`: Enterprise runbook, spike findings and generated access matrix.
- `docs/runbooks/promote-plugin-release.md`: release, pilot, promotion and rollback runbook for Claude and Copilot.
- `claude-pilot` group and `stage: pilot` in the access policy. `scripts/access.py` checks pilot plugins reach only pilot groups.
- `scripts/package-plugin.py` and a `preview-packages` CI job: zips of changed plugins on every pull request for pilot testers.
- `core` 0.2.0: `security-baseline`, `security-api`, `security-llm`, `security-mcp`, `security-agent`, `compliance-gdpr`, `compliance-eu-ai-act`, `brand-personal`, `ux-personal`. Policies live in core so every plugin can use them.
- `dev-review` 0.2.0: `pr-template`, `conventional-commits`.

Changed:
- README: removed the beta-branch channel. Organisation sync reads only the default branch.
- `scripts/validate.py`: runs the access policy checks and fails if the access matrix is out of date.
- CODEOWNERS: department plugin and policy entries, with the Enterprise team to use for each.
- `dev-review` 0.2.0: `pr-description` replaced with the version from the skills catalogue.
- `scripts/validate.py`: trigger-phrase check accepts "whenever", "triggers on" and "asks to"; documentation placeholder emails (example.com, project.org) no longer fail the personal-data scan.

## 0.1.0 - 2026-10-01

Added:
- Marketplace `personal-plugins`.
- `core`: `data-handling`.
- `dev-review`: `pr-review`, `pr-description`.
- `scripts/validate.py` and a `validate` GitHub Actions workflow.
- `scripts/build-m365.sh` for Microsoft 365 Copilot packages.
- CODEOWNERS.
