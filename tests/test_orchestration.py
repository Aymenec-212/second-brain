"""Orchestration tests: the compiler is pure, the dispatch is code,
both fully testable without any model. The router adapter itself follows
the proven structured-output retry pattern and is exercised by the real
system; router *accuracy* belongs to the eval harness.
"""

from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from second_brain.app.session import SessionRuntime
from second_brain.app.turns import handle_turn
from second_brain.domain.contracts import ActivityQueryPlan, Intent, RouterDecision
from second_brain.domain.models import (
    Abstention,
    ActivityReport,
    ChatReply,
    Language,
    Note,
    NoteType,
    SaveAck,
    SourceSpan,
    Turn,
)
from second_brain.infra.index.activity import compile_activity_query
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.fakes import FakeChatResponder, FakeEmbedder, FakeEnricher, FakeSegmenter
from second_brain.infra.llm.router import RoutingFailure
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink
from second_brain.domain.retrieval import index_notes


# --- compiler -------------------------------------------------------------

def test_compiler_builds_bounded_parameterized_sql() -> None:
    plan = ActivityQueryPlan(
        since=date(2026, 6, 1),
        until=date(2026, 6, 30),
        tags=["Cairn", "running"],
        types=[NoteType.DECISION],
        limit=10,
    )
    sql, params = compile_activity_query(plan)
    assert "created_at >= ?" in sql and "created_at < ?" in sql
    assert sql.count("tags LIKE ?") == 2
    assert "type IN (?)" in sql
    assert sql.strip().endswith("LIMIT ?")
    assert params[0] == "2026-06-01"
    assert params[1] == "2026-07-01"  # inclusive end → strictly before next day
    assert '%"cairn"%' in params  # tags folded to write-time lowercase
    assert params[-1] == 10


def test_compiler_with_empty_plan_is_just_recency() -> None:
    sql, params = compile_activity_query(ActivityQueryPlan())
    assert "WHERE 1=1" in sql
    assert params == [20]


# --- activity search against a real index ---------------------------------

def dated_note(note_id: str, title: str, when: datetime, tags: list[str]) -> Note:
    return Note(
        id=note_id,
        title=title,
        created_at=when,
        language=Language.EN,
        type=NoteType.IDEA,
        tags=tags,
        source=SourceSpan(session_id="s", start_turn=0, end_turn=1),
        body=f"Body of {title}.",
    )


JUNE_CAIRN = dated_note(
    "01ARZ3NDEKTSV4RRFFQ69G5FAA", "Cairn beta feedback",
    datetime(2026, 6, 20, tzinfo=UTC), ["cairn"],
)
JULY_RUN = dated_note(
    "01BRZ3NDEKTSV4RRFFQ69G5FAB", "Hydration strategy",
    datetime(2026, 7, 4, tzinfo=UTC), ["marathon"],
)
JAN_BREAD = dated_note(
    "01CRZ3NDEKTSV4RRFFQ69G5FAC", "Levain restart",
    datetime(2026, 1, 15, tzinfo=UTC), ["cuisine"],
)


def seeded_index(tmp_path: Path) -> SqliteNoteIndex:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    index_notes(
        [JUNE_CAIRN, JULY_RUN, JAN_BREAD],
        enricher=FakeEnricher(), embedder=embedder, index=index,
    )
    return index


def test_activity_search_filters_by_window_and_orders_desc(tmp_path: Path) -> None:
    index = seeded_index(tmp_path)
    ids = index.activity_search(
        ActivityQueryPlan(since=date(2026, 6, 1), until=date(2026, 7, 31))
    )
    assert ids == [JULY_RUN.id, JUNE_CAIRN.id]  # newest first, January excluded


def test_activity_search_filters_by_tag(tmp_path: Path) -> None:
    index = seeded_index(tmp_path)
    assert index.activity_search(ActivityQueryPlan(tags=["cairn"])) == [JUNE_CAIRN.id]


# --- dispatch --------------------------------------------------------------

class StubRouter:
    def __init__(self, decision: RouterDecision | Exception) -> None:
        self._decision = decision

    def route(self, text: str, history: Sequence[Turn]) -> RouterDecision:
        if isinstance(self._decision, Exception):
            raise self._decision
        return self._decision


def runtime_with(tmp_path: Path) -> tuple[SessionRuntime, JsonlTranscriptStore]:
    transcripts = JsonlTranscriptStore(tmp_path / "transcripts")
    embedder = FakeEmbedder()
    runtime = SessionRuntime(
        responder=FakeChatResponder(),
        segmenter=FakeSegmenter(),
        repo=MarkdownNoteRepository(tmp_path / "notes"),
        transcripts=transcripts,
        traces=JsonlTraceSink(tmp_path / "traces"),
        embedder=embedder,
        index=SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions),
        enricher=FakeEnricher(),
    )
    return runtime, transcripts


def fake_ask(question: str, pivot: str | None) -> Abstention:
    return Abstention(message=f"asked: {question} (pivot={pivot})")


def fake_activity(plan: ActivityQueryPlan) -> ActivityReport:
    return ActivityReport(caption=f"limit={plan.limit}", notes=[])


def decision(*intents: Intent, **kwargs: object) -> RouterDecision:
    return RouterDecision(intents=list(intents), confidence=0.9, **kwargs)


def test_mixed_turn_executes_in_order(tmp_path: Path) -> None:
    runtime, _ = runtime_with(tmp_path)
    runtime.chat_turn("we decided flutter for cairn")  # something to save
    results = handle_turn(
        runtime,
        "save that, and what did I say about Cairn?",
        router=StubRouter(
            decision(
                Intent.SAVE, Intent.NOTES_QA,
                question="what did I say about Cairn?",
                query_en="what did I say about Cairn?",
            )
        ),
        ask=fake_ask,
        activity=fake_activity,
    )
    assert isinstance(results[0], SaveAck)
    assert isinstance(results[1], Abstention)
    assert "pivot=what did I say about Cairn?" in results[1].message


def test_activity_intent_dispatches_the_plan(tmp_path: Path) -> None:
    runtime, _ = runtime_with(tmp_path)
    results = handle_turn(
        runtime,
        "what did I work on last week?",
        router=StubRouter(
            decision(Intent.ACTIVITY, activity=ActivityQueryPlan(limit=7))
        ),
        ask=fake_ask,
        activity=fake_activity,
    )
    assert isinstance(results[0], ActivityReport)
    assert results[0].caption == "limit=7"


def test_low_confidence_asks_to_rephrase_without_models(tmp_path: Path) -> None:
    runtime, _ = runtime_with(tmp_path)
    low = RouterDecision(intents=[Intent.NOTES_QA], confidence=0.2, question="hmm?")
    results = handle_turn(
        runtime, "euh…", router=StubRouter(low), ask=fake_ask, activity=fake_activity
    )
    assert isinstance(results[0], ChatReply)
    assert "rephrase" in results[0].text or "reformuler" in results[0].text


def test_routing_failure_degrades_to_chat(tmp_path: Path) -> None:
    runtime, _ = runtime_with(tmp_path)
    results = handle_turn(
        runtime,
        "just thinking out loud",
        router=StubRouter(RoutingFailure("boom")),
        ask=fake_ask,
        activity=fake_activity,
    )
    assert isinstance(results[0], ChatReply)
    assert results[0].text == "ok"  # FakeChatResponder replied → real chat path


def test_only_chat_turns_enter_the_transcript(tmp_path: Path) -> None:
    runtime, transcripts = runtime_with(tmp_path)
    handle_turn(
        runtime,
        "what did I decide about Cairn?",
        router=StubRouter(decision(Intent.NOTES_QA, question="Cairn?", query_en="Cairn?")),
        ask=fake_ask,
        activity=fake_activity,
    )
    assert transcripts.read(runtime.session_id) == []  # question about memory ≠ thinking
    handle_turn(
        runtime,
        "let me think about pricing",
        router=StubRouter(decision(Intent.CHAT)),
        ask=fake_ask,
        activity=fake_activity,
    )
    contents = [t.content for t in transcripts.read(runtime.session_id)]
    assert contents == ["let me think about pricing", "ok"]


def test_contract_rejects_activity_without_plan() -> None:
    with pytest.raises(ValueError):
        RouterDecision(intents=[Intent.ACTIVITY], confidence=0.9)
