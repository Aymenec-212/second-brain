# Second Brain

A personal memory assistant. You hold open-ended conversations with it to think
through ideas; each session is distilled to a store of Markdown notes. Later
sessions carry no conversation history — they answer questions from the
accumulated notes, report on your activity, and reach the web when the notes
come up empty.

- **`DESIGN.md`** — the architecture, how I know it works, the decisions and
  trade-offs (including what didn't work), and where it breaks first. Start here
  for the thinking.
- **`ARCHITECTURE.md`** — component diagrams and the deterministic/probabilistic
  seam.
- **`NOTES.md`** — deferred work and what I'd improve with more time.

The repository ships with a **seeded store already in `data/`** (a synthetic
persona's ~6 months of bilingual EN/FR sessions), so you can query it
immediately without generating anything.

---

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)** — the Python package manager.
  Install: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux).
- **Python 3.12** — uv will fetch it if you don't have it (`uv python install
  3.12`). 3.12 specifically; the reranker's torch stack is friction-free there.
- **An OpenAI API key** — required. Powers chat, segmentation, enrichment,
  routing, answering, embeddings, and web search.
- **A Groq API key** — optional. Only needed for voice input (Whisper).

---

## Setup

```bash
# 1. Install dependencies into a local virtualenv (reads uv.lock)
uv sync

# 2. Provide your API key(s)
cp .env.example .env
# then edit .env and set:
#   OPENAI_API_KEY=sk-...
#   GROQ_API_KEY=gsk_...      # optional, only for voice
```

That's it. `uv sync` installs everything, including the local cross-encoder
reranker's dependencies (torch + sentence-transformers).

> **First-run note:** the very first `sb ask` downloads the reranker model
> (`bge-reranker-v2-m3`, ~2.3 GB, one time) and loads it into memory (~5–15s).
> Subsequent calls are fast. This cold start is discussed in DESIGN.md under
> latency — it's a one-time model load, not per-query cost.

---

## Quick start — query the seeded store

The store is already populated, so you can ask it things right away. Every
example below has a real answer planted in the seed corpus (see
`evals/PLANTED.md` for the map).

```bash
# A cross-lingual question — the notes are in French, the answer comes in English
uv run sb ask "what's my apartment budget?"

# A decision that was reversed months later — the newer one wins, and it says so
uv run sb ask "which mobile framework am I using for Cairn?"

# An activity question — answered by SQL over metadata, not vector search
uv run sb ask "what did I work on in June?"

# Something never written down — it abstains instead of guessing, and offers the web
uv run sb ask "do my notes say anything about scuba diving?"
```

---

## Commands

```bash
uv run sb chat        # open a thinking session (see below)
uv run sb ask "..."   # ask the notes a question, from a fresh process
uv run sb reindex     # rebuild the SQLite index from the Markdown notes
uv run sb seed        # (re)generate the synthetic store — see below
```

### `sb chat` — a thinking session

Type to converse. The assistant is a thinking partner, not just a Q&A bot.
Inside a session:

- **`/save`** — distill the conversation so far into notes now.
- **`/voice`** — speak instead of type (needs `GROQ_API_KEY`). Press Enter to
  stop recording. Handles English, French, and code-switching.
- **`/quit`** — close the session (ingests anything not yet saved).

You don't have to use `/save` — closing the session ingests automatically. You
can also just say things in natural language: *"save that"*, *"what did I decide
about X?"*, *"what did I work on last week?"*, or *"search the web for ..."* —
the system routes each turn to the right action.

> A session becomes notes at close (or on `/save`). Ctrl-C also ingests cleanly
> — an abrupt exit still saves your thinking.

### `sb ask` — one-shot questions

Answers from the notes with citations, hedges when retrieval is weak, and
abstains (rather than hallucinating) when the notes don't cover the topic —
offering a web search as a fallback.

### `sb reindex` — rebuild the derived index

The Markdown notes in `data/notes/` are the source of truth; the SQLite index is
derived and rebuildable. If you ever delete `data/index.db`, this reconstructs it
from the notes. (It re-embeds via OpenAI, but reuses a cached enrichment, so it's
cheap on a store that's already been enriched once.)

### `sb seed` — regenerate the store (optional)

The store ships pre-seeded, so **you don't need this to try the system.** If you
want to regenerate it from scratch (it uses your OpenAI key and costs a few
dollars with `gpt-5-mini`, a few minutes):

```bash
uv run sb seed --limit 3     # generate just 3 sessions first, to sanity-check
uv run sb seed               # the full corpus (~60 sessions)
```

`seed` is resumable — re-running skips sessions already generated, so a crash
mid-run is safe to restart.

---

## Where things live

```
data/
  notes/          canonical Markdown notes ({ulid}--{slug}.md) — the source of truth
  transcripts/    append-only JSONL, one file per session
  traces/         JSONL observability — one file per session/ask, every step recorded
  index.db        derived SQLite (vectors + FTS + metadata) — rebuildable via reindex
```

To see ingestion working end to end: read a raw session in `data/transcripts/`,
then the distilled notes it produced in `data/notes/`. To see the retrieval
funnel's decisions, open a file in `data/traces/` after an `sb ask` — each turn
records both retrieval legs with scores, the fused order, every rerank score, and
the gate decision.

---


## Troubleshooting

- **`OPENAI_API_KEY is not set`** — copy `.env.example` to `.env` and add your
  key.
- **First `sb ask` hangs for ~10s** — expected; it's the one-time reranker model
  download and load. Subsequent calls are fast.
- **`/voice` says the key is missing** — voice needs `GROQ_API_KEY` in `.env`;
  everything else works without it.
- **Dimension-mismatch error on startup** — if you changed the embedding
  dimension after building the index, delete `data/index.db` and run
  `uv run sb reindex`.
- **A `sqlite3` loadable-extension error** — use a uv-managed interpreter
  (`uv python install 3.12`); some system Pythons are built without extension
  support, which `sqlite-vec` needs.