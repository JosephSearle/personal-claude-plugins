---
name: proposal-draft
description: Drafts a first-version customer proposal from a deal summary. Use when someone in Sales asks to write a proposal, statement of work outline, pitch document or response to a customer request.
---

# Proposal draft

Turn a deal summary into a proposal a customer can approve.

## Inputs

A deal summary (see `deal-summary`), the scope agreed so far, and any customer template or required sections. Ask for the commercial terms. Do not invent prices or discounts.

## Process

1. **Executive summary** – the customer's goal, our approach and the outcome, in under 150 words.
2. **Understanding of need** – restate the problem so the customer recognises it.
3. **Scope** – in scope and out of scope, as lists.
4. **Approach and timeline** – phases with deliverables.
5. **Commercials** – placeholders for figures the user supplies.
6. **Assumptions and dependencies** – what we need from the customer.
7. **Next steps** – how to approve.

## Rules

- Write in the customer's terms, not internal product names.
- Every claim about outcomes must trace to the deal summary.
- Mark gaps as `[TO CONFIRM: ...]` for the account owner.

## Output

The proposal in Markdown, then the list of `[TO CONFIRM]` items.
