---
name: deal-summary
description: "Summarises a sales opportunity into a one-page deal brief with risks and next steps. Use when the user asks for a deal summary, opportunity brief, account update, pipeline review note or handover note."
---

# Deal summary

Turn notes, emails or CRM exports into a one-page brief a manager can read in two minutes. Apply the `brand-voice` skill for tone.

## Inputs

Take whatever the user provides: call notes, email threads, CRM fields. Ask only for what is critical and missing: customer, deal value, stage, close date.

## Structure

1. **Snapshot.** Customer, deal value, stage, expected close date, owner.
2. **Customer need.** One paragraph on the problem and why now.
3. **Decision process.** Who decides, who influences, who blocks. Use role titles, not personal details.
4. **Competition and alternatives.**
5. **Risks.** Rank by impact. Each risk gets an owner and a mitigation.
6. **Next steps.** Action, owner, date.
7. **Confidence.** Low, medium or high, with one sentence of evidence.

## Rules

1. Separate facts from assumptions. Mark assumptions.
2. Do not invent figures or dates. Write "Not stated" when information is missing.
3. Keep to one page.
4. Do not include personal data beyond role titles. Follow the `data-handling` skill.

## Output

The brief, then a list of the questions that would most raise confidence in the deal.
