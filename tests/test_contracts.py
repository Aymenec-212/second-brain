"""Contract tests: the rules the segmenter's output must obey.

These run offline — no network, no keys — and double as executable
documentation of what a valid NoteDraft looks like.
"""

from typing import Any

import pytest
from pydantic import ValidationError

from second_brain.domain.contracts import NoteDraft, SegmentationResult


def draft_kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "title": "Chose SQLite for the index",
        "language": "en",
        "type": "decision",
        "tags": ["Architecture", "sqlite", "  architecture "],
        "entities": ["SQLite", "SQLite", "  "],
        "start_turn": 0,
        "end_turn": 4,
        "body": "We compared LanceDB, FAISS and sqlite-vec and picked SQLite.",
    }
    base.update(overrides)
    return base


def test_tags_are_lowercased_stripped_and_deduped() -> None:
    draft = NoteDraft(**draft_kwargs())
    assert draft.tags == ["architecture", "sqlite"]


def test_entities_keep_case_but_dedupe_and_drop_blanks() -> None:
    draft = NoteDraft(**draft_kwargs())
    assert draft.entities == ["SQLite"]


def test_span_must_be_ordered() -> None:
    with pytest.raises(ValidationError):
        NoteDraft(**draft_kwargs(start_turn=5, end_turn=2))


def test_title_and_body_must_be_non_empty() -> None:
    with pytest.raises(ValidationError):
        NoteDraft(**draft_kwargs(title="   "))
    with pytest.raises(ValidationError):
        NoteDraft(**draft_kwargs(body=""))


def test_segmentation_result_parses_provider_json() -> None:
    payload = {"notes": [draft_kwargs()]}
    result = SegmentationResult.model_validate(payload)
    assert len(result.notes) == 1
    assert result.notes[0].type == "decision"
    assert result.notes[0].language == "en"
