"""Ingestion policy: how a session's transcript becomes notes.

Pure domain logic over ports. The idempotency rule — "what still needs
ingesting?" — is derived from the store itself: the high-water mark is the
largest turn index any existing note of this session already covers. There
is no separate state file to corrupt or drift; the notes are the record.

Mid-session /save, session close, and a re-run after a crash all take the
same path through ingest_session, which is a no-op when nothing is pending.
"""

from __future__ import annotations

from collections.abc import Sequence

from second_brain.domain.contracts import NoteDraft
from second_brain.domain.models import Note, Role, SourceSpan, Turn
from second_brain.domain.ports import NoteRepository, Segmenter


def ingested_watermark(repo: NoteRepository, session_id: str) -> int:
    """Highest turn index already covered by saved notes; -1 if none.

    Full-store scan for now — acceptable at hundreds of Markdown files.
    Phase 2's SQLite index turns this into `SELECT MAX(end_turn) WHERE
    session_id = ?`.
    """
    ends = [
        note.source.end_turn
        for note in repo.iter_all()
        if note.source.session_id == session_id
    ]
    return max(ends, default=-1)


def materialize(draft: NoteDraft, session_id: str) -> Note:
    """Draft → Note. Identity (id, created_at) and provenance (SourceSpan)
    are assigned here, by the domain — never by the model."""
    return Note(
        title=draft.title,
        language=draft.language,
        type=draft.type,
        tags=draft.tags,
        entities=draft.entities,
        source=SourceSpan(
            session_id=session_id,
            start_turn=draft.start_turn,
            end_turn=draft.end_turn,
        ),
        body=draft.body,
    )


def ingest_session(
    *,
    session_id: str,
    turns: Sequence[Turn],
    repo: NoteRepository,
    segmenter: Segmenter,
) -> list[Note]:
    """Segment and persist everything not yet ingested; return the new notes.

    Notes are saved in ascending end_turn order so that, under a partial
    failure, the derived watermark stays consistent with what is actually
    on disk and a re-run resumes cleanly.
    """
    watermark = ingested_watermark(repo, session_id)
    pending = [t for t in turns if t.index > watermark]
    if not pending:
        return []
    if not any(t.role is Role.USER for t in pending):
        # A trailing assistant-only remainder holds nothing of the user's
        # thinking; skip the segmenter call entirely.
        return []
    drafts = segmenter.segment(pending)
    notes = sorted(
        (materialize(d, session_id) for d in drafts),
        key=lambda n: n.source.end_turn,
    )
    for note in notes:
        repo.save(note)
    return notes
