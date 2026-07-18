"""Seed generator: synthetic sessions pushed through the real pipeline.

The synthesis contract lives here, not in domain contracts — seeding is
tooling, not product. The `synthesize` callable is injected into the run
loop so resumability is testable offline.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from datetime import timedelta

from openai import OpenAI
from pydantic import BaseModel, ValidationError, model_validator

from second_brain.domain.ingestion import ingest_session
from second_brain.domain.models import NonEmptyStr, Role, Turn
from second_brain.domain.ports import (
    Embedder,
    NoteIndex,
    NoteRepository,
    Segmenter,
    TranscriptStore,
)
from second_brain.domain.retrieval import index_notes
from second_brain.seed.spec import SessionBrief, session_id_for

_MAX_ATTEMPTS = 3

_SYNTH_SYSTEM = """\
You write realistic transcripts of private thinking sessions between a
person and their "second brain" assistant.

Rules:
- Write the whole session in the requested language ("mixed" means natural
  French/English code-switching by the person).
- 8 to 14 turns. The first turn is the user's. Roles alternate strictly.
- The user drives: they think out loud with the concrete specifics from
  the brief — keep every number, name, and date it mentions.
- The assistant stays brief: reflects, or asks one sharp question.
- No meta-talk, no mention of this being synthetic; end naturally.
"""


class SyntheticTurn(BaseModel):
    role: Role
    content: NonEmptyStr


class SyntheticSession(BaseModel):
    turns: list[SyntheticTurn]

    @model_validator(mode="after")
    def _well_formed(self) -> SyntheticSession:
        if len(self.turns) < 6:
            raise ValueError("a session needs at least 6 turns")
        if self.turns[0].role is not Role.USER:
            raise ValueError("the first turn must be the user's")
        for prev, cur in zip(self.turns, self.turns[1:], strict=False):
            if prev.role is cur.role:
                raise ValueError("roles must alternate strictly")
        return self


def synthesize_openai(
    client: OpenAI, model: str, persona: str, brief: SessionBrief
) -> list[Turn]:
    prompt = (
        f"Persona:\n{persona}\n"
        f"Date of the session: {brief.date.date().isoformat()}\n"
        f"Language: {brief.language.value}\n"
        f"Brief for this session: {brief.brief}"
    )
    messages: list[dict[str, str]] = [
        {"role": "system", "content": _SYNTH_SYSTEM},
        {"role": "user", "content": prompt},
    ]
    last_error = ""
    for _ in range(_MAX_ATTEMPTS):
        try:
            completion = client.chat.completions.parse(
                model=model,
                messages=messages,  # type: ignore[arg-type]
                response_format=SyntheticSession,
            )
            parsed = completion.choices[0].message.parsed
            if parsed is None:
                raise ValueError("empty or refused output")
            return [
                Turn(
                    index=i,
                    role=turn.role,
                    content=turn.content,
                    ts=brief.date + timedelta(minutes=2 * i),
                )
                for i, turn in enumerate(parsed.turns)
            ]
        except (ValidationError, ValueError) as exc:
            last_error = str(exc)
            messages.append(
                {
                    "role": "user",
                    "content": f"Invalid session ({last_error}). Write it again, obeying every rule.",
                }
            )
    raise RuntimeError(f"could not synthesize session after {_MAX_ATTEMPTS} attempts: {last_error}")


def run_seed(
    briefs: list[SessionBrief],
    *,
    synthesize: Callable[[SessionBrief], list[Turn]],
    transcripts: TranscriptStore,
    repo: NoteRepository,
    segmenter: Segmenter,
    embedder: Embedder,
    index: NoteIndex,
) -> Iterator[str]:
    """Resumable: existing transcripts skip generation; the watermark makes
    re-ingestion a no-op. Crash mid-seed, run again, nothing duplicates."""
    for position, brief in enumerate(briefs, start=1):
        session_id = session_id_for(brief)
        turns = transcripts.read(session_id)
        generated = False
        if not turns:
            turns = synthesize(brief)
            for turn in turns:
                transcripts.append(session_id, turn)
            generated = True
        notes = ingest_session(
            session_id=session_id,
            turns=turns,
            repo=repo,
            segmenter=segmenter,
            created_at=brief.date,
        )
        if notes:
            index_notes(notes, embedder=embedder, index=index)
        status = "generated" if generated else "resumed"
        yield (
            f"[{position}/{len(briefs)}] {brief.date.date()} "
            f"{brief.cluster} ({brief.language.value}): {status}, {len(notes)} notes"
        )
