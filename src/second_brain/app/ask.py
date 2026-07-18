"""One-shot question answering: the read path, v0.

Dense-only retrieval; Phase 3 replaces the middle of this pipeline with
the full funnel (lexical leg, fusion, rerank, three-zone gate).

Two deterministic rules live here, not in any prompt:
- No hits → ungrounded result without calling the answerer at all.
- Cited sources are re-read from the canonical repo, never from index rows.
"""

from __future__ import annotations

from second_brain.domain.models import Answer, Note, TraceEvent, new_id
from second_brain.domain.ports import (
    Answerer,
    Embedder,
    NoteIndex,
    NoteRepository,
    TraceSink,
)

_NOT_COVERED = (
    "Nothing in your notes covers this yet. / "
    "Rien dans vos notes ne couvre ce sujet pour l'instant."
)


def answer_question(
    question: str,
    *,
    embedder: Embedder,
    index: NoteIndex,
    repo: NoteRepository,
    answerer: Answerer,
    traces: TraceSink,
    k: int = 5,
) -> Answer:
    ask_id = f"ask-{new_id()}"
    traces.emit(
        TraceEvent(session_id=ask_id, kind="ask_received", payload={"chars": len(question)})
    )
    [query_vector] = embedder.embed([question])
    hits = index.dense_search(query_vector, k)
    notes: list[Note] = []
    for hit in hits:
        note = repo.get(hit.note_id)
        if note is not None:  # index/repo drift is skipped; `sb reindex` heals it
            notes.append(note)
    if not notes:
        traces.emit(
            TraceEvent(session_id=ask_id, kind="ask_answered", payload={"hits": 0})
        )
        return Answer(text=_NOT_COVERED, sources=[], grounded=False)
    draft = answerer.answer(question, notes)
    sources = [note for note in notes if note.id in draft.cited_note_ids]
    traces.emit(
        TraceEvent(
            session_id=ask_id,
            kind="ask_answered",
            payload={
                "hits": [(hit.note_id, round(hit.score, 4)) for hit in hits],
                "cited": draft.cited_note_ids,
                "grounded": draft.grounded,
            },
        )
    )
    return Answer(text=draft.answer, sources=sources, grounded=draft.grounded)
