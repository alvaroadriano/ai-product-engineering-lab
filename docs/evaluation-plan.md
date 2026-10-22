# Model evaluation plan

## Question

For the same small synthetic feedback set, do model-backed drafts improve theme usefulness and evidence traceability over the transparent keyword baseline, at an acceptable cost and review burden?

## Comparison setup

- Input: the same fixed dataset for every run
- Systems: offline keyword baseline, one configured OpenAI model, one configured Anthropic model
- Prompt and schema: held constant across model runs
- Repetitions: at least three per model to reveal output variability
- Review: blind reviewers score outputs without seeing the provider name
- Data: synthetic feedback only for the initial evaluation

## Rubric (1–5)

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence grounding | Most themes lack valid evidence | Most themes cite relevant items | Every claim is traceable and appropriately bounded |
| Theme usefulness | Groups are incoherent | Groups are partly actionable | Groups clarify a distinct user need and next step |
| Quote fidelity | Quotes are invented or altered | Some quotes are exact | Every quoted excerpt matches its source exactly |
| Uncertainty handling | Makes prevalence or impact claims without support | Some uncertainty is named | Limits, assumptions, and validation needs are clear |
| Review effort | Requires substantial reconstruction | Reviewer can verify with effort | Reviewer can quickly inspect and correct the draft |

## Measures

- Valid source-citation rate
- Exact quote match rate
- Unsupported-claim count per output
- Mean blind reviewer score by dimension
- Median completion and review time
- Provider-reported token usage and cost per run
- Failure rate and schema-valid output rate

## Decision rule

Do not call a model better based on one example or a small score difference. Review failure cases, inter-reviewer disagreement, and cost. Publish model names, run counts, dataset version, date, and caveats with any eventual result. A model remains a drafting aid even if it scores higher.

## Initial baseline run

The deterministic offline baseline was run once on fixture-v1 on 2026-10-22. The reproducible output is [baseline-report.json](../evals/baseline-report.json); rerun it with python evals/evaluate.py.

The six feedback items had 100% valid citation IDs, 100% exact-quote rate, 100% coverage, and 1.00 precision, recall, and F1 against the author-written theme/source labels. The heuristic did not flag unsupported-claim language. These are mechanical smoke-test results on a tiny fixture whose labels were not independently reviewed. They do not show that the themes are useful, representative, or better than an LLM output.

OpenAI and Anthropic provider runs have not been performed. The next benchmark step is three runs per provider, followed by blind human scoring for usefulness, grounding, uncertainty, and review effort. No model winner or provider quality, cost, or latency claim is published.
