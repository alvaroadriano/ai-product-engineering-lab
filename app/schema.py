"""Typed input and output contracts for the prototype."""

from pydantic import BaseModel, Field


class FeedbackItem(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    segment: str = "unspecified"


class FeedbackDataset(BaseModel):
    project: str
    feedback: list[FeedbackItem] = Field(min_length=1)


class Theme(BaseModel):
    name: str
    summary: str
    source_ids: list[str]
    representative_quotes: list[str]
    confidence: str = Field(description="Low, medium, or high; qualitative only")


class EvidenceBrief(BaseModel):
    project: str
    themes: list[Theme]
    claims_to_validate: list[str]
    research_questions: list[str]
    limitations: list[str]
