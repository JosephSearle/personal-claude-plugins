---
name: pr-description
description: "Writes a clear pull request title and description from a diff. Use when the user asks to write, draft or improve a PR description, pull request summary or change summary."
---

# Pull request description

Write a description that lets a reviewer understand the change before reading the code.

## Inputs

A diff or list of changes, and the linked ticket if there is one. Infer the rest.

## Structure

1. **Title.** Imperative mood, under 72 characters. Example: `Add retry to payment webhook handler`.
2. **Why.** The problem or ticket, in two or three sentences.
3. **What changed.** Bullets grouped by area.
4. **How to test.** Steps a reviewer can follow.
5. **Risks.** Migrations, config changes, rollback steps.
6. **Links.** Ticket and related changes.

## Rules

1. Describe what the diff does. Do not claim behaviour the diff does not show.
2. Call out breaking changes at the top.
3. Do not include secrets, internal hostnames or personal data.
4. Keep it under 300 words unless the change is large.

## Output

The title and description in Markdown, ready to paste.
