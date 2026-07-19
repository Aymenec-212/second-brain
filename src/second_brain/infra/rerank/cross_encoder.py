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

from collections.abc import Sequence
from typing import Any

from second_brain.domain.models import Note
from second_brain.domain.retrieval import rerank_text



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
        scores = self._ensure_model().predict(pairs)
        # CrossEncoder already applies sigmoid for single-label models —
        # our own on top squashed everything into [0.5, 0.73] and silently
        # disabled the abstention gate. Found via the ask_decided traces.
        return [min(1.0, max(0.0, float(score))) for score in scores]

    def _ensure_model(self) -> Any:
        if self._model is None:
            from sentence_transformers import CrossEncoder  # lazy: torch is heavy

            self._model = CrossEncoder(self._model_name, max_length=self._max_length)
        return self._model
