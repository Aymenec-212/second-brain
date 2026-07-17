"""Store round-trip tests. Everything offline, everything on tmp_path."""

from pathlib import Path

from second_brain.domain.models import (
    Language,
    Note,
    NoteType,
    Role,
    SourceSpan,
    TraceEvent,
    Turn,
)
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink

ULID_A = "01ARZ3NDEKTSV4RRFFQ69G5FAA"
ULID_B = "01BRZ3NDEKTSV4RRFFQ69G5FAB"


def make_note(note_id: str, title: str = "Décision: héberger l'index dans SQLite") -> Note:
    return Note(
        id=note_id,
        title=title,
        language=Language.FR,
        type=NoteType.DECISION,
        tags=["architecture", "sqlite"],
        entities=["SQLite"],
        source=SourceSpan(session_id="s-001", start_turn=0, end_turn=3),
        body="On a comparé plusieurs options — l'index dérivé reste reconstructible.",
    )


def test_note_roundtrip_preserves_everything(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    note = make_note(ULID_A)
    repo.save(note)
    assert repo.get(ULID_A) == note


def test_accented_titles_make_clean_ascii_filenames(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    repo.save(make_note(ULID_A))
    (path,) = tmp_path.glob("*.md")
    assert path.name.startswith(f"{ULID_A}--decision-heberger-l-index")


def test_save_is_an_upsert(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    note = make_note(ULID_A)
    repo.save(note)
    repo.save(note.model_copy(update={"superseded_by": ULID_B}))
    assert len(list(tmp_path.glob("*.md"))) == 1
    loaded = repo.get(ULID_A)
    assert loaded is not None
    assert loaded.superseded_by == ULID_B


def test_missing_note_returns_none(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    assert repo.get("01ZZZZZZZZZZZZZZZZZZZZZZZZ") is None


def test_iter_all_is_chronological(tmp_path: Path) -> None:
    repo = MarkdownNoteRepository(tmp_path)
    repo.save(make_note(ULID_B, title="Later note"))
    repo.save(make_note(ULID_A, title="Earlier note"))
    assert [n.id for n in repo.iter_all()] == [ULID_A, ULID_B]


def test_transcript_roundtrip_and_missing_session(tmp_path: Path) -> None:
    store = JsonlTranscriptStore(tmp_path)
    turns = [
        Turn(index=0, role=Role.USER, content="Salut, je réfléchis à mon projet"),
        Turn(index=1, role=Role.ASSISTANT, content="Dis-m'en plus."),
    ]
    for turn in turns:
        store.append("s-001", turn)
    assert store.read("s-001") == turns
    assert store.read("never-existed") == []


def test_trace_sink_appends_one_line_per_event(tmp_path: Path) -> None:
    sink = JsonlTraceSink(tmp_path)
    sink.emit(TraceEvent(session_id="s-001", kind="turn_received", payload={"chars": 42}))
    sink.emit(TraceEvent(session_id="s-001", kind="reply_sent"))
    lines = (tmp_path / "s-001.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
