"""Core domain entities.

this module imports nothing from app, infra, or presentation.
these are pure business objects (entities in domain driven design)
Serialization concerns (YAML frontmatter, JSONL) belong to infrastructure.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, Field, StringConstraints, model_validator
from ulid import ULID

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def utc_now() -> datetime:
    return datetime.now(UTC)


def new_id(at: datetime | None = None) -> str:
    """ULIDs are time-sortable. `at` lets seeded data mint ids from simulated time."""
    return str(ULID.from_datetime(at)) if at is not None else str(ULID())


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class Language(StrEnum):
    EN = "en"
    FR = "fr"
    MIXED = "mixed"


class NoteType(StrEnum):
    IDEA = "idea"
    DECISION = "decision"
    FACT = "fact"
    TASK = "task"
    JOURNAL = "journal"


class Turn(BaseModel):
    """One utterance. `index` is absolute within its session — spans depend on it."""

    index: int = Field(ge=0)
    role: Role
    content: NonEmptyStr
    ts: datetime = Field(default_factory=utc_now)


class SourceSpan(BaseModel):
    """Provenance: exactly which turns of which session a note distills."""

    session_id: str
    start_turn: int = Field(ge=0)
    end_turn: int = Field(ge=0)

    @model_validator(mode="after")
    def _ordered(self) -> SourceSpan:
        if self.end_turn < self.start_turn:
            raise ValueError("end_turn must be >= start_turn")
        return self


class Note(BaseModel):
    """The atomic unit of memory: one idea, decision, or fact-cluster.

    The note is also the retrieval unit — the granularity chosen at write
    time is what fixes recall quality later.
    """

    id: str = Field(default_factory=new_id)
    title: NonEmptyStr
    created_at: datetime = Field(default_factory=utc_now)
    language: Language
    type: NoteType
    tags: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    source: SourceSpan
    supersedes: str | None = None
    superseded_by: str | None = None
    body: NonEmptyStr


class TraceEvent(BaseModel):
    """One observable fact about a turn. The trace log is the debugger."""

    ts: datetime = Field(default_factory=utc_now)
    session_id: str
    turn_index: int | None = None
    kind: str
    payload: dict[str, Any] = Field(default_factory=dict)


class ChatReply(BaseModel):
    """Plain conversational response."""

    text: str


class SaveAck(BaseModel):
    """Confirmation that notes were persisted."""

    notes: list[Note]


TurnResult = ChatReply | SaveAck

class SessionClosed(BaseModel):
    """Final ingestion happened; the session accepts no more turns."""

    notes: list[Note]


TurnResult = ChatReply | SaveAck | SessionClosed

class SearchHit(BaseModel):
    """One retrieval candidate. Cosine similarity; higher is better."""

    note_id: str
    score: float

class Answer(BaseModel):
    """Confident, grounded answer with its sources."""

    text: str
    sources: list[Note]


class HedgedAnswer(BaseModel):
    """Best available match, explicitly below full confidence."""

    text: str
    sources: list[Note]
    top_score: float


class Abstention(BaseModel):
    """The notes don't cover it — said plainly."""

    message: str


AskResult = Answer | HedgedAnswer | Abstention

class ActivityReport(BaseModel):
    """Deterministic answer to 'what did I work on': notes matched by SQL."""

    caption: str
    notes: list[Note]


TurnResult = (
    ChatReply | SaveAck | SessionClosed | ActivityReport
    | Answer | HedgedAnswer | Abstention
)