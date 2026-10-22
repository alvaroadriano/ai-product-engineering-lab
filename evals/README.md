# Evaluation harness and cases

The initial fixture lives in fixtures/feedback.json; author-written reference labels are in reference.json. Run the deterministic baseline smoke evaluation from the repository root:

~~~bash
python evals/evaluate.py
~~~

To run the configured provider once, set MODEL and the matching provider API key, then run python evals/evaluate.py --provider. The provider run is a single exploratory sample, not a benchmark. The fuller plan requires at least three runs per provider and blind human review.

The runner checks source-ID validity, exact quote copying, fixture coverage, theme/source pairs against the small reference labels, and a limited unsupported-language keyword scan. It does not establish semantic quality or real-world value. The reference labels are not independently reviewed, and the current six-item fixture is deliberately small. Do not present these smoke-test scores as model performance evidence.
