"""One-shot question answering: the full read-path funnel.

original query → dense leg          ┐
original + EN pivot → lexical leg   ┴→ RRF → cross-encoder → gate → answerer

Deterministic rules living here, not in any prompt:
- No candidates, or top rerank score below τ-low → abstain, zero tokens.
- Only notes above τ-low (max answer_top) ever reach the answerer.
- A confident retrieval with an ungrounded answer downgrades to abstention:
  retrieval confidence and content confirmation veto independently.
"""

from __future__ import annotations

from second_brain.domain.models import (
    Abstention,
    Answer,
    AskResult,
    HedgedAnswer,
    Note,
    TraceEvent,
    new_id,
)
from second_brain.domain.ports import (
    Answerer,
    Embedder,
    NoteIndex,
    NoteRepository,
    QueryPivoter,
    Reranker,
    TraceSink,
)
from second_brain.domain.retrieval import GateZone, ScoredNote, gate_candidates, rrf_fuse

_NOT_COVERED = (
    "Nothing in your notes covers this. / "
    "Rien dans vos notes ne couvre ce sujet."
)


def answer_question(
    question: str,
    *,
    embedder: Embedder,
    index: NoteIndex,
    repo: NoteRepository,
    answerer: Answerer,
    reranker: Reranker,
    pivoter: QueryPivoter,
    traces: TraceSink,
    rerank_top: int = 20,
    answer_top: int = 5,
    tau_high: float = 0.6,
    tau_low: float = 0.2,
) -> AskResult:
    ask_id = f"ask-{new_id()}"
    traces.emit(
        TraceEvent(session_id=ask_id, kind="ask_received", payload={"chars": len(question)})
    )

    pivot = pivoter.pivot(question)
    [query_vector] = embedder.embed([question])
    dense = index.dense_search(query_vector, rerank_top)
    lexical = index.lexical_search(f"{question} {pivot}", rerank_top)
    fused = rrf_fuse(dense, lexical)[:rerank_top]

    notes: list[Note] = []
    for hit in fused:
        note = repo.get(hit.note_id)
        if note is not None:  # index/repo drift is skipped; `sb reindex` heals it
            notes.append(note)

    if not notes:
        _emit_decision(traces, ask_id, pivot, dense, lexical, [], "abstain")
        return Abstention(message=_NOT_COVERED)

    scores = reranker.rerank(question, notes)
    scored = [
        ScoredNote(note=note, score=score)
        for note, score in zip(notes, scores, strict=True)
    ]
    decision = gate_candidates(
        scored, tau_high=tau_high, tau_low=tau_low, max_notes=answer_top
    )
    _emit_decision(traces, ask_id, pivot, dense, lexical, scored, decision.zone.value)

    if decision.zone is GateZone.ABSTAIN:
        return Abstention(message=_NOT_COVERED)

    kept = [s.note for s in decision.notes]
    draft = answerer.answer(question, kept)
    if not draft.grounded:
        return Abstention(message=draft.answer)
    sources = [note for note in kept if note.id in draft.cited_note_ids]
    if decision.zone is GateZone.HEDGED:
        return HedgedAnswer(
            text=draft.answer, sources=sources, top_score=decision.notes[0].score
        )
    return Answer(text=draft.answer, sources=sources)


def _emit_decision(
    traces: TraceSink,
    ask_id: str,
    pivot: str,
    dense: list,
    lexical: list,
    scored: list[ScoredNote],
    zone: str,
) -> None:
    traces.emit(
        TraceEvent(
            session_id=ask_id,
            kind="ask_decided",
            payload={
                "pivot": pivot,
                "dense": [(h.note_id, round(h.score, 4)) for h in dense],
                "lexical": [(h.note_id, round(h.score, 4)) for h in lexical],
                "reranked": [(s.note.id, round(s.score, 4)) for s in scored],
                "zone": zone,
            },
        )
    )
