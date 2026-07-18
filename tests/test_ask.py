"""Ask pipeline tests — deliberately lean.

Per our testing philosophy: fakes guard *our* deterministic logic (the
no-hit short-circuit, source mapping, drift handling, citation rules);
answer *quality* is judged on the real system and, in Phase 3, the eval
harness. The answerer's retry loop follows the segmenter pattern already
proven in test_llm_adapters.py and is not re-tested here.
"""

from collections.abc import Sequence
from pathlib import Path

import pytest

from second_brain.app.ask import answer_question
from second_brain.domain.contracts import AnswerDraft
from second_brain.domain.models import Language, Note, NoteType, SourceSpan
from second_brain.domain.retrieval import index_notes
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.answerer import InvalidAnswer, check_citations
from second_brain.infra.llm.fakes import FakeEmbedder
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.trace.jsonl import JsonlTraceSink


class StubAnswerer:
    """Test-local stub: returns a preset draft, records what it was shown."""

    def __init__(self, draft: AnswerDraft) -> None:
        self._draft = draft
        self.calls: list[tuple[str, list[str]]] = []

    def answer(self, question: str, notes: Sequence[Note]) -> AnswerDraft:
        self.calls.append((question, [note.id for note in notes]))
        return self._draft


def make_note(note_id: str, title: str, body: str) -> Note:
    return Note(
        id=note_id,
        title=title,
        language=Language.EN,
        type=NoteType.IDEA,
        source=SourceSpan(session_id="s-001", start_turn=0, end_turn=1),
        body=body,
    )


SQLITE_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAA"
BREAD_ID = "01BRZ3NDEKTSV4RRFFQ69G5FAB"


def seeded(tmp_path: Path) -> tuple[FakeEmbedder, SqliteNoteIndex, MarkdownNoteRepository]:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    repo = MarkdownNoteRepository(tmp_path / "notes")
    notes = [
        make_note(SQLITE_ID, "Tuning the sqlite index", "Pragma tuning for the sqlite index."),
        make_note(BREAD_ID, "Sourdough banana bread", "Starter plus ripe bananas."),
    ]
    for note in notes:
        repo.save(note)
    index_notes(notes, embedder=embedder, index=index)
    return embedder, index, repo


def test_no_hits_short_circuits_without_calling_the_answerer(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)  # empty
    stub = StubAnswerer(AnswerDraft(answer="unused", grounded=False))
    result = answer_question(
        "anything?",
        embedder=embedder,
        index=index,
        repo=MarkdownNoteRepository(tmp_path / "notes"),
        answerer=stub,
        traces=JsonlTraceSink(tmp_path / "traces"),
    )
    assert result.grounded is False
    assert result.sources == []
    assert stub.calls == []  # zero tokens spent on an empty store


def test_sources_map_only_to_cited_notes(tmp_path: Path) -> None:
    embedder, index, repo = seeded(tmp_path)
    stub = StubAnswerer(
        AnswerDraft(answer="Tune the pragmas.", cited_note_ids=[SQLITE_ID], grounded=True)
    )
    result = answer_question(
        "how do I tune my sqlite index",
        embedder=embedder,
        index=index,
        repo=repo,
        answerer=stub,
        traces=JsonlTraceSink(tmp_path / "traces"),
        k=2,
    )
    assert result.grounded is True
    assert [note.id for note in result.sources] == [SQLITE_ID]
    (_, shown_ids) = stub.calls[0]
    assert SQLITE_ID in shown_ids  # the answerer saw the retrieved notes


def test_index_repo_drift_is_skipped(tmp_path: Path) -> None:
    embedder, index, repo = seeded(tmp_path)
    ghost = make_note("01ZRZ3NDEKTSV4RRFFQ69G5FAZ", "Ghost note", "Indexed but not on disk.")
    index_notes([ghost], embedder=embedder, index=index)  # index only, never repo.save
    stub = StubAnswerer(AnswerDraft(answer="ok", cited_note_ids=[SQLITE_ID], grounded=True))
    answer_question(
        "ghost note indexed on disk",
        embedder=embedder,
        index=index,
        repo=repo,
        answerer=stub,
        traces=JsonlTraceSink(tmp_path / "traces"),
        k=3,
    )
    (_, shown_ids) = stub.calls[0]
    assert ghost.id not in shown_ids  # drifted hit filtered before the model


def test_citation_rules() -> None:
    allowed = {SQLITE_ID}
    check_citations(
        AnswerDraft(answer="fine", cited_note_ids=[SQLITE_ID], grounded=True), allowed
    )
    with pytest.raises(InvalidAnswer):
        check_citations(
            AnswerDraft(answer="bad", cited_note_ids=["01FAKE"], grounded=True), allowed
        )
    with pytest.raises(InvalidAnswer):
        check_citations(AnswerDraft(answer="bad", cited_note_ids=[], grounded=True), allowed)
