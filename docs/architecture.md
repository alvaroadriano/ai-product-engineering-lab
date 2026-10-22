# Architecture

## Current flow

1. CLI loads a JSON dataset and validates it with Pydantic models.
2. The offline path groups feedback using visible keyword rules.
3. The optional model path sends the same dataset to a configured model through Pydantic AI and requests the same typed output contract.
4. A validation pass removes unknown source IDs and quotes that do not exactly match cited input records.
5. The CLI prints the draft as JSON; the human remains responsible for review.

## Boundaries and risks

| Boundary | Current behavior | Risk or follow-up |
| --- | --- | --- |
| Input | Local JSON file | Add validation limits and explicit data-retention guidance before accepting larger inputs. |
| Model provider | Selected via `MODEL`; provider key from environment | Provider terms, retention, data location, availability, and cost must be assessed before real data use. |
| Output | Structured JSON | Schema-valid output can still be misleading; source validation does not prove a theme is correct. |
| Persistence | None | Output is printed locally; no database or telemetry is configured. |
| Human review | Required by product design | A future UI should make source inspection and edits easy, not hide uncertainty. |

## Failure handling in this version

- Invalid input fails during schema validation.
- Missing model configuration returns a CLI usage error.
- Provider/network errors are surfaced by the runtime; there is no silent retry or fallback.
- Unknown citations and non-verbatim quotes are removed from the returned model draft.
- The output includes limitations and is explicitly labeled as a draft.

## Next technical steps

1. Add bounded input size and request timeout handling.
2. Capture provider, model, latency, token usage, and errors for repeatable evaluation while avoiding feedback retention.
3. Compare model outputs with the baseline using the rubric in `evaluation-plan.md`.
4. Add a reviewer interface only after evidence shows that manual traceability is cumbersome.
