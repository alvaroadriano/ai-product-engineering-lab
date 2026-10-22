"""Offline baseline and optional LLM-backed synthesis."""

from __future__ import annotations

from collections import defaultdict

from app.schema import EvidenceBrief, FeedbackDataset, Theme


KEYWORD_GROUPS = {
    "Inventory visibility": {"stock", "inventory", "available", "availability"},
    "Checkout reliability": {"payment", "error", "failed", "failure", "charged", "charge"},
    "Order status clarity": {"order", "status", "tracking", "delivery", "shipped"},
}


def baseline_analysis(dataset: FeedbackDataset) -> EvidenceBrief:
    """Group synthetic feedback using transparent keyword rules.

    This baseline is intentionally simple. It makes a useful comparison point,
    not a claim that keyword matching understands customer intent.
    """
    grouped: dict[str, list] = defaultdict(list)
    unmatched = []
    for item in dataset.feedback:
        text = item.text.lower()
        matched = [
            name
            for name, keywords in KEYWORD_GROUPS.items()
            if any(keyword in text for keyword in keywords)
        ]
        if not matched:
            unmatched.append(item.id)
        for name in matched:
            grouped[name].append(item)

    themes = [
        Theme(
            name=name,
            summary=f"{len(items)} feedback item(s) matched the baseline keywords for {name.lower()}.",
            source_ids=[item.id for item in items],
            representative_quotes=[item.text for item in items[:2]],
            confidence="low",
        )
        for name, items in grouped.items()
    ]
    limitations = [
        "The offline baseline uses keyword matching and may miss synonyms, intent, or context.",
        "The sample is synthetic and too small to represent a real customer population.",
        "Qualitative confidence labels are not statistical confidence intervals.",
    ]
    if unmatched:
        limitations.append(f"Items not grouped by the keyword baseline: {', '.join(unmatched)}.")

    return EvidenceBrief(
        project=dataset.project,
        themes=themes,
        claims_to_validate=[
            "Whether the identified themes reflect distinct underlying user needs.",
            "How common each need is in the broader customer population.",
        ],
        research_questions=[
            "Which user segment and task were involved in each reported issue?",
            "What outcome did the user expect, and what happened instead?",
        ],
        limitations=limitations,
    )


async def model_analysis(dataset: FeedbackDataset, model: str) -> EvidenceBrief:
    """Run a structured synthesis through Pydantic AI.

    Provider authentication is read from the corresponding environment variable
    by Pydantic AI. The caller must supply a current model identifier.
    """
    from pydantic_ai import Agent

    agent = Agent(
        model,
        output_type=EvidenceBrief,
        system_prompt=(
            "You are assisting a product manager with a small feedback sample. "
            "Do not infer prevalence, causation, revenue, or impact from this sample. "
            "Every theme must cite source IDs from the input and include verbatim "
            "representative quotes copied exactly from those sources. If evidence is "
            "weak or ambiguous, say so. Return a concise draft for human review."
        ),
    )
    result = await agent.run(dataset.model_dump_json(indent=2))
    brief: EvidenceBrief = result.output
    valid_ids = {item.id for item in dataset.feedback}
    for theme in brief.themes:
        theme.source_ids = [source_id for source_id in theme.source_ids if source_id in valid_ids]
        allowed_quotes = {item.text for item in dataset.feedback if item.id in theme.source_ids}
        theme.representative_quotes = [quote for quote in theme.representative_quotes if quote in allowed_quotes]
    brief.limitations = list(dict.fromkeys(brief.limitations + ["AI-generated draft; review every theme and claim before use."]))
    return brief
