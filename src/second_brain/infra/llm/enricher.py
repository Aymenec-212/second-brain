"""Enricher adapter: one note → English gist + questions it answers.

This is the write-time attack on the two hardest retrieval constraints:
"queries and notes rarely share surface form" (the questions field is a
doc2query bridge) and cross-lingual reach (the gist gives the lexical leg
an English shadow of every French note).
"""

from __future__ import annotations

from openai import OpenAI
from pydantic import ValidationError

from second_brain.domain.contracts import NoteEnrichment
from second_brain.domain.models import Note

_MAX_ATTEMPTS = 3

_SYSTEM_PROMPT = """\
You enrich one note from a personal knowledge store so it can be found
later, including across languages. The store's owner writes in English
and French; retrieval normalizes to English.

Given the note, produce:
- gist_en: a 2-4 sentence English summary. Keep every number, name, and
  date. If the note is in French, translate faithfully — do not embellish.
- questions: 3-6 short English questions this note answers, phrased the
  way the owner might actually ask months later ("what did I decide
  about…", "how much…", "which… did I pick for…", "when…").
"""


class EnrichmentFailure(RuntimeError):
    """No valid enrichment within the attempt budget."""


class OpenAIEnricher:
    """Implements the Enricher port with structured outputs + bounded retry."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def enrich(self, note: Note) -> NoteEnrichment:
        content = (
            f"Note language: {note.language.value}\n"
            f"Title: {note.title}\n\n{note.body}"
        )
        messages: list[dict[str, str]] = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ]
        last_error = ""
        for _ in range(_MAX_ATTEMPTS):
            try:
                completion = self._client.chat.completions.parse(
                    model=self._model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=NoteEnrichment,
                )
                parsed = completion.choices[0].message.parsed
                if parsed is None:
                    raise ValueError("empty or refused output")
                return parsed
            except (ValidationError, ValueError) as exc:
                last_error = str(exc)
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Your previous enrichment was invalid: {last_error}. "
                            "Enrich the same note again, obeying every rule."
                        ),
                    }
                )
        raise EnrichmentFailure(
            f"no valid enrichment after {_MAX_ATTEMPTS} attempts: {last_error}"
        )
