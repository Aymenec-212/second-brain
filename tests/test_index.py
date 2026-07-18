"""Index tests: dense + lexical legs and the enrichment cache, fully offline.

The FakeEmbedder gives deterministic geometry; FakeEnricher presets plant
known English shadows for cross-lingual lexical assertions.
"""

from pathlib import Path

import pytest

from second_brain.domain.contracts import NoteEnrichment
from second_brain.domain.models import Language, Note, NoteType, SourceSpan
from second_brain.domain.retrieval import embedding_text, index_notes
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.fakes import FakeEmbedder, FakeEnricher


def make_note(
    note_id: str, title: str, body: str, language: Language = Language.EN
) -> Note:
    return Note(
        id=note_id,
        title=title,
        language=language,
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
NOTE_APPART = make_note(
    "01CRZ3NDEKTSV4RRFFQ69G5FAC",
    "Budget pour héberger le projet appartement",
    "Budget maximal de 420 000 EUR avec un apport de 60 000 EUR.",
    language=Language.FR,
)

APPART_ENRICHMENT = NoteEnrichment(
    gist_en="Apartment budget: 420000 EUR maximum with a 60000 EUR down payment.",
    questions=["What is my apartment budget?", "How much is my down payment?"],
)


def default_enrichment() -> NoteEnrichment:
    return NoteEnrichment(gist_en="A gist.", questions=["A question?"])


def seeded_index(
    tmp_path: Path,
) -> tuple[SqliteNoteIndex, FakeEmbedder, FakeEnricher]:
    embedder = FakeEmbedder()
    enricher = FakeEnricher(presets={NOTE_APPART.id: APPART_ENRICHMENT})
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    index_notes(
        [NOTE_SQLITE, NOTE_BREAD, NOTE_APPART],
        enricher=enricher,
        embedder=embedder,
        index=index,
    )
    return index, embedder, enricher


def test_dense_search_ranks_by_shared_content(tmp_path: Path) -> None:
    index, embedder, _ = seeded_index(tmp_path)
    [query] = embedder.embed(["how do I tune my sqlite index"])
    hits = index.dense_search(query, k=3)
    assert hits[0].note_id == NOTE_SQLITE.id
    scores = [hit.score for hit in hits]
    assert scores == sorted(scores, reverse=True)


def test_lexical_search_matches_exact_terms(tmp_path: Path) -> None:
    index, _, _ = seeded_index(tmp_path)
    hits = index.lexical_search("sourdough bananas", k=3)
    assert hits[0].note_id == NOTE_BREAD.id


def test_lexical_search_folds_diacritics(tmp_path: Path) -> None:
    index, _, _ = seeded_index(tmp_path)
    hits = index.lexical_search("heberger", k=3)  # note says "héberger"
    assert [h.note_id for h in hits] == [NOTE_APPART.id]


def test_lexical_search_crosses_languages_via_enrichment(tmp_path: Path) -> None:
    index, _, _ = seeded_index(tmp_path)
    hits = index.lexical_search("apartment down payment", k=3)
    assert hits[0].note_id == NOTE_APPART.id  # FR note found by EN query


def test_lexical_search_survives_operator_syntax(tmp_path: Path) -> None:
    index, _, _ = seeded_index(tmp_path)
    hits = index.lexical_search('sqlite AND "pragma" (tuning) -bananas', k=3)
    assert any(h.note_id == NOTE_SQLITE.id for h in hits)


def test_enrichment_cache_avoids_repeat_model_calls(tmp_path: Path) -> None:
    index, embedder, enricher = seeded_index(tmp_path)
    assert len(enricher.calls) == 3
    index_notes(
        [NOTE_SQLITE, NOTE_BREAD, NOTE_APPART],
        enricher=enricher,
        embedder=embedder,
        index=index,
    )
    assert len(enricher.calls) == 3  # every enrichment served from cache


def test_enrichment_cache_survives_clear(tmp_path: Path) -> None:
    index, embedder, enricher = seeded_index(tmp_path)
    index.clear()
    assert index.count() == 0
    assert index.lexical_search("sourdough", k=3) == []
    index_notes(
        [NOTE_BREAD], enricher=enricher, embedder=embedder, index=index
    )
    assert len(enricher.calls) == 3  # rebuild after clear: still no new calls


def test_changed_content_invalidates_the_cache(tmp_path: Path) -> None:
    index, embedder, enricher = seeded_index(tmp_path)
    edited = NOTE_BREAD.model_copy(update={"body": "Now with walnuts and honey."})
    index_notes([edited], enricher=enricher, embedder=embedder, index=index)
    assert len(enricher.calls) == 4  # hash mismatch → fresh enrichment


def test_dimension_stamp_rejects_config_drift(tmp_path: Path) -> None:
    SqliteNoteIndex(tmp_path / "index.db", dimensions=8).close()
    with pytest.raises(RuntimeError, match="reindex"):
        SqliteNoteIndex(tmp_path / "index.db", dimensions=16)


def test_upsert_rejects_wrong_dimension_vector(tmp_path: Path) -> None:
    index = SqliteNoteIndex(tmp_path / "index.db", dimensions=8)
    with pytest.raises(ValueError):
        index.upsert(NOTE_SQLITE, [0.5] * 16, default_enrichment())


def test_search_on_empty_index_returns_nothing(tmp_path: Path) -> None:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    [query] = embedder.embed(["anything at all"])
    assert index.dense_search(query, k=5) == []
    assert index.lexical_search("anything", k=5) == []


def test_upsert_replaces_across_all_tables(tmp_path: Path) -> None:
    index, embedder, enricher = seeded_index(tmp_path)
    moved = NOTE_SQLITE.model_copy(
        update={"body": "Now this note is about sourdough starter and bananas."}
    )
    index_notes([moved], enricher=enricher, embedder=embedder, index=index)
    assert index.count() == 3
    lex = index.lexical_search("pragma", k=3)
    assert all(h.note_id != NOTE_SQLITE.id for h in lex)  # old FTS row gone
