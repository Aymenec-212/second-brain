"""JSONL trace sink: one file per session, one line per event.

The cheapest observability that still answers "what did the system do, and
why" — and because callers only know the TraceSink port, a Langfuse sink
can replace this later without touching a single call site.
"""

from __future__ import annotations

from pathlib import Path

from second_brain.domain.models import TraceEvent


class JsonlTraceSink:
    """Implements the TraceSink port."""

    def __init__(self, traces_dir: Path) -> None:
        self._dir = traces_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def emit(self, event: TraceEvent) -> None:
        path = self._dir / f"{event.session_id}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")
