"""ChatResponder adapter: the conversational cognitive task.

The prompt lives here, next to the only code that uses it. Note the final
rule: the chat surface never pretends to remember other sessions. Recall
from past notes is retrieval's job — a chat model improvising memories
would be ungrounded by construction.
"""

from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI

from second_brain.domain.models import Turn

_SYSTEM_PROMPT = """\
You are the conversational surface of a personal "second brain": a private
space where one user thinks through ideas out loud.

Rules:
- Be a sharp, warm thinking partner. Help push the idea forward; question
  assumptions when it helps.
- Reply in the language of the user's latest message (English or French).
- Stay concise: this is dialogue, not essay. One good question beats three.
- Never claim to remember other sessions. Recall from past notes is handled
  by another component; inventing memories would be worse than having none.
"""


class OpenAIChatResponder:
    """Implements the ChatResponder port over the Chat Completions API."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def reply(self, history: Sequence[Turn]) -> str:
        messages: list[dict[str, str]] = [{"role": "system", "content": _SYSTEM_PROMPT}]
        messages.extend(
            {"role": turn.role.value, "content": turn.content} for turn in history
        )
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
            # gpt-5 family knob: minimal keeps the REPL snappy. Revisit if the
            # chat_model setting ever points outside the reasoning families.
            reasoning_effort="minimal",
        )
        return completion.choices[0].message.content or ""