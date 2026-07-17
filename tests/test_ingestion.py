"""Ingestion policy tests: FakeSegmenter + real Markdown store, fully offline.

These are the first tests that exercise the fakes — and they double as the
executable spec for the watermark semantics.
"""

from pathlib import Path

from second_brain.domain.contracts import NoteDraft
from second_brain.domain.ingestion import ingest_session, ingested_watermark, materialize
from second_brain.domain.models import Language, NoteType, Role, Turn
from second_brain.infra.llm.fakes import FakeSegmenter
from second_brain.infra.store.markdown import MarkdownNoteRepository


def make_turns(n: int, start: int = 0) -> list[Turn]:
    return [
        Turn(
            index=start + i,
            role=Role.USER if (start + i) % 2 == 0 else Role.ASSISTANT,
            content=f"turn {start + i}: substance about the side project",
        )
        for i in range(n)
    ]


def preset_draft(start: int, end: int, title: str) -> NoteDraft:
    return NoteDraft(
        title=title,
        language=Language.EN,
        type=NoteType.IDEA,
        start_turn=start,
        end_turn=end,
        body=f"Body covering turns {start} to {end}.",
    )


def test_first_ingestion_persists_notes_with_provenance(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    segmenter = FakeSegmenter()
    notes = ingest_session(
        session_id="s-001", turns=make_turns(4), repo=repo, segmenter=segmenter
    )
    assert len(notes) == 1
    note = notes[0]
    assert note.source.session_id == "s-001"
    assert (note.source.start_turn, note.source.end_turn) == (0, 3)
    assert len(note.id) == 26  # ULID assigned by the domain
    assert repo.get(note.id) == note


def test_reingesting_same_turns_is_a_noop(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    segmenter = FakeSegmenter()
    turns = make_turns(4)
    first = ingest_session(session_id="s-001", turns=turns, repo=repo, segmenter=segmenter)
    second = ingest_session(session_id="s-001", turns=turns, repo=repo, segmenter=segmenter)
    assert len(first) == 1
    assert second == []
    assert len(segmenter.calls) == 1  # second run never reached the model
    assert len(list(repo.iter_all())) == 1


def test_incremental_ingestion_only_sees_new_turns(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    segmenter = FakeSegmenter()
    ingest_session(session_id="s-001", turns=make_turns(4), repo=repo, segmenter=segmenter)
    grown = make_turns(6)  # turns 0..5: the session continued
    notes = ingest_session(session_id="s-001", turns=grown, repo=repo, segmenter=segmenter)
    window = segmenter.calls[1]
    assert [t.index for t in window] == [4, 5]
    assert (notes[0].source.start_turn, notes[0].source.end_turn) == (4, 5)
    assert ingested_watermark(repo, "s-001") == 5


def test_watermark_is_per_session(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    ingest_session(
        session_id="s-001", turns=make_turns(4), repo=repo, segmenter=FakeSegmenter()
    )
    assert ingested_watermark(repo, "s-001") == 3
    assert ingested_watermark(repo, "s-other") == -1


def test_materialize_assigns_fresh_identity_each_time() -> None:
    draft = preset_draft(0, 1, "Same draft, two notes")
    a = materialize(draft, "s-001")
    b = materialize(draft, "s-001")
    assert a.id != b.id  # the model never controls identity


def test_notes_are_saved_in_end_turn_order(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    drafts = [
        preset_draft(2, 3, "Later span, listed first"),
        preset_draft(0, 1, "Earlier span, listed second"),
    ]
    notes = ingest_session(
        session_id="s-001",
        turns=make_turns(4),
        repo=repo,
        segmenter=FakeSegmenter(drafts=drafts),
    )
    assert [n.source.end_turn for n in notes] == [1, 3]


def test_assistant_only_remainder_skips_the_segmenter(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    segmenter = FakeSegmenter()
    farewell = [Turn(index=0, role=Role.ASSISTANT, content="Bonne nuit !")]
    notes = ingest_session(
        session_id="s-001", turns=farewell, repo=repo, segmenter=segmenter
    )
    assert notes == []
    assert segmenter.calls == []
