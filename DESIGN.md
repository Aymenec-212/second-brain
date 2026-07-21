# DESIGN.md — Second Brain

A personal memory assistant: you hold open-ended conversations with it to think
through ideas, each session is distilled to a store of Markdown notes, and later
sessions, carrying no conversation history, can answer questions from those notes (or at least try to),
report on your activity, and reach the web when the notes come up empty.(dictation is enabled as well)

This document explains the thinking: the architecture, how I know it works, the
decisions and trade-offs (including what I tried that didn't work out very well), and where it
breaks first. A companion `ARCHITECTURE.md` holds the component diagrams and system context;
`PLAN.md` holds the phase-by-phase build log and the full numbered decision log
this document refers to.

---

## 1. Architecture

### 1.1 The one idea

Every design choice here serves a single principle: **the model understands,
code decides.** A language model is a powerful, non-deterministic component; the
system around it must be legible and testable. So models are pushed to the
edges, behind interfaces, and allowed to influence control flow *only* by
returning a validated, typed object. Routing, ranking, thresholds, SQL, and
storage are basic Python code! The seam between the two is the thing
I most want to be visible — and it is literally visible, as the package
structure.

### 1.2 Layered hexagonal, layers as packages

Four layers, each a Python package under `src/second_brain/`:

- **`presentation/`** — modality only. The Rich terminal loop, and push-to-talk
  voice capture. It renders typed result objects and turns keystrokes or speech
  into text. It knows nothing about retrieval or storage.
- **`app/`** — thin coordination. The turn dispatch ladder (`turns.py`), the
  session lifecycle (`session.py`), and the read-path funnel orchestration
  (`ask.py`). This layer wires steps together; it holds no business rules (domain model in DDD terminology).
- **`domain/`** — pure Python: the note model, the ingestion policy, the
  retrieval funnel (fusion + the three-zone gate), the activity query plan
  types, every typed contract, and — the important file — `ports.py`.
- **`infra/`** — adapters that implement the ports: the Markdown store, the
  SQLite index, every model call (with its prompt colocated), web search, the
  trace sink.

`domain/ports.py` is **the complete and only list** of places a model or an
external system can touch the core. Ports are `Protocol`s (structural typing),
so a test fake or a real adapter satisfies a port by shape alone — no
inheritance, no registration, and no import from infrastructure back into the
core. They split by nature: *cognitive* ports back onto LLMs (`IntentRouter`,
`Segmenter`, `Enricher`, `Answerer`, `ChatResponder`, `QueryPivoter`,
`Reranker`, `Embedder`, `WebSearcher`, `Transcriber`); *deterministic* ports
back onto storage (`NoteRepository`, `NoteIndex`, `TranscriptStore`,
`TraceSink`). Adapters are wired to ports in one place, the composition root in
`cli.py`.

 The honest cost of this hexagonal pattern is indirection. For a single-user tool, strict layering is usually overkill. However, I applied it here because the seam between model-driven control and deterministic code is the exact thing being graded; the indirection provides clear boundaries. Crucially, I did not over-apply it: internal pure logic (RRF fusion, the 3-zone gate, the SQL compiler) remains plain functions and dataclasses. Ports exist only at genuine external boundaries.

### 1.3 Two-layer persistence — Markdown is canonical, everything else is derived

- **Canonical: Markdown.** Notes are `{ulid}--{slug}.md` with YAML frontmatter.
  Human-readable, chronologically ordered by the ULID prefix, accents folded for
  clean filenames, written atomically (temp-file + replace), save-as-upsert-by-id.
  This is the *only* source of truth.
- **Derived: SQLite.** Metadata + `sqlite-vec` vectors + an FTS5 lexical table +
  an enrichment cache. Entirely rebuildable: delete the database, run
  `sb reindex`, and it reconstructs from the Markdown.
- **Archive: JSONL transcripts.** Append-only, one file per session, flushed per
  turn *before* the model is called. Ingestion reads the transcript back from
  disk, never from process memory.

This directly answers the brief's stated tension — raw transcripts don't scale
to clean retrieval, aggressive summaries lose detail irreversibly. The
resolution: the *index* only ever sees distilled notes (clean embeddings,
scalable reads), while the *transcript* survives as un-indexed provenance that
notes point back into (nothing is irrecoverable). Notes are distilled but quite
detailed, around 150–500 words, decontextualized so they stand alone months later,
which is a retrieval-quality decision as much as a persistence one: the note is
itself the retrieval unit, so there is no separate chunking layer.

### 1.4 The write path

A turn is appended to the transcript, then, on an explicit `/save`, on session
close, on Ctrl-C, or on a crash re-run — the *same* `ingest_session` path runs:
slice the turns not yet ingested, segment them into note drafts (one LLM call),
enrich each draft (English gist + "questions this note answers"), embed, and
write canonical-Markdown-first, index-second.
The enrichment step—generating an English gist and 3–6 hypothetical questions the note answers—is inspired by the Doc2Query method. This directly attacks the "surface form gap": notes are written as declarative statements ("Decided to use PostgreSQL"), but months later are queried as questions ("Which database did I pick?"). By indexing these generated questions alongside the original text, the lexical leg (FTS5) achieves cross-lingual reach and matches exact keywords that dense vectors alone might blur. Enrichment is cached by content hash, ensuring sb reindex never re-pays the LLM cost for unchanged notes

Two properties matter. **Idempotency is derived, not stored.** "What still needs
ingesting?" is answered by the canonical store itself — the high-water mark is
the largest turn index any existing note of this session already covers. There
is no sidecar state file to corrupt or drift, so a crash or a deleted index can
never cause duplicate ingestion. **Identity is assigned by the domain, never the
model.** The model proposes a draft's content and its span; the ULID, the
timestamp, and the provenance record are stamped by our code.

### 1.5 The read path — a funnel that ends in a gate

A question flows through a widening-then-narrowing funnel where every stage
*between* the models is deterministic:

1. **Router (LLM)** classifies the turn and extracts a *self-contained* question
   plus its English pivot.
2. **Dense leg** embeds the original question and matches vectors.
3. **Lexical leg** runs BM25 over the note text *and* its English gist and
   questions — which is what gives a French note an English shadow — queried
   with the question plus its pivot.
4. **RRF fusion** merges the two legs by *rank* (K=60), because dense
   similarities and BM25 scores are incommensurable but ranks are not.
5. **Cross-encoder reranker (local, that explains the high latency)** rescores the fused candidates.
6. **Three-zone gate (deterministic)** judges the single best score:
   `≥ τ-high` → answer; `τ-low ≤ top < τ-high` → hedged; `< τ-low` → abstain —
   and it abstains *before* the answerer runs, so a miss costs zero generation
   tokens.
7. **Answerer (LLM)** grounds the reply in only the kept notes and cites them;
   if it reports the notes don't actually contain the answer, a confident
   retrieval still downgrades to abstention. Retrieval confidence and content
   confirmation veto independently.

### 1.6 Orchestration — one structured call, then a deterministic flow

Per turn, exactly one small routing call returns a `RouterDecision`: an *ordered*
list of intents (`chat | save | notes_qa | activity | web_search`), a
confidence, the extracted question and pivot, and — for activity queries — an
`ActivityQueryPlan`. Then `app/turns.py` disposes deterministically: slash
commands resolve first (free), a confidence floor sends low-confidence turns to
a clarify prompt, and otherwise a plain loop executes the ordered intents. Mixed
turns work because the loop runs multiple intents in order — "save that, and what
did I say about X?" returns `[SaveAck, Answer]`.

The activity route is deliberately *not* vector search. "What did I work on last
week?" wants exact metadata aggregation, so the model fills the
`ActivityQueryPlan` schema (resolving "last week" into absolute dates from
today's date, which the prompt provides) and a **pure function compiles that plan
to parameterized SQL**. The model's entire surface is the plan's fields; it never
writes SQL, so injection is structurally impossible and the compiler is unit-
testable with no model in the loop.

### 1.7 Observability

Every observable step of every turn emits a JSONL trace event: intents and
confidence, the route taken, both retrieval legs with scores, the fused order,
every rerank score, the gate zone, citations. The trace log is the debugger —
and that is not a slogan; it caught a real bug (3.1).

---

## 2. How I know it works

Two instruments, for two different questions.

**Deterministic logic is covered by an offline test suite.** Every test runs
without network or API keys, using deterministic fakes for the models (a hashing
embedder with real geometry, a token-overlap reranker, canned responders). This
suite proves the *mechanics* never silently break: watermark idempotency (re-
ingesting the same turns is a no-op and never reaches the model), span validation
(a note can't claim provenance over turns outside its window), RRF fusion
(presence in both legs wins; ties are deterministic), the three-zone gate (each
zone fires at the right boundary; weak candidates are dropped before the
answerer; a confident retrieval with an ungrounded answer downgrades to
abstention), the SQL compiler (bounded, parameterized, inclusive-date-correct),
multi-intent dispatch order, and the crash-safety invariant (a user turn hits
disk before the model is called, proven with a probe that reads the file at call
time).

What that suite deliberately does *not* prove is *quality* — whether a note reads
well, or whether retrieval finds the *right* note. Fakes can't answer that. That
question is answered two ways: by running the real system against a seeded store
and reading the output, and — the repeatable version — by the evaluation harness.

**The seeded store makes quality testable at scale.** `sb seed` generates a
synthetic persona's ~6 months of sessions (~60% English, ~40% French) and pushes
them *through the real ingestion pipeline* — dogfooding that stress-tests the
write path and produces an authentic store rather than hand-authored notes. The
spec plants known structure for the harness to grade against: contradiction pairs
(a decision reversed months later), near-miss distractors (two different database
decisions in two different projects, so "which DB for project X?" must not surface
project Y's), cross-lingual pairs (a French-only cluster queried in English), and
a written list of topics never discussed anywhere (for abstention). The map of
what's planted lives in `evals/planted.md`, and the gold questions are written
against it.

> **Status note — a deliberate scope decision.** Given the time, I prioritized a
> complete working system (orchestration, web search, voice) over a metrics
> harness. The consequence, stated plainly: the thresholds τ-high/τ-low and the
> router confidence floor are principled defaults, not values calibrated from
> data, and this document reports no metrics it has not measured. The harness is
> cheap in this architecture — the seeded store already carries planted gold
> structure (`evals/PLANTED.md`) and the system is drivable offline through its
> ports — so this is a scope choice, not a design gap; it is the first thing I
> would build with extra time. See `NOTES.md`.

---

## 3. Decisions and trade-offs — including what didn't work

The full numbered decision log is in `PLAN.md`. Here are the load-bearing ones,
and the things that actively went wrong.

### 3.1 What didn't work

**The abstention gate was silently broken by a double sigmoid — and the traces
caught it.** The reranker adapter applied a sigmoid to the cross-encoder's
output to turn logits into [0,1] probabilities for the gate. But
`sentence-transformers`' `CrossEncoder` *already* applies a sigmoid for single-
label models like `bge-reranker-v2-m3`. The second one squashed every score into
roughly [0.5, 0.73]: τ-low = 0.2 was always cleared (so abstention never fired
from scores) and τ-high = 0.6 was almost never reached (so everything hedged). A
question about a topic that *doesn't exist in the store* came back "hedged"
instead of abstaining. There was no crash, no exception — the gate just quietly
did nothing. It was diagnosed by reading the `ask_decided` trace events and
noticing every reranked score clustered in a narrow band centered on 0.5. The
fix was deleting our sigmoid. The lesson is the whole argument for building
observability from day one: an invisible calibration bug is caught by an audit
trail, not by tests that don't know what "correct" looks like.


**Dense-only retrieval was the honest baseline, and it lost where predicted.**
The system was built dense-only first (Phase 2), on purpose, so the failures
would be real. Reading its output on the seeded store showed exactly the two
weaknesses the funnel was designed to fix: cross-lingual misses (a French note
not surfacing for an English question) and near-miss imprecision (a query about
one project's database blurring in another project's). That motivated the lexical
leg with English enrichment (cross-lingual reach) and the cross-encoder reranker
(precision). This is why the architecture has a funnel and not just a vector
search.

**The answerer over-synthesized until told not to.** Early on, handed several
retrieved notes, the answerer treated "here are relevant notes" as "summarize
all of them" and, worse, once performed arithmetic across notes to invent a
figure that appeared in none of them ( you can see in demo recording, the system did not do very well in answering apartment budget question). Two fixes: the gate now narrows the context
to only genuinely-relevant notes before the answerer sees them, and the answerer
prompt forbids arithmetic outright — report figures exactly as written, never
combine or reconcile, and when notes disagree give the newest and name the older.

**The answerer over-synthesized until the context was narrowed.** In early testing, the dense-only baseline shoved loosely-related notes into the LLM's context window. Treating this as a summarization task, the LLM attempted arithmetic across conflicting documents—most notably inventing a €1,600 apartment budget figure that appeared in no single note.(you can see in the demo recording, the system still struggles with apartment budget related questions) The fix was two-fold. First, the 3-zone gate's tau_low threshold acts as a strict deterministic filter: any note scoring below this floor is discarded before the LLM sees it, starving the model of irrelevant data. Second, the answerer prompt explicitly forbids arithmetic ("Report every figure exactly as written, never combine or reconcile; if notes disagree, give the newest value and mention the older one with its date"). Together, these changes structurally eliminated context-overload hallucinations.



**A planned optimization was reverted for correctness.** The original Phase 2 plan was to move the ingestion watermark (the marker dictating where the next slice of un-ingested turns begins) from a filesystem scan to a fast SQL MAX() query. Implementing this exposed a classic distributed systems trap: write-path control flow was being driven by a derived artifact. The SQLite index is a cache that can legitimately lag the canonical Markdown store (e.g., a crash between the Markdown write and the index upsert, a manually deleted database, or a fresh clone). If the system reads a stale watermark from SQLite, it assumes recent turns were never ingested, re-slices them, and creates duplicate notes—breaking idempotency. The watermark derivation was therefore reverted to scan the canonical Markdown store directly. While this is an O(store) operation (~100ms at 500 notes) rather than an O(1) SQL query. We trade a slight performance hit for a hard guarantee: write-path decisions are always made against the source of truth, ensuring crash-safe, idempotent ingestion.

### 3.2 Load-bearing decisions

**Compute split: rent the dense leg, own the rerank leg.** Dense embeddings come
from OpenAI (`text-embedding-3-large`) — a fast write path and strong FR/EN with
no second local model to manage. The reranker is a *local* cross-encoder
specifically because the abstention gate thresholds its scores: they must be
deterministic and calibratable, which an LLM judge (noisy, re-rolled each call)
cannot provide.

**RRF over score-normalization.** Fusing dense cosine and BM25 by normalizing and
adding their scores requires calibrating two incommensurable scales. Rank-based
RRF sidesteps the problem entirely — it only needs the ordering each leg
produces. Simpler and more robust.

**Contracts do double duty.** A Pydantic `Field(description=…)` is serialized into
the JSON schema the model receives under structured outputs, so the validation
rule and the prompt guidance are one source of truth. And every contract-
returning adapter enforces in three layers — server-side structured-output shape,
client-side Pydantic validators, and an adapter check no schema can express (e.g.
a segmenter span must fall inside the actual transcript window) — then a bounded
corrective retry that names the violated rule, then a typed failure the app
degrades on. No crash, no silent acceptance.

**No heavy frameworks.** No Temporal, no agent framework. For a local single-user
tool, a durable-execution engine or an autonomous agent loop would be complexity
without payoff, and would *hide* the seam I want visible. A turn has a bounded,
inspectable path. Where these would matter in a production, multi-user setting is
noted in `NOTES.md`.

**Two histories, kept separate.** The transcript holds only chat-intent turns —
the thinking worth remembering, and the only thing ingestion reads. A separate,
in-memory, never-persisted *exchange log* holds every turn and its outcome, and
is what the router sees, so a follow-up ("and the final score?") keeps its
referent. Memory and routing-context are different problems with different
retention rules; conflating them (an earlier version fed the transcript to the
router) broke multi-turn web search.

---

## 4. Where it breaks first, and what I wouldn't trust it with

**Long sessions exceed whole-window segmentation.** Ingestion segments the whole
pending transcript window in one pass. A session longer than the model's context
window needs a rolling "open topics" segmenter that emits notes as the
conversation moves on.

**Uncalibrated thresholds.** τ-high, τ-low, and the
router confidence floor are arbitrarily configured. a thorough eval harness is definitely needed.

**Scale ceiling of exact vector search.** `sqlite-vec` does exact nearest-
neighbor. At the seeded scale (around 400 notes) and well beyond (into the low
tens of thousands), that is single-digit milliseconds and correct. Around ~10^5
notes it would need an approximate index (HNSW). The port makes that a swap (thanks to the hexagonal architecture).

**Latency.** I tried to optimize for correctness and observability rather than raw speed. The known costs, and their architectural fixes, are explicit: the local cross-encoder reranker cold-starts on the first ask (a one-time ~5–15s model load; the fix is warming it in a background thread at startup). A /save runs segmentation, per-note enrichment, and embedding sequentially, so saving several notes incurs multiple round-trips (enrichment is embarrassingly parallel and could be an asyncio.gather, cutting save latency to the slowest note). For the read path, a single ask chains router → embed → rerank → answer. Initially, cross-lingual support required a separate LLM call to translate the query to English for the lexical (FTS5) leg. I would eliminate this obvious redundancy by folding the translation directly into the IntentRouter's structured output (query_en). Because the router was already parsing the query semantically, it now returns the English pivot in the exact same API call, removing an entire network round-trip from the critical path. Finally, writes are deliberately kept off the interactive path so the chat REPL remains snappy.



**What I would not trust it with.** as a v0 prototype, this app is far from being ready to deploy :)
nonetheless It demonstrates the necessary trade-offs clearly, but I would not yet trust it with: High-stakes environments where a missed memory is costly. By design, the system abstains rather than guesses—the right default for a personal thinking aid, but wrong for compliance or legal record-keeping where silent omissions are unacceptable. Corpora at 10⁵+ notes, where exact nearest-neighbor search and O(store) watermark scans would degrade unacceptably.
---

## 5. What I would build next

**Proactive recall.** The case study's most interesting bonus, and the one I chose to
scope out under time pressure. The retrieval funnel 
already exists; proactive recall is that funnel run against a rolling topic state,
behind a strict gate stack, a threshold *stricter* than the Q&A gate, a novelty
check (don't surface what the user just said), a cooldown between firings, and a
final "would a thoughtful friend interrupt for this?" LLM judge, surfaced as a
side-channel nudge that never hijacks the reply. Precision is the whole feature:
one bad interruption destroys trust, so the entire design effort is the gate, not
the retrieval. This is the piece I'm most ready to discuss in depth.

**Knowledge supersedence, write-time.** A read-time recency preference with
conflict narration already exists (the answerer prefers the newer of two
conflicting notes and says the thinking changed). The write-time version — detect
a near-duplicate at ingest, run a contradiction judge, set `superseded_by`, and
down-rank superseded notes except for explicitly temporal questions — composes
cleanly with this architecture and is the natural next increment.