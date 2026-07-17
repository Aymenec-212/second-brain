"""Turn dispatch: the deterministic ladder.

Slash commands resolve before any model is consulted; everything else is
conversation. Phase 4's intent router slots in exactly here — between the
command check and the chat fallthrough.

Control commands are traced but never appended to the transcript:
transcripts hold thinking, not control signals.
"""

from __future__ import annotations

from second_brain.app.session import SessionRuntime
from second_brain.domain.models import ChatReply, SaveAck, SessionClosed, TurnResult

_HELP = "Commands: /save (ingest now) · /quit (close the session). Anything else is conversation."


def handle_turn(runtime: SessionRuntime, raw: str) -> TurnResult:
    text = raw.strip()
    if text.startswith("/"):
        command = text.split()[0].lower()
        if command == "/save":
            return SaveAck(notes=runtime.save())
        if command == "/quit":
            return SessionClosed(notes=runtime.close())
        return ChatReply(text=_HELP)
    return ChatReply(text=runtime.chat_turn(text))
