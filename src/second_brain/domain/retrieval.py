"""Read-path policy. Born in Phase 2 with a single decision: what text
represents a note in the dense embedding space. The retrieval funnel
(fusion, rerank, gate) grows here in Phase 3.
"""

from __future__ import annotations

from second_brain.domain.models import Note


def embedding_text(note: Note) -> str:
    """Title + body. The title carries the searchable phrasing a future
    query is likely to share; the body carries the substance."""
    return f"{note.title}\n\n{note.body}"
