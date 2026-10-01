---
name: data-handling
description: "Keeps personal and confidential data out of outputs, saved files and prompts. Use whenever the user shares or asks about names, contact details, salaries, health, performance or customer records, or asks to summarise, anonymise or redact a document."
---

# Data handling

Personal data must never persist in skills, plugins, saved prompts or reusable templates. This skill sets the rules for working with it in a session.

## Rules

1. **Never write personal data into a skill, template or reusable prompt.** Use placeholders: `[CANDIDATE_NAME]`, `[CUSTOMER_NAME]`, `[SALARY]`.
2. **Use only what the task needs.** Do not repeat personal data in an output if a role, ID or placeholder works.
3. **Treat these as special-category and handle with extra care:** health, ethnicity, religion, sexual orientation, trade union membership, criminal records, and any performance or disciplinary detail.
4. **Do not infer protected characteristics** from names, photos or writing style.
5. **Do not guess missing details.** Ask, or leave a placeholder.
6. **Do not retain or restate data from earlier tasks** in a new, unrelated task.

## Redaction

When asked to anonymise or redact:

1. Replace names with role labels (`[CANDIDATE_1]`).
2. Remove direct identifiers: email, phone, address, ID numbers, account numbers.
3. Generalise indirect identifiers: exact dates become months, small locations become regions.
4. List what you changed. Do not list the original values.

## When unsure

If the task seems to need data the user may not be entitled to share, say so and ask them to check with their data protection contact before continuing.
