"""Segmenter adapter: transcript → validated note drafts.

Three enforcement layers, each catching what the previous cannot:
1. Structured outputs constrain the shape server-side.
2. Pydantic validators on the contract enforce field semantics.
3. This adapter checks the one thing no static schema can express —
   that spans point inside the actual transcript.

Any violation triggers a bounded retry with the violated rule named;
exhausting the budget raises a typed failure for the app layer to trace.
"""

from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI
from pydantic import ValidationError

from second_brain.domain.contracts import NoteDraft, SegmentationResult
from second_brain.domain.models import Turn

_MAX_ATTEMPTS = 3

_SYSTEM_PROMPT = """\
You convert the transcript of one thinking session into atomic notes for a
personal knowledge store. The session is a private dialogue between one
user and an assistant.

Segmentation rules:
- One note per distinct idea, decision, fact-cluster, task, or personal
  log entry.
- A note's body is distilled but detailed prose, roughly 150-500 words:
  preserve decisions, reasoning, open questions, concrete numbers, names,
  and any phrasing that matters. Drop filler and repetition.
- Each note must stand alone months later: resolve pronouns, name projects
  and people explicitly, restate the minimal context needed.
- Write each note in the language of its span; use "mixed" only for truly
  bilingual spans.
- start_turn and end_turn are the absolute [n] indices shown in the
  transcript. Spans of different notes may overlap when topics interleave.
- Small talk, greetings, and logistics yield no notes. Returning zero
  notes is the correct answer for a session with no substance.
- Titles are specific and searchable, never generic.
"""


class InvalidSegmentation(ValueError):
    """A structurally valid result that violates a semantic rule."""


class SegmentationFailure(RuntimeError):
    """No valid segmentation within the attempt budget."""


def render_transcript(turns: Sequence[Turn]) -> str:
    """Absolute indices in [n] brackets — the coordinates spans refer to."""
    return "\n".join(f"[{t.index}] {t.role.value}: {t.content}" for t in turns)


def check_spans(drafts: Sequence[NoteDraft], max_index: int) -> None:
    for draft in drafts:
        if draft.end_turn > max_index:
            raise InvalidSegmentation(
                f"note '{draft.title}' spans up to turn {draft.end_turn}, "
                f"but the transcript ends at turn {max_index}"
            )


class OpenAISegmenter:
    """Implements the Segmenter port with structured outputs + bounded retry."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def segment(self, turns: Sequence[Turn]) -> list[NoteDraft]:
        if not turns:
            return []
        max_index = max(t.index for t in turns)
        messages: list[dict[str, str]] = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": render_transcript(turns)},
        ]
        last_error = ""
        for _ in range(_MAX_ATTEMPTS):
            try:
                completion = self._client.chat.completions.parse(
                    model=self._model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=SegmentationResult,
                )
                parsed = completion.choices[0].message.parsed
                if parsed is None:
                    raise InvalidSegmentation("empty or refused output")
                check_spans(parsed.notes, max_index)
                return parsed.notes
            except (ValidationError, InvalidSegmentation) as exc:
                last_error = str(exc)
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Your previous segmentation was invalid: {last_error}. "
                            "Produce a corrected segmentation of the same "
                            "transcript, obeying every rule."
                        ),
                    }
                )
        raise SegmentationFailure(
            f"no valid segmentation after {_MAX_ATTEMPTS} attempts: {last_error}"
        )