"""SQLite derived index: metadata + vectors + FTS5 lexical leg.

Derived and rebuildable: this database can be deleted at any time and
recreated by `sb reindex`. Nothing here is ever an input to write-path
control flow — the Markdown store stays the only source of truth
(decision log #23).

One deliberate exception to "everything is disposable": the enrichment
cache survives `clear()`, because enrichment is the only expensive thing
here to re-derive. Content-hash keying keeps it honest.
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Sequence
from pathlib import Path

import sqlite_vec

from second_brain.domain.contracts import NoteEnrichment
from second_brain.domain.models import Note, SearchHit
from second_brain.domain.retrieval import content_hash


class SqliteNoteIndex:
    """Implements the NoteIndex port over SQLite + sqlite-vec + FTS5."""

    def __init__(self, db_path: Path, dimensions: int) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._dim = dimensions
        self._conn = sqlite3.connect(str(db_path))
        if not hasattr(self._conn, "enable_load_extension"):
            raise RuntimeError(
                "this Python's sqlite3 was built without loadable-extension "
                "support; use a uv-managed interpreter (uv python install 3.12)"
            )
        self._conn.enable_load_extension(True)
        sqlite_vec.load(self._conn)
        self._conn.enable_load_extension(False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._create_schema()
        self._check_dimensions()

    def upsert(
        self, note: Note, embedding: Sequence[float], enrichment: NoteEnrichment
    ) -> None:
        if len(embedding) != self._dim:
            raise ValueError(
                f"embedding has {len(embedding)} dims, index expects {self._dim}"
            )
        with self._conn:
            self._conn.execute(
                """
                INSERT OR REPLACE INTO notes
                  (id, title, created_at, session_id, start_turn, end_turn,
                   language, type, tags, entities, superseded_by, body)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    note.id,
                    note.title,
                    note.created_at.isoformat(),
                    note.source.session_id,
                    note.source.start_turn,
                    note.source.end_turn,
                    note.language.value,
                    note.type.value,
                    json.dumps(note.tags),
                    json.dumps(note.entities),
                    note.superseded_by,
                    note.body,
                ),
            )
            self._conn.execute("DELETE FROM note_vectors WHERE note_id = ?", (note.id,))
            self._conn.execute(
                "INSERT INTO note_vectors (note_id, embedding) VALUES (?, ?)",
                (note.id, sqlite_vec.serialize_float32(list(embedding))),
            )
            self._conn.execute("DELETE FROM notes_fts WHERE note_id = ?", (note.id,))
            self._conn.execute(
                "INSERT INTO notes_fts (note_id, title, body, gist_en, questions)"
                " VALUES (?, ?, ?, ?, ?)",
                (
                    note.id,
                    note.title,
                    note.body,
                    enrichment.gist_en,
                    "\n".join(enrichment.questions),
                ),
            )
            self._conn.execute(
                "INSERT OR REPLACE INTO enrichment_cache"
                " (note_id, content_hash, gist_en, questions) VALUES (?, ?, ?, ?)",
                (
                    note.id,
                    content_hash(note),
                    enrichment.gist_en,
                    json.dumps(enrichment.questions),
                ),
            )

    def cached_enrichment(self, note: Note) -> NoteEnrichment | None:
        row = self._conn.execute(
            "SELECT content_hash, gist_en, questions FROM enrichment_cache"
            " WHERE note_id = ?",
            (note.id,),
        ).fetchone()
        if row is None or row[0] != content_hash(note):
            return None
        return NoteEnrichment(gist_en=row[1], questions=json.loads(row[2]))

    def dense_search(self, query_embedding: Sequence[float], k: int) -> list[SearchHit]:
        total = self.count()
        if total == 0 or k <= 0:
            return []
        rows = self._conn.execute(
            """
            SELECT note_id, distance
            FROM note_vectors
            WHERE embedding MATCH ? AND k = ?
            ORDER BY distance
            """,
            (sqlite_vec.serialize_float32(list(query_embedding)), min(k, total)),
        ).fetchall()
        # OpenAI embeddings are unit-normalized, so L2 distance is
        # rank-equivalent to cosine: similarity = 1 − d²/2 (decision #24).
        return [
            SearchHit(note_id=note_id, score=1.0 - (distance * distance) / 2.0)
            for note_id, distance in rows
        ]

    def lexical_search(self, query: str, k: int) -> list[SearchHit]:
        """BM25 over title, body, English gist, and English questions.

        The query is reduced to quoted OR-terms: recall-biased on purpose —
        RRF and the reranker restore precision downstream. Scores are
        negated bm25 (higher is better) for trace readability; fusion uses
        ranks, never these raw values.
        """
        tokens = re.findall(r"\w+", query, flags=re.UNICODE)
        if not tokens or k <= 0:
            return []
        match_expr = " OR ".join(f'"{token}"' for token in tokens)
        rows = self._conn.execute(
            """
            SELECT note_id, bm25(notes_fts) AS score
            FROM notes_fts
            WHERE notes_fts MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (match_expr, k),
        ).fetchall()
        return [SearchHit(note_id=note_id, score=-score) for note_id, score in rows]

    def count(self) -> int:
        (n,) = self._conn.execute("SELECT COUNT(*) FROM notes").fetchone()
        return int(n)

    def clear(self) -> None:
        """Clears everything rebuildable. The enrichment cache is kept —
        it is the one thing costly to re-derive, and content hashing
        guarantees staleness is impossible."""
        with self._conn:
            self._conn.execute("DELETE FROM notes")
            self._conn.execute("DELETE FROM note_vectors")
            self._conn.execute("DELETE FROM notes_fts")

    def close(self) -> None:
        self._conn.close()

    def _create_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    start_turn INTEGER NOT NULL,
                    end_turn INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    type TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    entities TEXT NOT NULL,
                    superseded_by TEXT,
                    body TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_notes_session"
                " ON notes(session_id, end_turn)"
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_notes_created ON notes(created_at)"
            )
            self._conn.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS note_vectors USING vec0("
                f"note_id TEXT PRIMARY KEY, embedding float[{self._dim}])"
            )
            self._conn.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5("
                "note_id UNINDEXED, title, body, gist_en, questions,"
                " tokenize = 'unicode61 remove_diacritics 2')"
            )
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS enrichment_cache ("
                "note_id TEXT PRIMARY KEY, content_hash TEXT NOT NULL,"
                " gist_en TEXT NOT NULL, questions TEXT NOT NULL)"
            )
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS index_meta"
                " (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            self._conn.execute(
                "INSERT OR IGNORE INTO index_meta (key, value)"
                " VALUES ('dimensions', ?)",
                (str(self._dim),),
            )

    def _check_dimensions(self) -> None:
        row = self._conn.execute(
            "SELECT value FROM index_meta WHERE key = 'dimensions'"
        ).fetchone()
        stored = int(row[0])
        if stored != self._dim:
            raise RuntimeError(
                f"index was built with {stored}-dim embeddings but config now "
                f"says {self._dim} — delete data/index.db and run `sb reindex`"
            )
