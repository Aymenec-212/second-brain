"""Query pivoter: English form of a query, for the lexical leg only.

The dense leg and the reranker are natively cross-lingual and receive the
original query; only FTS5 needs an English shadow. Phase 4's intent router
absorbs this task into its single per-turn call — the port is shaped for
that handover.
"""

from __future__ import annotations

from openai import OpenAI
from pydantic import ValidationError

from second_brain.domain.contracts import QueryPivot

_MAX_ATTEMPTS = 2

_SYSTEM_PROMPT = """\
Return the English form of the user's search query.
- If it is already English, return it unchanged.
- Translate French faithfully; keep names, project names, and numbers
  exactly as written.
- Output the query only — no explanation, no expansion.
"""


class OpenAIQueryPivoter:
    """Implements the QueryPivoter port. Falls back to the original query
    rather than failing — a missing pivot degrades the lexical leg, it
    should never block an answer."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def pivot(self, query: str) -> str:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
        for _ in range(_MAX_ATTEMPTS):
            try:
                completion = self._client.chat.completions.parse(
                    model=self._model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=QueryPivot,
                )
                parsed = completion.choices[0].message.parsed
                if parsed is not None:
                    return parsed.english
            except ValidationError:
                continue
        return query
