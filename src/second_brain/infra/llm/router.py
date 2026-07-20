"""Intent router adapter: one small structured call per turn.

The router classifies, extracts a SELF-CONTAINED question (references
resolved from the recent exchanges and today's date), pivots it to
English, and fills the activity plan. It proposes; app/turns.py disposes.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from openai import OpenAI
from pydantic import ValidationError

from second_brain.domain.contracts import RouterDecision

_MAX_ATTEMPTS = 3

_SYSTEM_PROMPT = """\
You route one turn of a conversation between a user and their personal
"second brain". Today is {today}.

Intents — emit 1 to 3, ordered by execution:
- chat: the default. Thinking out loud, developing ideas, anything that is
  not one of the cases below.
- save: an explicit ask to save or note now ("save that", "note ça",
  "garde une note là-dessus").
- notes_qa: a question about the user's own past thinking or notes
  ("what did I decide about X?", "qu'est-ce que j'avais dit sur X ?").
- activity: a meta question about the store itself — browsing or
  summarizing by time, tag, or kind ("what did I work on last week?",
  "montre mes notes de juin sur cairn"). Keep limit at 20 unless the user
  explicitly asks for everything.
- web_search: only when they explicitly ask to search the web or internet.

Rules:
- question must be SELF-CONTAINED. Resolve pronouns and references
  ("that", "it", "the match", "today") using the recent exchanges and
  today's date, so it can be executed with no other context.
  "report what match is played today" after talk of the World Cup in the
  USA → "what men's football World Cup match is played in the USA today,
  {today}?".
- A turn that refines, corrects, or answers a clarification about a
  previous request keeps that request's intent — check the recent
  exchanges. Refining an earlier web search is still web_search.
- A content question that merely mentions time stays notes_qa; activity is
  for browsing/summarizing the store, not for content answers.
- question: original language; query_en: its faithful English pivot
  (identical if already English).
- activity: fill the plan; resolve relative dates ("last week",
  "ce mois-ci") into absolute ISO dates using today's date.
- Mixed turns: order intents as they should execute
  ("save that, and what did I say about X?" → [save, notes_qa]).
- confidence: your honest routing confidence in [0, 1].
"""


class RoutingFailure(RuntimeError):
    """No valid decision within the attempt budget."""


def render_context(context: Sequence[str], text: str) -> str:
    tail = "\n".join(context)
    prefix = f"Recent exchanges (oldest first):\n{tail}\n\n" if tail else ""
    return f"{prefix}Current turn to route:\n{text}"


class OpenAIIntentRouter:
    """Implements the IntentRouter port with structured outputs + bounded retry."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def route(self, text: str, context: Sequence[str]) -> RouterDecision:
        system = _SYSTEM_PROMPT.format(today=datetime.now(UTC).date().isoformat())
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": render_context(context, text)},
        ]
        last_error = ""
        for _ in range(_MAX_ATTEMPTS):
            try:
                completion = self._client.chat.completions.parse(
                    model=self._model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=RouterDecision,
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
                            f"Your previous decision was invalid: {last_error}. "
                            "Route the same turn again, obeying every rule."
                        ),
                    }
                )
        raise RoutingFailure(f"no valid decision after {_MAX_ATTEMPTS} attempts: {last_error}")
