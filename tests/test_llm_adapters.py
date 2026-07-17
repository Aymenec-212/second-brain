"""Adapter logic tests — no network.

The OpenAI client is stubbed; everything tested here is ours: transcript
rendering, span validation, and the corrective retry loop.
"""

from types import SimpleNamespace
from typing import Any, cast

import pytest
from openai import OpenAI

from second_brain.domain.contracts import NoteDraft, SegmentationResult
from second_brain.domain.models import Role, Turn
from second_brain.infra.llm.segmenter import (
    InvalidSegmentation,
    OpenAISegmenter,
    SegmentationFailure,
    check_spans,
    render_transcript,
)


def turns() -> list[Turn]:
    return [
        Turn(index=0, role=Role.USER, content="Je pense à mon second cerveau"),
        Turn(index=1, role=Role.ASSISTANT, content="Quel angle ?"),
        Turn(index=2, role=Role.USER, content="L'architecture de récupération"),
    ]


def draft(end_turn: int = 2) -> NoteDraft:
    return NoteDraft(
        title="Architecture de récupération du second cerveau",
        language="fr",
        type="idea",
        start_turn=0,
        end_turn=end_turn,
        body="Réflexion sur l'architecture de récupération du second cerveau.",
    )


def completion_with(parsed: SegmentationResult | None) -> Any:
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(parsed=parsed))])


class StubCompletions:
    def __init__(self, results: list[Any]) -> None:
        self._results = results
        self.requests: list[dict[str, Any]] = []

    def parse(self, **kwargs: Any) -> Any:
        self.requests.append(kwargs)
        result = self._results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


def stub_client(results: list[Any]) -> tuple[OpenAI, StubCompletions]:
    stub = StubCompletions(results)
    client = SimpleNamespace(chat=SimpleNamespace(completions=stub))
    return cast(OpenAI, client), stub


def test_render_transcript_shows_absolute_indices() -> None:
    text = render_transcript(turns())
    assert "[0] user: Je pense à mon second cerveau" in text
    assert "[2] user: L'architecture de récupération" in text


def test_check_spans_rejects_out_of_range() -> None:
    with pytest.raises(InvalidSegmentation):
        check_spans([draft(end_turn=99)], max_index=2)


def test_valid_segmentation_returns_first_try() -> None:
    client, stub = stub_client([completion_with(SegmentationResult(notes=[draft()]))])
    notes = OpenAISegmenter(client, model="test-model").segment(turns())
    assert len(notes) == 1
    assert len(stub.requests) == 1


def test_out_of_range_span_triggers_corrective_retry() -> None:
    bad = completion_with(SegmentationResult(notes=[draft(end_turn=99)]))
    good = completion_with(SegmentationResult(notes=[draft()]))
    client, stub = stub_client([bad, good])
    notes = OpenAISegmenter(client, model="test-model").segment(turns())
    assert notes[0].end_turn == 2
    assert len(stub.requests) == 2
    correction = stub.requests[1]["messages"][-1]["content"]
    assert "invalid" in correction


def test_attempt_budget_exhaustion_raises_typed_failure() -> None:
    bads = [
        completion_with(SegmentationResult(notes=[draft(end_turn=99)])) for _ in range(3)
    ]
    client, _ = stub_client(bads)
    with pytest.raises(SegmentationFailure):
        OpenAISegmenter(client, model="test-model").segment(turns())


def test_empty_transcript_yields_no_notes_and_no_call() -> None:
    client, stub = stub_client([])
    assert OpenAISegmenter(client, model="test-model").segment([]) == []
    assert stub.requests == []
