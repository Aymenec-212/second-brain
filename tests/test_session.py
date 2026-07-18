"""Session lifecycle tests: fakes + real stores on tmp_path, fully offline.

This file is the executable spec for Phase 1's exit criteria.
"""

from collections.abc import Sequence
from pathlib import Path

import pytest

from second_brain.app.session import SessionRuntime
from second_brain.app.turns import handle_turn
from second_brain.domain.models import ChatReply, SaveAck, SessionClosed, TraceEvent, Turn
from second_brain.infra.llm.fakes import FakeChatResponder, FakeSegmenter, FakeEmbedder
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink
from second_brain.infra.index.sqlite import SqliteNoteIndex


class Deps:
    """One session wired with fakes over real stores."""

    def __init__(self, tmp_path: Path) -> None:
        self.repo = MarkdownNoteRepository(tmp_path / "notes")
        self.transcripts = JsonlTranscriptStore(tmp_path / "transcripts")
        self.traces_dir = tmp_path / "traces"
        self.responder = FakeChatResponder()
        self.segmenter = FakeSegmenter()
        self.embedder = FakeEmbedder()
        self.index = SqliteNoteIndex(tmp_path / "index.db", self.embedder.dimensions)
        self.runtime = SessionRuntime(
            responder=self.responder,
            segmenter=self.segmenter,
            embedder=self.embedder,
            index=self.index,
            repo=self.repo,
            transcripts=self.transcripts,
            traces=JsonlTraceSink(self.traces_dir),
        )


class DiskProbeResponder:
    """Records what the transcript file contains at the moment it is called."""

    def __init__(self, store: JsonlTranscriptStore) -> None:
        self._store = store
        self.session_id = ""
        self.on_disk_at_call: list[list[int]] = []

    def reply(self, history: Sequence[Turn]) -> str:
        turns = self._store.read(self.session_id)
        self.on_disk_at_call.append([t.index for t in turns])
        return "ok"


def test_user_turn_hits_disk_before_the_model(tmp_path: Path) -> None:
    transcripts = JsonlTranscriptStore(tmp_path / "transcripts")
    probe = DiskProbeResponder(transcripts)
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    runtime = SessionRuntime(
        responder=probe,
        segmenter=FakeSegmenter(),
        embedder=embedder,
        index=index,
        repo=MarkdownNoteRepository(tmp_path / "notes"),
        transcripts=transcripts,
        traces=JsonlTraceSink(tmp_path / "traces"),
    )
    probe.session_id = runtime.session_id
    handle_turn(runtime, "an idea worth keeping")
    assert probe.on_disk_at_call == [[0]]  # user turn was persisted first


def test_save_mid_session_ingests_the_window(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    handle_turn(deps.runtime, "thinking about retrieval quality")
    result = handle_turn(deps.runtime, "/save")
    assert isinstance(result, SaveAck)
    assert len(result.notes) == 1
    span = result.notes[0].source
    assert (span.start_turn, span.end_turn) == (0, 1)
    #verifies the index was updated with the new note
    assert deps.index.count() == 1


def test_close_ingests_only_the_remainder(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    handle_turn(deps.runtime, "first topic of the evening")
    handle_turn(deps.runtime, "/save")
    handle_turn(deps.runtime, "second topic, after the save")
    result = handle_turn(deps.runtime, "/quit")
    assert isinstance(result, SessionClosed)
    assert [t.index for t in deps.segmenter.calls[1]] == [2, 3]
    assert len(list(deps.repo.iter_all())) == 2


def test_double_close_is_a_noop(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    handle_turn(deps.runtime, "the only topic")
    first = deps.runtime.close()
    second = deps.runtime.close()
    assert len(first) == 1
    assert second == []
    assert len(deps.segmenter.calls) == 1  # second close never reached the model


def test_commands_never_enter_the_transcript(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    handle_turn(deps.runtime, "real content")
    handle_turn(deps.runtime, "/save")
    turns = deps.transcripts.read(deps.runtime.session_id)
    assert [t.content for t in turns] == ["real content", "ok"]


def test_unknown_command_gets_help_without_a_model_call(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    result = handle_turn(deps.runtime, "/sav")
    assert isinstance(result, ChatReply)
    assert "/save" in result.text
    assert deps.responder.calls == []


def test_session_leaves_a_complete_trace(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    handle_turn(deps.runtime, "an idea")
    handle_turn(deps.runtime, "/quit")
    trace_file = deps.traces_dir / f"{deps.runtime.session_id}.jsonl"
    kinds = [
        TraceEvent.model_validate_json(line).kind
        for line in trace_file.read_text(encoding="utf-8").splitlines()
    ]
    assert kinds == [
        "session_opened",
        "turn_received",
        "reply_sent",
        "ingestion_completed",
        "notes_indexed",
        "session_closed",
    ]


def test_chat_after_close_raises(tmp_path: Path) -> None:
    deps = Deps(tmp_path)
    deps.runtime.close()
    with pytest.raises(RuntimeError):
        deps.runtime.chat_turn("hello?")
