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

from second_brain.domain.contracts import NoteDraft
from second_brain.domain.models import Note, TraceEvent, Turn


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