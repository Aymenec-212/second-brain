"""Deterministic fakes for offline tests — and, later, an offline demo mode.

Both fakes record every call so tests can assert on what the core handed
them, not just on what came back.
"""

from __future__ import annotations

from collections.abc import Sequence

from second_brain.domain.contracts import NoteDraft
from second_brain.domain.models import Language, NoteType, Turn


class FakeChatResponder:
    """Replays canned replies in order; falls back to a fixed answer."""

    def __init__(self, replies: Sequence[str] = ()) -> None:
        self._replies = list(replies)
        self.calls: list[list[Turn]] = []

    def reply(self, history: Sequence[Turn]) -> str:
        self.calls.append(list(history))
        if self._replies:
            return self._replies.pop(0)
        return "ok"


class FakeSegmenter:
    """Returns preset drafts, or one whole-span draft derived from the input."""

    def __init__(self, drafts: list[NoteDraft] | None = None) -> None:
        self._drafts = drafts
        self.calls: list[list[Turn]] = []

    def segment(self, turns: Sequence[Turn]) -> list[NoteDraft]:
        self.calls.append(list(turns))
        if not turns:
            return []
        if self._drafts is not None:
            return self._drafts
        return [
            NoteDraft(
                title=f"Fake note: {turns[0].content[:40]}",
                language=Language.EN,
                type=NoteType.IDEA,
                tags=["fake"],
                start_turn=turns[0].index,
                end_turn=turns[-1].index,
                body=" ".join(t.content for t in turns),
            )
        ]