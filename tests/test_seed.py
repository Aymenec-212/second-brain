"""Seed tests: spec invariants, synthesis contract rules, simulated time,
and offline resumability with a counting stub synthesizer.
"""

from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError
from ulid import ULID

from second_brain.domain.ingestion import ingest_session
from second_brain.domain.models import Language, Role, Turn
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.fakes import FakeEmbedder, FakeSegmenter, FakeEnricher
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.seed.generate import SyntheticSession, run_seed
from second_brain.seed.spec import SessionBrief, all_briefs, session_id_for

SIM_DATE = datetime(2026, 3, 14, 20, 30, tzinfo=UTC)


def test_briefs_are_plentiful_ordered_and_bilingual() -> None:
    briefs = all_briefs()
    assert len(briefs) >= 55
    dates = [b.date for b in briefs]
    assert dates == sorted(dates)
    fr_share = sum(1 for b in briefs if b.language is Language.FR) / len(briefs)
    assert 0.25 <= fr_share <= 0.55


def test_session_ids_are_deterministic_and_distinct() -> None:
    briefs = all_briefs()
    ids = [session_id_for(b) for b in briefs]
    assert ids == [session_id_for(b) for b in all_briefs()]  # stable across calls
    assert len(set(ids)) == len(ids)


def test_synthetic_session_contract_rules() -> None:
    def turn(role: str, text: str) -> dict[str, str]:
        return {"role": role, "content": text}

    valid = [turn("user", "a"), turn("assistant", "b")] * 3
    SyntheticSession.model_validate({"turns": valid})
    with pytest.raises(ValidationError):  # assistant-first
        SyntheticSession.model_validate({"turns": [turn("assistant", "a")] + valid[:5]})
    with pytest.raises(ValidationError):  # broken alternation
        broken = valid[:3] + [turn("assistant", "x")] + valid[3:5]
        SyntheticSession.model_validate({"turns": broken})
    with pytest.raises(ValidationError):  # too short
        SyntheticSession.model_validate({"turns": valid[:4]})


def test_simulated_time_reaches_note_and_ulid(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path / "notes")
    turns = [
        Turn(index=0, role=Role.USER, content="budget appartement 420 000 EUR", ts=SIM_DATE),
        Turn(index=1, role=Role.ASSISTANT, content="ok", ts=SIM_DATE),
    ]
    [note] = ingest_session(
        session_id="seed-test",
        turns=turns,
        repo=repo,
        segmenter=FakeSegmenter(),
        created_at=SIM_DATE,
    )
    assert note.created_at == SIM_DATE
    assert ULID.from_str(note.id).datetime.date() == SIM_DATE.date()


def test_run_seed_is_resumable_without_regenerating(tmp_path: Path) -> None:
    briefs = all_briefs()[:3]
    calls: list[str] = []

    def stub_synthesize(brief: SessionBrief) -> list[Turn]:
        calls.append(brief.brief)
        return [
            Turn(index=0, role=Role.USER, content=f"thinking: {brief.brief}", ts=brief.date),
            Turn(index=1, role=Role.ASSISTANT, content="noted", ts=brief.date),
        ]

    embedder = FakeEmbedder()
    deps = {
        "transcripts": JsonlTranscriptStore(tmp_path / "transcripts"),
        "repo": MarkdownNoteRepository(tmp_path / "notes"),
        "segmenter": FakeSegmenter(),
        "embedder": embedder,
        "index": SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions),
        "enricher": FakeEnricher(),
    }
    first = list(run_seed(briefs, synthesize=stub_synthesize, **deps))
    assert len(calls) == 3
    assert all("generated" in line for line in first)
    notes_after_first = deps["index"].count()

    second = list(run_seed(briefs, synthesize=stub_synthesize, **deps))
    assert len(calls) == 3  # nothing regenerated
    assert all("resumed, 0 notes" in line for line in second)
    assert deps["index"].count() == notes_after_first
