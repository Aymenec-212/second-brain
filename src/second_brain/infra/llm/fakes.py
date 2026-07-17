"""Deterministic fakes for offline tests — and, later, an offline demo mode.

The fakes record every call so tests can assert on what the core handed
them, not just on what came back.
"""

from __future__ import annotations

import hashlib
import math
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


class FakeEmbedder:
    """Deterministic bag-of-words hashing embedder.

    Same text → same unit vector, across processes and runs (md5, not
    Python's salted hash). Texts sharing tokens land closer together —
    enough geometric structure for ranking tests without any model.
    """

    def __init__(self, dimensions: int = 32) -> None:
        self._dim = dimensions

    @property
    def dimensions(self) -> int:
        return self._dim

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vec = [0.0] * self._dim
        for token in text.lower().split():
            digest = hashlib.md5(token.encode("utf-8")).digest()
            vec[digest[0] % self._dim] += 1.0
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0.0:
            vec[0] = 1.0
            norm = 1.0
        return [v / norm for v in vec]
