# Changelog

## Unreleased

Added:
- `sdlc`: `sdlc-plan`, `sdlc-design`, `playbook`, `gh-issue-filing`, `gh-issue-template`, `architectural-decision-record`, `spike`.
- `repo-docs`: `tech-doc-readme`, `tech-doc-changelog`, `tech-doc-contributing`, `tech-doc-governance`, `tech-doc-codeowners`, `tech-doc-security`, `tech-doc-support`, `tech-doc-code-of-conduct`.
- `security-policy`: `security-baseline`, `security-api`, `security-llm`, `security-mcp`, `security-agent`, `compliance-gdpr`, `compliance-eu-ai-act`.
- `ai-engineering`: `prompt-engineering`, `prompt-evaluation`.
- `ops-incident`: `runbook`, `post-incident-calibration`, `post-incident-report`.
- `personal-standards`: `brand-personal`, `ux-personal`.
- `dev-review` 0.2.0: `pr-template`, `conventional-commits`.

Changed:
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
