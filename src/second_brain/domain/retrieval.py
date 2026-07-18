"""Read-path policy and write-side indexing.

Phase 2: what text represents a note in the dense space, and how a batch
of notes enters the index. The retrieval funnel (lexical leg, fusion,
rerank, gate) grows here in Phase 3.
"""

from __future__ import annotations

from collections.abc import Sequence

from second_brain.domain.models import Note
from second_brain.domain.ports import Embedder, NoteIndex


def embedding_text(note: Note) -> str:
    """Title + body. The title carries the searchable phrasing a future
    query is likely to share; the body carries the substance."""
    return f"{note.title}\n\n{note.body}"


def index_notes(notes: Sequence[Note], *, embedder: Embedder, index: NoteIndex) -> None:
    """Embed and upsert a batch of notes. One embedding request per batch,
    not per note — seed and reindex push hundreds through here."""
    if not notes:
        return
    vectors = embedder.embed([embedding_text(note) for note in notes])
    for note, vector in zip(notes, vectors, strict=True):
        index.upsert(note, vector)
