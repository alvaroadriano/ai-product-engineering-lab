"""Run the small synthetic evaluation and check traceability mechanics."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.analysis import baseline_analysis, model_analysis  # noqa: E402
from app.schema import EvidenceBrief, FeedbackDataset  # noqa: E402


def evaluate(brief: EvidenceBrief, dataset: FeedbackDataset, reference: dict) -> dict:
    valid_ids = {item.id for item in dataset.feedback}
    quote_sources = {item.text: item.id for item in dataset.feedback}
    predicted_pairs: set[tuple[str, str]] = set()
    citation_count = 0
    valid_citations = 0
    quote_count = 0
    exact_quotes = 0
    invalid_quotes = 0
    cited_ids: set[str] = set()
    for theme in brief.themes:
        for source_id in theme.source_ids:
            citation_count += 1
            if source_id in valid_ids:
                valid_citations += 1
                cited_ids.add(source_id)
                predicted_pairs.add((theme.name, source_id))
        for quote in theme.representative_quotes:
            quote_count += 1
            source_id = quote_sources.get(quote)
            if source_id is not None:
                exact_quotes += 1
                if source_id not in theme.source_ids:
                    invalid_quotes += 1

    expected_pairs = {
        (theme, source_id)
        for theme, source_ids in reference["themes"].items()
        for source_id in source_ids
    }
    true_positive = len(expected_pairs & predicted_pairs)
    precision = true_positive / len(predicted_pairs) if predicted_pairs else 0.0
    recall = true_positive / len(expected_pairs) if expected_pairs else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0

    risky_language = re.compile(
        r"\b(most users|many users|majority|widespread|usually|often|frequently|"
        r"increased revenue|reduced revenue|conversion lift|caused|led to)\b",
        re.IGNORECASE,
    )
    text_fields = [theme.summary for theme in brief.themes] + brief.claims_to_validate
    flagged_claims = [text for text in text_fields if risky_language.search(text)]

    return {
        "dataset_version": reference["dataset_version"],
        "feedback_items": len(dataset.feedback),
        "themes": len(brief.themes),
        "citation_validity": valid_citations / citation_count if citation_count else 1.0,
        "exact_quote_rate": exact_quotes / quote_count if quote_count else 1.0,
        "quote_source_mismatch_count": invalid_quotes,
        "feedback_coverage": len(cited_ids) / len(valid_ids) if valid_ids else 0.0,
        "reference_pair_precision": precision,
        "reference_pair_recall": recall,
        "reference_pair_f1": f1,
        "unsupported_claims_flagged_by_heuristic": flagged_claims,
        "limitations": [
            "One deterministic run on six fictional items; this is a smoke test, not a model benchmark.",
            "Reference labels were written by the project author and were not independently reviewed.",
            "The unsupported-claim scan is a keyword heuristic and cannot establish factuality.",
            "No human usefulness, review-time, latency, or cost scores were collected.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", action="store_true", help="Evaluate the configured model once")
    parser.add_argument("--output", type=Path, help="Write the JSON report to this path")
    args = parser.parse_args()

    dataset = FeedbackDataset.model_validate_json((ROOT / "fixtures/feedback.json").read_text(encoding="utf-8"))
    reference = json.loads((ROOT / "evals/reference.json").read_text(encoding="utf-8"))
    if args.provider:
        model = os.getenv("MODEL", "").strip()
        if not model:
            parser.error("Set MODEL and the matching provider API key before using --provider.")
        brief = asyncio.run(model_analysis(dataset, model))
        system = model
    else:
        brief = baseline_analysis(dataset)
        system = "offline-keyword-baseline"

    report = {"run_date": date.today().isoformat(), "system": system, **evaluate(brief, dataset, reference)}
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
