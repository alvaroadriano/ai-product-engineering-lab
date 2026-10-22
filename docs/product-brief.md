# Product brief: Product Evidence Copilot

## Problem

Product teams receive feedback across interviews, support conversations, and surveys. Summarizing a small sample can save time, but a fluent summary can obscure which statements are directly supported and which are assumptions.

## Target user

A product manager or researcher preparing an early discovery readout from a small, manually selected set of feedback.

## Job to be done

When I review a small set of user feedback, help me group recurring needs and trace each conclusion to its source, so I can decide what to investigate next without mistaking a draft synthesis for validated evidence.

## Proposed experience

1. Provide structured feedback with stable source IDs.
2. Generate a draft of themes, source IDs, exact example quotes, open claims, and research questions.
3. Review each theme against its cited source before copying anything into a product decision.
4. Record corrections and evaluation outcomes for future iterations.

## Scope for this prototype

- JSON input and JSON output
- Synthetic example dataset
- Transparent offline keyword baseline
- Optional structured model call through Pydantic AI
- Source-ID and verbatim-quote checks on model output
- Written evaluation rubric, without fabricated benchmark results

## Out of scope

- Connecting to production customer systems
- Automated roadmap prioritization or decision making
- User accounts, persistence, or collaboration
- Claims about customer impact, time savings, or model superiority
- Processing sensitive or identifiable customer data

## Success measures to test

- Evidence traceability: share of generated claims with valid source IDs
- Quote fidelity: share of representative quotes that exactly match input
- Unsupported-claim rate: reviewer-identified statements not supported by cited input
- Theme usefulness: reviewer rating against a defined rubric
- Review time: measured in a controlled task, not assumed
- Cost per run: provider-reported usage and current price schedule

These are proposed measures. No empirical result is claimed in this repository yet.
