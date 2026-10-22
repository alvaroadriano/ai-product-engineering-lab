"""Run the Product Evidence Copilot CLI."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from app.analysis import baseline_analysis, model_analysis
from app.schema import FeedbackDataset


def load_dataset(path: Path) -> FeedbackDataset:
    return FeedbackDataset.model_validate_json(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft an evidence-grounded product brief from feedback JSON.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", action="store_true", help="Use the included fictional feedback sample")
    source.add_argument("--input", type=Path, help="Path to a feedback JSON file")
    parser.add_argument("--provider", action="store_true", help="Use Pydantic AI with MODEL from the environment")
    args = parser.parse_args()

    fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "feedback.json"
    dataset = load_dataset(args.input or fixture_path)

    if args.provider:
        model = os.getenv("MODEL", "").strip()
        if not model:
            parser.error("Set MODEL to a supported provider model identifier before using --provider.")
        brief = asyncio.run(model_analysis(dataset, model))
    else:
        brief = baseline_analysis(dataset)

    print(json.dumps(brief.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
