"""Read-path policy and write-side indexing.

Phase 3 completes the funnel: reciprocal rank fusion of the two legs, the
rerank text policy, and the three-zone gate. Everything in this module is
pure and deterministic — models contribute scores through ports, but every
ranking and thresholding decision is code.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from enum import StrEnum

from pydantic import BaseModel

from second_brain.domain.models import Note, SearchHit
from second_brain.domain.ports import Embedder, Enricher, NoteIndex

_RRF_K = 60  # standard constant; rank-based, so leg scores never mix


def embedding_text(note: Note) -> str:
    """Title + body. The title carries the searchable phrasing a future
    query is likely to share; the body carries the substance."""
    return f"{note.title}\n\n{note.body}"


def rerank_text(note: Note, max_chars: int = 4000) -> str:
    """What the cross-encoder reads: title + body, bounded for latency."""
    return f"{note.title}\n\n{note.body}"[:max_chars]


def content_hash(note: Note) -> str:
    """What the enrichment cache keys on: if title+body are unchanged,
    the cached enrichment is still valid."""
    return hashlib.md5(f"{note.title}\n{note.body}".encode("utf-8")).hexdigest()


def rrf_fuse(*legs: Sequence[SearchHit]) -> list[SearchHit]:
    """Reciprocal rank fusion: score = Σ 1/(K + rank) over the legs a note
    appears in. Rank-based on purpose — dense similarities and BM25 values
    are incommensurable, ranks are not. Deterministic tie-break by id."""
    fused: dict[str, float] = {}
    for leg in legs:
        for rank, hit in enumerate(leg, start=1):
            fused[hit.note_id] = fused.get(hit.note_id, 0.0) + 1.0 / (_RRF_K + rank)
    ordered = sorted(fused.items(), key=lambda item: (-item[1], item[0]))
    return [SearchHit(note_id=note_id, score=score) for note_id, score in ordered]


class ScoredNote(BaseModel):
    """A note with its reranker relevance in [0, 1]."""

    note: Note
    score: float


class GateZone(StrEnum):
    ANSWER = "answer"
    HEDGED = "hedged"
    ABSTAIN = "abstain"


class GateDecision(BaseModel):
    zone: GateZone
    notes: list[ScoredNote]


def gate_candidates(
    scored: Sequence[ScoredNote],
    *,
    tau_high: float,
    tau_low: float,
    max_notes: int,
) -> GateDecision:
    """The three-zone gate, judged on the single best candidate:
    top ≥ τ-high → answer; τ-low ≤ top < τ-high → hedged; below → abstain.
    Only candidates above τ-low (capped at max_notes) pass through — the
    answerer never sees weakly-relevant context."""
    ranked = sorted(scored, key=lambda s: (-s.score, s.note.id))
    if not ranked or ranked[0].score < tau_low:
        return GateDecision(zone=GateZone.ABSTAIN, notes=[])
    kept = [s for s in ranked[:max_notes] if s.score >= tau_low]
    zone = GateZone.ANSWER if ranked[0].score >= tau_high else GateZone.HEDGED
    return GateDecision(zone=zone, notes=kept)


def index_notes(
    notes: Sequence[Note],
    *,
    enricher: Enricher,
    embedder: Embedder,
    index: NoteIndex,
) -> None:
    """Enrich (cache-first), embed (one batch), upsert."""
    if not notes:
        return
    enrichments = [
        index.cached_enrichment(note) or enricher.enrich(note) for note in notes
    ]
    vectors = embedder.embed([embedding_text(note) for note in notes])
    for note, vector, enrichment in zip(notes, vectors, enrichments, strict=True):
        index.upsert(note, vector, enrichment)
