"""Read-path policy and write-side indexing.

Phase 2 gave this module the dense representation; Phase 3 adds the
enrichment step of the write path. The dense text deliberately does NOT
change with enrichment — keeping it fixed is what lets the eval compare
baseline vs hybrid without confounds.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence

from second_brain.domain.models import Note
from second_brain.domain.ports import Embedder, Enricher, NoteIndex


def embedding_text(note: Note) -> str:
    """Title + body. The title carries the searchable phrasing a future
    query is likely to share; the body carries the substance."""
    return f"{note.title}\n\n{note.body}"


def content_hash(note: Note) -> str:
    """What the enrichment cache keys on: if title+body are unchanged,
    the cached enrichment is still valid."""
    return hashlib.md5(f"{note.title}\n{note.body}".encode("utf-8")).hexdigest()


def index_notes(
    notes: Sequence[Note],
    *,
    enricher: Enricher,
    embedder: Embedder,
    index: NoteIndex,
) -> None:
    """Enrich (cache-first), embed (one batch), upsert.

    Enrichment is the only per-note model call on this path, and the cache
    makes it a one-time cost per note content — `sb reindex` re-pays only
    the embeddings, which arrive in a single batched request.
    """
    if not notes:
        return
    enrichments = [
        index.cached_enrichment(note) or enricher.enrich(note) for note in notes
    ]
    vectors = embedder.embed([embedding_text(note) for note in notes])
    for note, vector, enrichment in zip(notes, vectors, enrichments, strict=True):
        index.upsert(note, vector, enrichment)
