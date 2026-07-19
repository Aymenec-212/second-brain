"""Ports: the seam.

Domain and app depend on these Protocols only; infrastructure implements
them. A model can inform control flow solely by returning a validated
contract through one of these interfaces — this file is the complete list
of places where that can happen.

We used Protocols (structural typing) instead of ABCs
since it can enable no import no inheritance,
a criteria to respect DDD
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol

from second_brain.domain.contracts import NoteDraft, AnswerDraft, NoteEnrichment, RouterDecision, ActivityQueryPlan
from second_brain.domain.models import Note, TraceEvent, Turn, SearchHit, WebAnswer


class IntentRouter(Protocol):
    """Cognitive task: classify a turn and fill its slots."""

    def route(self, text: str, history: Sequence[Turn]) -> RouterDecision: ...


# NoteIndex gains:
    def activity_search(self, plan: ActivityQueryPlan) -> list[str]: ...


class ChatResponder(Protocol):
    """Cognitive task: continue the conversation. The adapter owns the prompt."""

    def reply(self, history: Sequence[Turn]) -> str: ...


class Segmenter(Protocol):
    """Cognitive task: split a transcript span into atomic note drafts."""

    def segment(self, turns: Sequence[Turn]) -> list[NoteDraft]: ...


class NoteRepository(Protocol):
    """Canonical Markdown store of notes."""

    def save(self, note: Note) -> None: ...

    def get(self, note_id: str) -> Note | None: ...

    def iter_all(self) -> Iterable[Note]: ...


class TranscriptStore(Protocol):
    """Append-only session archive; crash-safe by construction."""

    def append(self, session_id: str, turn: Turn) -> None: ...

    def read(self, session_id: str) -> list[Turn]: ...


class TraceSink(Protocol):
    """Receives one event per observable step of a turn."""

    def emit(self, event: TraceEvent) -> None: ...

class Embedder(Protocol):
    """Text → vector; queries and documents share one space."""

    @property
    def dimensions(self) -> int: ...

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class NoteIndex(Protocol):
    """Derived, rebuildable search index over the canonical store."""

    def upsert(self, note: Note, embedding: Sequence[float], enrichment: NoteEnrichment) -> None: ...

    def dense_search(self, query_embedding: Sequence[float], k: int) -> list[SearchHit]: ...

    def lexical_search(self, query: str, k: int) -> list[SearchHit]: ...

    def cached_enrichment(self, note: Note) -> NoteEnrichment | None: ...

    def count(self) -> int: ...

    def clear(self) -> None: ...

class Answerer(Protocol):
    """Cognitive task: answer a question from retrieved notes only."""

    def answer(self, question: str, notes: Sequence[Note]) -> AnswerDraft: ...

class Enricher(Protocol):
    """Cognitive task: produce retrieval enrichment for one note."""

    def enrich(self, note: Note) -> NoteEnrichment: ...

class QueryPivoter(Protocol):
    """Cognitive task: English pivot of a query for lexical search."""

    def pivot(self, query: str) -> str: ...


class Reranker(Protocol):
    """Relevance scores in [0, 1], aligned with the input order.
    Sorting and thresholding stay in the domain."""

    def rerank(self, query: str, notes: Sequence[Note]) -> list[float]: ...

class WebSearcher(Protocol):
    """Answer from the live web; presentation must mark it as such."""

    def search(self, question: str) -> WebAnswer: ...       