"""OpenAI embedder: the dense leg rents its vectors (decision log #21).

text-embedding-3-large with Matryoshka truncation via `dimensions` — 1536
by default: half the storage and distance compute of the full 3072 for
negligible retrieval loss. The API returns unit-normalized vectors, which
is exactly what makes the index's L2 ↔ cosine equivalence hold.
"""

from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI

_BATCH = 128


class OpenAIEmbedder:
    """Implements the Embedder port.

    Batched: seed and reindex embed hundreds of notes per run; one request
    per note would be the "obviously unnecessary work" the brief warns
    about.
    """

    def __init__(self, client: OpenAI, model: str, dimensions: int) -> None:
        self._client = client
        self._model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), _BATCH):
            batch = list(texts[start : start + _BATCH])
            response = self._client.embeddings.create(
                model=self._model,
                input=batch,
                dimensions=self._dimensions,
            )
            ordered = sorted(response.data, key=lambda item: item.index)
            vectors.extend(item.embedding for item in ordered)
        return vectors
