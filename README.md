# AI Product Engineering Lab

An independent product and technical exploration of evidence-grounded product discovery with generative AI.

**Product Evidence Copilot** turns a small set of synthetic customer feedback into a structured brief: themes, representative evidence, confidence, open questions, and claims that need validation. It includes a deterministic local mode and an optional provider-backed mode that can run the same task with OpenAI or Anthropic through Pydantic AI.

> This is a portfolio learning project. The feedback is fictional and the workflow is illustrative. A small baseline smoke evaluation is published; provider comparison results are not yet available.

## Why this project

Product teams often move quickly from scattered feedback to a confident-sounding roadmap request. This prototype explores a narrower question: **can an AI-assisted workflow make the evidence behind a product recommendation easier to inspect?**

The project demonstrates product framing, structured output, provider abstraction, source traceability, failure-aware evaluation planning, and explicit human review. It does not claim to replace user research or product judgment.

## Try it locally

~~~bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# No API key required: deterministic, rules-based baseline
python -m app --fixture

# Optional: run the same feedback through an LLM provider
cp .env.example .env
# Add one provider key and set MODEL in .env, then:
python -m app --fixture --provider

# Run the offline behavior checks
python -m unittest discover -s tests -v

# Run the traceability and fixture-label smoke evaluation
python evals/evaluate.py
~~~

Provider mode reads MODEL (for example, a current OpenAI or Anthropic model identifier) and the corresponding OPENAI_API_KEY or ANTHROPIC_API_KEY from the environment. Model availability and pricing change; check the provider's current documentation before use. API usage is billed separately from ChatGPT or Claude subscriptions.

To analyze your own data, pass a UTF-8 JSON file with the schema shown in [fixtures/feedback.json](fixtures/feedback.json):

~~~bash
python -m app --input path/to/feedback.json
~~~

Do not put confidential, personal, or customer-identifiable data into this demo.

## What the output contains

- Theme summaries tied to source IDs
- Representative feedback excerpts, copied from the input
- A simple confidence label, not a statistical confidence interval
- Unsupported or decision-critical claims to validate
- Suggested next questions for research

## Repository map

~~~text
app/          typed analysis schema, baseline, and optional LLM path
docs/         product brief, system design, and evaluation plan
evals/        synthetic reference labels, evaluation runner, and baseline report
fixtures/     fictional feedback used by the demo
tests/        checks for source traceability, baseline behavior, and evaluation rules
~~~

## Curated open-source projects

These are upstream projects to study or build on, not code copied into this repository. Verify each license and its terms before incorporating code.

| Project | Why it is relevant here |
| --- | --- |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Typed agent framework with OpenAI and Anthropic providers; used as the optional model layer. |
| [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) | Product-management workflows for research synthesis, specs, roadmaps, and stakeholder updates; useful workflow reference. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Gateway approach for routing across many LLM providers; a possible next step for managed evaluation and cost tracking. |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Turns code and documentation into a queryable knowledge graph; worth exploring for traceability across larger product evidence sets. |

## Product and engineering decisions

- Start with a rules-based offline baseline so the workflow can be inspected without model calls.
- Keep source IDs attached to themes and examples so reviewers can trace generated claims back to input.
- Use one typed output contract for both model providers.
- Treat model output as a draft. Human review remains a required step before decisions.
- Evaluate evidence grounding and unsupported claims before optimizing for speed or cost.

See [docs/product-brief.md](docs/product-brief.md), [docs/architecture.md](docs/architecture.md), and [docs/evaluation-plan.md](docs/evaluation-plan.md).

## Current status

Prototype and learning project. The offline baseline, three unit tests, and a small traceability smoke evaluation are runnable. On the six-item fictional fixture, the baseline matched the author-written reference labels and preserved its cited source IDs and quotes. This is not independent evidence of usefulness or model quality. OpenAI and Anthropic runs, blind human review, cost, and latency have not been measured. See the [baseline report](evals/baseline-report.json) and [evaluation plan](docs/evaluation-plan.md) for scope and limitations.

## About the author

Alvaro Adriano is a product leader focused on enterprise platforms, B2B workflows, and integrations. This independent project extends his portfolio toward hands-on technical product work in AI-enabled workflows.

## License

This project is released under the MIT License. Upstream repositories listed above retain their own licenses.
