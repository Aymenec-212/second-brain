"""Contracts for model outputs.

Every LLM response that crosses into control flow is validated into one of
these types. Invalid output triggers a bounded retry in the adapter, never
a crash, never silent acceptance.

Field descriptions are serialized into the JSON schema sent to the provider
(OpenAI structured outputs), so validation rules and prompt guidance share a
single source of truth.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator

from second_brain.domain.models import Language, NonEmptyStr, NoteType


class NoteDraft(BaseModel):
    """One prospective note, proposed by the segmenter over a transcript span."""

    title: NonEmptyStr = Field(
        description="Specific and searchable, written in the note's language",
    )
    language: Language
    type: NoteType
    tags: list[str] = Field(
        default_factory=list,
        description="Up to 8 lowercase topical tags",
    )
    entities: list[str] = Field(
        default_factory=list,
        description="Canonical names of people, projects, tools mentioned",
    )
    start_turn: int = Field(
        ge=0, description="First transcript turn this note covers (absolute index)"
    )
    end_turn: int = Field(
        ge=0, description="Last transcript turn this note covers (absolute index)"
    )
    body: NonEmptyStr = Field(
        description=(
            "Distilled but detailed prose, roughly 150-500 words, written in "
            "`language`. Preserve decisions, reasoning, open questions, numbers, "
            "and names — this text is all that survives the conversation."
        ),
    )

    @field_validator("tags")
    @classmethod
    def _normalize_tags(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for tag in (t.strip().lower() for t in v):
            if tag and tag not in out:
                out.append(tag)
        return out

    @field_validator("entities")
    @classmethod
    def _dedupe_entities(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for ent in (e.strip() for e in v):
            if ent and ent not in out:
                out.append(ent)
        return out

    @model_validator(mode="after")
    def _span_ordered(self) -> NoteDraft:
        if self.end_turn < self.start_turn:
            raise ValueError("end_turn must be >= start_turn")
        return self


class SegmentationResult(BaseModel):
    """Wrapper object to match the provider's constraints.
       OpenAI's structured outputs require a root object"""

    notes: list[NoteDraft] = Field(default_factory=list)

class AnswerDraft(BaseModel):
    """The answerer's proposal: an answer grounded in the provided notes."""

    answer: NonEmptyStr = Field(
        description="Answer in the language of the question, drawn from the notes only"
    )
    cited_note_ids: list[str] = Field(
        default_factory=list,
        description="Ids of the notes the answer draws on; empty when not grounded",
    )
    grounded: bool = Field(
        description="False when the provided notes do not contain the answer"
    )    