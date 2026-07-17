"""Index tests: SqliteNoteIndex + FakeEmbedder, fully offline.

The FakeEmbedder gives deterministic geometry (shared tokens → nearby
vectors), so ranking assertions are stable across runs and machines.
"""

from pathlib import Path

import pytest

from second_brain.domain.models import Language, Note, NoteType, SourceSpan
from second_brain.domain.retrieval import embedding_text
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.fakes import FakeEmbedder


def make_note(note_id: str, title: str, body: str) -> Note:
    return Note(
        id=note_id,
        title=title,
        language=Language.EN,
        type=NoteType.IDEA,
        source=SourceSpan(session_id="s-001", start_turn=0, end_turn=1),
        body=body,
    )


NOTE_SQLITE = make_note(
    "01ARZ3NDEKTSV4RRFFQ69G5FAA",
    "Tuning the sqlite index",
    "Notes about sqlite index performance and pragma tuning.",
)
NOTE_BREAD = make_note(
    "01BRZ3NDEKTSV4RRFFQ69G5FAB",
    "Sourdough banana bread",
    "A recipe experiment with sourdough starter and ripe bananas.",
)
NOTE_EVAL = make_note(
    "01CRZ3NDEKTSV4RRFFQ69G5FAC",
    "Retrieval evaluation metrics",
    "Recall and MRR for judging retrieval quality on a gold set.",
)


def build_index(tmp_path: Path, embedder: FakeEmbedder) -> SqliteNoteIndex:
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    notes = [NOTE_SQLITE, NOTE_BREAD, NOTE_EVAL]
    vectors = embedder.embed([embedding_text(n) for n in notes])
    for note, vector in zip(notes, vectors, strict=True):
        index.upsert(note, vector)
    return index


def test_dense_search_ranks_by_shared_content(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = build_index(tmp_path, embedder)
    [query] = embedder.embed(["how do I tune my sqlite index"])
    hits = index.dense_search(query, k=3)
    assert hits[0].note_id == NOTE_SQLITE.id
    scores = [hit.score for hit in hits]
    assert scores == sorted(scores, reverse=True)


def test_upsert_replaces_instead_of_duplicating(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = build_index(tmp_path, embedder)
    moved = NOTE_SQLITE.model_copy(
        update={"body": "Now this note is about sourdough starter and bananas."}
    )
    [vector] = embedder.embed([embedding_text(moved)])
    index.upsert(moved, vector)
    assert index.count() == 3  # replaced, not added
    [query] = embedder.embed(["sourdough starter bananas"])
    top_ids = {hit.note_id for hit in index.dense_search(query, k=2)}
    assert moved.id in top_ids


def test_index_persists_across_reopen(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = build_index(tmp_path, embedder)
    index.close()
    reopened = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    assert reopened.count() == 3


def test_dimension_stamp_rejects_config_drift(tmp_path: Path) -> None:
    SqliteNoteIndex(tmp_path / "index.db", dimensions=8).close()
    with pytest.raises(RuntimeError, match="reindex"):
        SqliteNoteIndex(tmp_path / "index.db", dimensions=16)


def test_upsert_rejects_wrong_dimension_vector(tmp_path: Path) -> None:
    index = SqliteNoteIndex(tmp_path / "index.db", dimensions=8)
    with pytest.raises(ValueError):
        index.upsert(NOTE_SQLITE, [0.5] * 16)


def test_search_on_empty_index_returns_nothing(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    [query] = embedder.embed(["anything at all"])
    assert index.dense_search(query, k=5) == []


def test_k_larger_than_corpus_returns_everything(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = build_index(tmp_path, embedder)
    [query] = embedder.embed(["sqlite"])
    assert len(index.dense_search(query, k=50)) == 3


def test_clear_empties_both_tables(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = build_index(tmp_path, embedder)
    index.clear()
    assert index.count() == 0
    [query] = embedder.embed(["sqlite"])
    assert index.dense_search(query, k=3) == []


def test_fake_embedder_is_deterministic_across_instances() -> None:
    first = FakeEmbedder().embed(["même texte, même vecteur"])
    second = FakeEmbedder().embed(["même texte, même vecteur"])
    assert first == second
