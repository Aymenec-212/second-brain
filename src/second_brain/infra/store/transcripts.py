"""Append-only transcript archive: one JSONL file per session.

Turns hit disk as they happen, so a crashed session loses at most the line
being written. Ingestion at session close reads back from this file — the
running process is never the source of truth.
"""

from __future__ import annotations

from pathlib import Path

from second_brain.domain.models import Turn


class JsonlTranscriptStore:
    """Implements the TranscriptStore port."""

    def __init__(self, transcripts_dir: Path) -> None:
        self._dir = transcripts_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def append(self, session_id: str, turn: Turn) -> None:
        path = self._dir / f"{session_id}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(turn.model_dump_json() + "\n")

    def read(self, session_id: str) -> list[Turn]:
        """A session with no file yet reads as an empty transcript."""
        path = self._dir / f"{session_id}.jsonl"
        if not path.exists():
            return []
        with path.open(encoding="utf-8") as f:
            return [Turn.model_validate_json(line) for line in f if line.strip()]
