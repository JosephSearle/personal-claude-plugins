---
name: pr-review
description: "Reviews a code change for correctness, security, tests and readability and returns prioritised findings. Use when the user asks to review a pull request, diff, patch or code change, or to check code before merge."
---

# Pull request review

Review a change and return findings a developer can act on.

## Inputs

A diff, patch or file contents, plus the intent of the change. If the intent is missing, infer it from the diff and state your assumption.

## Process

1. State what the change does in two sentences.
2. Check in this order:
   - **Correctness.** Logic errors, edge cases, error handling.
   - **Security.** Input validation, secrets, authentication, injection, unsafe dependencies.
   - **Tests.** Is new behaviour covered? Do tests assert outcomes?
   - **Readability.** Naming, structure, dead code, comments that explain why.
   - **Compatibility.** Breaking changes, migrations, performance impact.
3. Rank each finding: **Blocker**, **Should fix**, **Nit**.
4. For each finding give: location, the problem, a suggested fix.

## Rules

1. Cite the line or hunk for every finding.
2. Do not report style preferences as blockers.
3. Do not flag what you cannot see. List missing context separately.
4. If a secret appears in the diff, mark it Blocker and say it must be rotated.
5. Say what is good. One or two points.

## Output

A short summary, findings grouped by rank, then a verdict: Approve, Approve with changes, or Request changes.
