# Changelog

## Unreleased

Added:
- `core` 0.2.0: `security-baseline`, `security-api`, `security-llm`, `security-mcp`, `security-agent`, `compliance-gdpr`, `compliance-eu-ai-act`, `brand-personal`, `ux-personal`. Policies live in core so every plugin can use them.
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
