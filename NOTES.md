# NOTES.md — what I didn't get to, and what I'd improve

deferred work, and honest edges. DESIGN.md covers the four
required sections;

## Deliberately scoped out (and why)

**The evaluation harness.** Given the time, I prioritized a complete, working
system with orchestration, web search, and voice over a metrics harness. The
consequence is stated plainly in DESIGN.md: the retrieval thresholds
(τ-high / τ-low) and the router confidence floor are arbitrarily configured, not
values calibrated from data, and I report no metrics I haven't measured. The
harness itself is cheap in this architecture, the seeded store already has
planted gold structure (`evals/PLANTED.md`), and the whole system is drivable
offline through its ports — so this is a scope decision under time pressure, not
a design gap. If I had another day it would be the first thing built: recall@5,
MRR, abstention precision/recall, and router accuracy over the planted cases,
then thresholds calibrated from the curve instead of chosen by hand. Building
the system dense-only first (Phase 2) was partly to make this harness produce a
real before/after: dense-only baseline vs hybrid+rerank.

**Proactive recall.** The retrieval funnel already
exists; proactive recall is that funnel run per-turn against a rolling topic
state, behind a gate stack stricter than the Q&A gate: a higher threshold, a
novelty check (don't echo what the user just said), a cooldown between firings,
and a final "would a thoughtful friend interrupt for this?" LLM judge, surfaced
as a side-channel nudge that never hijacks the reply. Happy to discuss it on interview.

## What I'd improve with more time

**Parallelize enrichment on the write path.** A `/save` currently runs
segmentation, then per-note enrichment, then embedding — sequentially. Enrichment
across notes is embarrassingly parallel; a single `asyncio.gather` would cut save
latency to roughly the slowest single note instead of their sum. Writes are off
the interactive path, so this is comfort, not correctness — but it's low-hanging.

**Warm the reranker at startup.** The cross-encoder loads lazily on the first
`ask` (~5–15s one-time). Warming it in a background thread when a `chat` session
opens would overlap the load with the user's first turn of thinking, hiding the
cold start entirely.


**Rolling-window segmentation.** Ingestion segments the whole pending transcript
in one pass, so a session longer than the model's context window would be
truncated. The fix is a rolling "open topics" segmenter that emits notes as the
conversation moves on — and pleasingly, that same rolling topic state is exactly
what proactive recall needs as its query, so the two features share a mechanism.

## Stray observations

**The traces earned their keep immediately.** Building observability from day one
felt like over-investment for a one-week tool — until a double-sigmoid bug
silently disabled the abstention gate (every rerank score squashed to ~0.5, so
nothing ever abstained and everything hedged) and the *only* way it surfaced was
reading the `ask_decided` trace events and noticing the scores clustered
impossibly tight. No test caught it, because the tests didn't know what a
"correct" score distribution looked like. That incident is the whole argument for
principle 3 (every turn leaves a trace).

**Dogfooding the seed corpus stress-tested the write path for free.** `sb seed`
generates synthetic sessions and pushes them through the *real* ingestion
pipeline rather than writing notes directly. That surfaced write-path behavior at
volume (a few hundred notes) that single manual sessions never would have —
segmentation consistency, enrichment cost, filename collisions — and it means the
shipped store is produced the same way a real user's store would be.

**"The model never writes SQL".** The activity route was
the place most tempting to let a model emit a query string. Keeping it to a
filled schema compiled by a pure function means the SQL surface is
unit-testable with zero model calls, prompt injection is structurally impossible, and
the "deterministic vs probabilistic" seam stays clean exactly where it would
otherwise blur.

**Provider portability held up.** Every model sits behind a task-named port with
its provider SDK call in the adapter, so the OpenAI/Groq split (OpenAI for
language and embeddings, Groq for Whisper) is a config concern, not an
architectural one. Swapping either is a one-adapter change, which is also what
makes the whole system testable offline through fakes.
