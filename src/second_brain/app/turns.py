"""Turn dispatch: the deterministic ladder.

Order: slash commands (free) → intent router (one call) → dispatch.
The router proposes a validated RouterDecision; this module disposes —
a plain loop over intents executing injected callables. Fallbacks are
deterministic: routing failure degrades to chat, low confidence asks for
a rephrase, a web failure reports itself honestly.

Only chat-intent turns reach the transcript — a question *about* memory
is not thinking *worth remembering* — and this falls out of the
structure: chat_turn is the only path that appends.
"""

from __future__ import annotations

from collections.abc import Callable

from second_brain.app.session import SessionRuntime
from second_brain.domain.contracts import ActivityQueryPlan, Intent
from second_brain.domain.models import (
    ActivityReport,
    AskResult,
    ChatReply,
    SaveAck,
    SessionClosed,
    TurnResult,
    WebAnswer,
)
from second_brain.domain.ports import IntentRouter
from second_brain.infra.llm.router import RoutingFailure

_HELP = "Commands: /save (ingest now) · /quit (close the session). Anything else is conversation."
_CLARIFY = (
    "I'm not sure what you're asking me to do — could you rephrase? / "
    "Je ne suis pas sûr de ce que tu me demandes — tu peux reformuler ?"
)
_WEB_FAILED = "The web search didn't return anything usable — try rephrasing."

AskFn = Callable[[str, str | None], AskResult]
ActivityFn = Callable[[ActivityQueryPlan], ActivityReport]
WebFn = Callable[[str], WebAnswer]


def handle_turn(
    runtime: SessionRuntime,
    raw: str,
    *,
    router: IntentRouter,
    ask: AskFn,
    activity: ActivityFn,
    web: WebFn,
    confidence_floor: float = 0.4,
) -> list[TurnResult]:
    text = raw.strip()
    if text.startswith("/"):
        command = text.split()[0].lower()
        if command == "/save":
            return [SaveAck(notes=runtime.save())]
        if command == "/quit":
            return [SessionClosed(notes=runtime.close())]
        return [ChatReply(text=_HELP)]

    try:
        decision = router.route(text, runtime.history_tail())
    except RoutingFailure as exc:
        runtime.trace("routing_failed", error=str(exc))
        return [ChatReply(text=runtime.chat_turn(text))]

    runtime.trace(
        "turn_routed",
        intents=[intent.value for intent in decision.intents],
        confidence=decision.confidence,
        question=decision.question,
        query_en=decision.query_en,
        plan=decision.activity.model_dump(mode="json") if decision.activity else None,
    )

    if decision.confidence < confidence_floor:
        return [ChatReply(text=_CLARIFY)]

    results: list[TurnResult] = []
    for intent in decision.intents:
        if intent is Intent.CHAT:
            results.append(ChatReply(text=runtime.chat_turn(text)))
        elif intent is Intent.SAVE:
            results.append(SaveAck(notes=runtime.save()))
        elif intent is Intent.NOTES_QA:
            results.append(ask(decision.question or text, decision.query_en))
        elif intent is Intent.ACTIVITY:
            assert decision.activity is not None  # guaranteed by the contract
            results.append(activity(decision.activity))
        elif intent is Intent.WEB_SEARCH:
            try:
                results.append(web(decision.question or text))
            except Exception as exc:  # noqa: BLE001 — a web hiccup must not sink the turn
                runtime.trace("web_failed", error=str(exc))
                results.append(ChatReply(text=_WEB_FAILED))
    return results
