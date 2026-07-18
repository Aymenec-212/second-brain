"""Session lifecycle: the thin coordinator.

A SessionRuntime owns one live session. It persists every conversational
turn to the transcript *before* the model sees it, keeps the in-memory
history the chat prompt needs, and funnels /save, close, Ctrl-C, and
crash re-runs through the single ingest_session path.

Write ordering: canonical Markdown first, index second and best-effort.
An indexing failure (network, provider outage) is traced and swallowed —
thinking is never lost to an outage, and `sb reindex` heals the drift.
"""

from __future__ import annotations

from second_brain.domain.ingestion import ingest_session
from second_brain.domain.models import Note, Role, TraceEvent, Turn, new_id
from second_brain.domain.ports import (
    ChatResponder,
    Embedder,
    NoteIndex,
    NoteRepository,
    Segmenter,
    TraceSink,
    TranscriptStore,
    Enricher,
)
from second_brain.domain.retrieval import index_notes


class SessionRuntime:
    def __init__(
        self,
        *,
        responder: ChatResponder,
        segmenter: Segmenter,
        repo: NoteRepository,
        transcripts: TranscriptStore,
        traces: TraceSink,
        embedder: Embedder,
        index: NoteIndex,
        enricher: Enricher,
    ) -> None:
        self._responder = responder
        self._segmenter = segmenter
        self._repo = repo
        self._transcripts = transcripts
        self._traces = traces
        self._embedder = embedder
        self._index = index
        self._enricher = enricher
        self.session_id = new_id()
        self._history: list[Turn] = []
        self._next_index = 0
        self._closed = False
        self._emit("session_opened")

    def chat_turn(self, content: str) -> str:
        if self._closed:
            raise RuntimeError("session is closed")
        user_turn = self._append(Role.USER, content)
        self._emit("turn_received", turn_index=user_turn.index, chars=len(content))
        reply = self._responder.reply(self._history)
        assistant_turn = self._append(Role.ASSISTANT, reply)
        self._emit("reply_sent", turn_index=assistant_turn.index, chars=len(reply))
        return reply

    def save(self, trigger: str = "save") -> list[Note]:
        """Ingest everything pending. Reads the transcript back from disk —
        the running process is never the source of truth."""
        turns = self._transcripts.read(self.session_id)
        notes = ingest_session(
            session_id=self.session_id,
            turns=turns,
            repo=self._repo,
            segmenter=self._segmenter,
        )
        self._emit("ingestion_completed", trigger=trigger, note_ids=[n.id for n in notes])
        if notes:
            try:
                index_notes(notes, embedder=self._embedder, index=self._index, enricher=self._enricher)
                self._emit("notes_indexed", count=len(notes))
            except Exception as exc:  # noqa: BLE001 — canonical write already succeeded
                self._emit("indexing_failed", error=str(exc))
        return notes

    def close(self) -> list[Note]:
        """Idempotent twice over: the flag guards the runtime, and the
        derived watermark would make a second ingestion a no-op anyway."""
        if self._closed:
            return []
        notes = self.save(trigger="close")
        self._closed = True
        self._emit("session_closed")
        return notes

    def _append(self, role: Role, content: str) -> Turn:
        turn = Turn(index=self._next_index, role=role, content=content)
        self._transcripts.append(self.session_id, turn)  # disk first, always
        self._history.append(turn)
        self._next_index += 1
        return turn

    def _emit(self, kind: str, turn_index: int | None = None, **payload: object) -> None:
        self._traces.emit(
            TraceEvent(
                session_id=self.session_id,
                turn_index=turn_index,
                kind=kind,
                payload=dict(payload),
            )
        )
