"""Markdown note store: the canonical layer.

Files are `{ulid}--{slug}.md` with YAML frontmatter. The ULID prefix makes
directory order chronological; the slug keeps the store humanly browsable.
Everything else in the system (SQLite metadata, FTS, vectors) is derived
from these files and rebuildable.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import frontmatter

from second_brain.domain.models import Note


def _slugify(text: str, max_len: int = 60) -> str:
    """Lowercase ASCII slug; accents folded so French titles stay clean."""
    ascii_text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "note"


class MarkdownNoteRepository:
    """Implements the NoteRepository port over a directory of .md files."""

    def __init__(self, notes_dir: Path) -> None:
        self._dir = notes_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def save(self, note: Note) -> None:
        """Upsert: the file is found by id, so re-saving (e.g. setting
        `superseded_by` in a later phase) rewrites in place, never duplicates.
        """
        path = self._path_for(note.id)
        if path is None:
            path = self._dir / f"{note.id}--{_slugify(note.title)}.md"
        meta = note.model_dump(mode="json", exclude={"body"}, exclude_none=True)
        post = frontmatter.Post(note.body, **meta)
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(frontmatter.dumps(post), encoding="utf-8")
        tmp.replace(path)  # atomic: a crash mid-write never tears a note

    def get(self, note_id: str) -> Note | None:
        path = self._path_for(note_id)
        return self._load(path) if path is not None else None

    def iter_all(self) -> Iterator[Note]:
        """Chronological, courtesy of time-sortable ULID filenames."""
        for path in sorted(self._dir.glob("*.md")):
            yield self._load(path)

    def _path_for(self, note_id: str) -> Path | None:
        return next(iter(self._dir.glob(f"{note_id}--*.md")), None)

    @staticmethod
    def _load(path: Path) -> Note:
        post = frontmatter.load(str(path))
        data: dict[str, Any] = {**post.metadata, "body": post.content}
        return Note.model_validate(data)
