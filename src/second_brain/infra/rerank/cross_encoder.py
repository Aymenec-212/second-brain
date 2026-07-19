"""Local cross-encoder reranker: the leg we pin instead of rent.

The abstention gate thresholds these scores, so they must be deterministic
and stable across runs — the reason this is a local model and not an LLM
judge (decision log #21). Logits pass through a sigmoid so thresholds read
as probabilities in [0, 1].

sentence-transformers (and torch underneath) is imported lazily on the
first rerank call: `sb chat` never pays the torch import, only `sb ask`
and the evals do.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from second_brain.domain.models import Note
from second_brain.domain.retrieval import rerank_text


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


class CrossEncoderReranker:
    """Implements the Reranker port over a sentence-transformers CrossEncoder."""

    def __init__(self, model_name: str, max_length: int = 1024) -> None:
        self._model_name = model_name
        self._max_length = max_length
        self._model: Any = None

    def rerank(self, query: str, notes: Sequence[Note]) -> list[float]:
        if not notes:
            return []
        pairs = [(query, rerank_text(note)) for note in notes]
        logits = self._ensure_model().predict(pairs)
        return [_sigmoid(float(logit)) for logit in logits]

    def _ensure_model(self) -> Any:
        if self._model is None:
            from sentence_transformers import CrossEncoder  # lazy: torch is heavy

            self._model = CrossEncoder(self._model_name, max_length=self._max_length)
        return self._model
