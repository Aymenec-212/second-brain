"""Answerer adapter: question + retrieved notes → grounded answer.

Same enforcement pattern as the segmenter: structured outputs constrain
shape, contract validators constrain semantics, and this adapter checks
what no schema can — that every cited id is among the notes actually
provided, and that a grounded answer cites at least one.
"""

from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI
from pydantic import ValidationError

from second_brain.domain.contracts import AnswerDraft
from second_brain.domain.models import Note

_MAX_ATTEMPTS = 3

_SYSTEM_PROMPT = """\
You answer questions from one user's personal knowledge store. You receive
their question and a set of notes retrieved from their past thinking
sessions. The notes are the only world you know.

Rules:
- Lead with the answer: first sentence answers the question directly.
  Keep it to a short paragraph unless the question truly needs more.
- Do not summarize every provided note — use only what answers the
  question, ignore the rest.
- Answer ONLY from the notes. No outside knowledge, no guessing, no
  filling gaps with plausible details.
- Report every figure exactly as it appears in a note. Never perform
  arithmetic, never combine, reconcile, or estimate numbers.
- If notes disagree, give the newest value, mention the older one with
  its date, and say the thinking changed.  
- If the notes do not contain the answer, set grounded=false and say so
  briefly and plainly.
- cited_note_ids lists exactly the notes your answer draws on.
- Answer in the language of the question, whatever language the notes are
  written in.
"""


class InvalidAnswer(ValueError):
    """A structurally valid draft that violates a grounding rule."""


class AnswerFailure(RuntimeError):
    """No valid answer within the attempt budget."""


def render_notes(notes: Sequence[Note]) -> str:
    blocks = [
        f"[{note.id}] {note.title} — {note.created_at.date().isoformat()}"
        f" ({note.language.value})\n{note.body}"
        for note in notes
    ]
    return "\n\n---\n\n".join(blocks)


def check_citations(draft: AnswerDraft, allowed_ids: set[str]) -> None:
    unknown = [i for i in draft.cited_note_ids if i not in allowed_ids]
    if unknown:
        raise InvalidAnswer(
            f"cited note ids that were not provided: {unknown}; "
            "cite only the notes you were given"
        )
    if draft.grounded and not draft.cited_note_ids:
        raise InvalidAnswer("a grounded answer must cite at least one note")


class OpenAIAnswerer:
    """Implements the Answerer port with structured outputs + bounded retry."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def answer(self, question: str, notes: Sequence[Note]) -> AnswerDraft:
        allowed_ids = {note.id for note in notes}
        messages: list[dict[str, str]] = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question: {question}\n\nNotes:\n\n{render_notes(notes)}",
            },
        ]
        last_error = ""
        for _ in range(_MAX_ATTEMPTS):
            try:
                completion = self._client.chat.completions.parse(
                    model=self._model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=AnswerDraft,
                )
                draft = completion.choices[0].message.parsed
                if draft is None:
                    raise InvalidAnswer("empty or refused output")
                check_citations(draft, allowed_ids)
                return draft
            except (ValidationError, InvalidAnswer) as exc:
                last_error = str(exc)
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Your previous answer was invalid: {last_error}. "
                            "Answer the same question again, obeying every rule."
                        ),
                    }
                )
        raise AnswerFailure(f"no valid answer after {_MAX_ATTEMPTS} attempts: {last_error}")
