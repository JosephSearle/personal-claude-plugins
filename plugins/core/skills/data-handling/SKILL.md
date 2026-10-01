---
name: data-handling
description: "Keeps secrets, credentials and personal data out of outputs, saved files, commits and prompts. Use whenever the user shares or asks about API keys, tokens, passwords, connection strings, internal hostnames, or personal data, or asks to summarise, anonymise or redact logs, diffs or documents."
---

# Data handling

Secrets and personal data must never persist in skills, plugins, saved prompts, commit messages, PR descriptions or logs. This skill sets the rules for working with them in a session.

## Rules

1. **Never write a secret into a skill, template, commit message, PR description or reusable prompt.** Use placeholders: `[API_KEY]`, `[DB_PASSWORD]`, `[CUSTOMER_NAME]`.
2. **If a secret appears in a diff, log or pasted output, flag it and say it must be rotated.** Do not repeat it back, even redacted.
3. **Use only what the task needs.** Do not repeat personal data or internal identifiers in an output if a role, ID or placeholder works.
4. **Treat these as special-category and handle with extra care:** health, ethnicity, religion, sexual orientation, trade union membership, criminal records.
5. **Do not guess missing details.** Ask, or leave a placeholder.
6. **Do not retain or restate data from earlier tasks** in a new, unrelated task.

## Redaction

When asked to anonymise or redact logs, diffs or documents:

1. Replace names with role labels (`[USER_1]`).
2. Remove direct identifiers: email, phone, address, ID numbers, account numbers, tokens, keys, connection strings.
3. Generalise indirect identifiers: exact dates become months, internal hostnames become `[HOST]`.
4. List what you changed. Do not list the original values.

## When unsure

If the task seems to need data you may not be entitled to share, say so and ask before continuing.
