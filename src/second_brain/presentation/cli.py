"""Terminal entry point and composition root.

The only place adapters meet ports. Rendering matches on result type:
the core decides *what* happened, presentation decides *how* to show it.
Voice is intercepted here, before the core ever sees the turn — a spoken
turn enters handle_turn as plain text, indistinguishable from typing.
"""

from __future__ import annotations

from functools import partial

import typer
from groq import Groq
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from second_brain.app.ask import answer_question
from second_brain.app.session import SessionRuntime
from second_brain.app.turns import handle_turn
from second_brain.config import Settings, get_settings
from second_brain.domain.contracts import ActivityQueryPlan
from second_brain.domain.models import (
    Abstention,
    ActivityReport,
    Answer,
    AskResult,
    ChatReply,
    HedgedAnswer,
    Note,
    SaveAck,
    SessionClosed,
    TurnResult,
    WebAnswer,
)
from second_brain.domain.retrieval import index_notes
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.answerer import OpenAIAnswerer
from second_brain.infra.llm.chat import OpenAIChatResponder
from second_brain.infra.llm.embeddings import OpenAIEmbedder
from second_brain.infra.llm.enricher import OpenAIEnricher
from second_brain.infra.llm.pivot import OpenAIQueryPivoter
from second_brain.infra.llm.router import OpenAIIntentRouter
from second_brain.infra.llm.segmenter import OpenAISegmenter
from second_brain.infra.rerank.cross_encoder import CrossEncoderReranker
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink
from second_brain.infra.voice.groq_whisper import GroqTranscriber, TranscriptionFailure
from second_brain.infra.web.openai_search import OpenAIWebSearcher
from second_brain.presentation.voice import record_until_enter
from second_brain.seed.generate import run_seed, synthesize_openai
from second_brain.seed.spec import PERSONA, all_briefs

app = typer.Typer(help="Second brain — a personal memory assistant.")
console = Console()


@app.callback()
def main() -> None:
    """Second brain — a personal memory assistant."""


def _client(settings: Settings) -> OpenAI:
    if settings.openai_api_key is None:
        console.print("[red]OPENAI_API_KEY is not set — add it to .env[/red]")
        raise typer.Exit(code=1)
    return OpenAI(api_key=settings.openai_api_key.get_secret_value())


def _build_runtime(settings: Settings, client: OpenAI) -> SessionRuntime:
    return SessionRuntime(
        responder=OpenAIChatResponder(client, settings.chat_model),
        segmenter=OpenAISegmenter(client, settings.segmenter_model),
        repo=MarkdownNoteRepository(settings.notes_dir),
        transcripts=JsonlTranscriptStore(settings.transcripts_dir),
        traces=JsonlTraceSink(settings.traces_dir),
        embedder=OpenAIEmbedder(client, settings.embed_model, settings.embed_dim),
        index=SqliteNoteIndex(settings.index_path, settings.embed_dim),
        enricher=OpenAIEnricher(client, settings.chat_model),
    )


def _saved_lines(notes: list[Note]) -> str:
    if not notes:
        return "Nothing new to save."
    return "\n".join(f"• {note.title}  [dim]({note.id})[/dim]" for note in notes)


def _sources_panel(sources: list[Note]) -> Panel:
    lines = "\n".join(
        f"• {note.title}  [dim]— {note.created_at.date()} · {note.id}[/dim]"
        for note in sources
    )
    return Panel(lines or "—", title="sources", border_style="blue")


def _render_result(result: TurnResult) -> None:
    match result:
        case ChatReply(text=text):
            console.print()
            console.print(Markdown(text))
            console.print()
        case SaveAck(notes=notes):
            console.print(Panel(_saved_lines(notes), title="saved", border_style="green"))
        case SessionClosed(notes=notes):
            console.print(
                Panel(_saved_lines(notes), title="session closed", border_style="green")
            )
        case Answer(text=text, sources=sources):
            console.print()
            console.print(Markdown(text))
            console.print(_sources_panel(sources))
        case HedgedAnswer(text=text, sources=sources, top_score=score):
            console.print(
                Panel(
                    f"[dim]closest match, not a confident answer "
                    f"(relevance {score:.2f})[/dim]\n\n{text}",
                    title="hedged",
                    border_style="yellow",
                )
            )
            console.print(_sources_panel(sources))
        case Abstention(message=message, question=question):
            body = message
            if question:
                body += f'\n\n[dim]try: "search the web for {question}"[/dim]'
            console.print(Panel(body, title="not in your notes", border_style="yellow"))
        case WebAnswer(text=text, sources=sources):
            links = "\n".join(f"• {s.title}  [dim]{s.url}[/dim]" for s in sources)
            body = text + (f"\n\n{links}" if links else "")
            console.print(
                Panel(body, title="from the web — not your notes", border_style="cyan")
            )
        case ActivityReport(caption=caption, notes=notes):
            lines = "\n".join(
                f"• {note.created_at.date()} — {note.title}"
                f"  [dim]({', '.join(note.tags[:3])})[/dim]"
                for note in notes
            )
            console.print(
                Panel(lines or "No notes match.", title=caption, border_style="magenta")
            )


def _activity_caption(plan: ActivityQueryPlan, count: int) -> str:
    window = ""
    if plan.since and plan.until:
        window = f" {plan.since} → {plan.until}"
    elif plan.since:
        window = f" since {plan.since}"
    elif plan.until:
        window = f" until {plan.until}"
    filters = ", ".join(plan.tags + plan.entities)
    scope = f" · {filters}" if filters else ""
    return f"activity{window}{scope} — {count} notes"


@app.command()
def chat() -> None:
    """Open a thinking session. /save ingests, /voice speaks, /quit closes."""
    settings = get_settings()
    client = _client(settings)
    runtime = _build_runtime(settings, client)
    repo = MarkdownNoteRepository(settings.notes_dir)
    index = SqliteNoteIndex(settings.index_path, settings.embed_dim)
    embedder = OpenAIEmbedder(client, settings.embed_model, settings.embed_dim)
    traces = JsonlTraceSink(settings.traces_dir)

    transcriber: GroqTranscriber | None = None
    if settings.groq_api_key is not None:
        transcriber = GroqTranscriber(
            Groq(api_key=settings.groq_api_key.get_secret_value()),
            settings.voice_model,
        )

    def ask_fn(question: str, pivot: str | None) -> AskResult:
        return answer_question(
            question,
            embedder=embedder,
            index=index,
            repo=repo,
            answerer=OpenAIAnswerer(client, settings.chat_model),
            reranker=CrossEncoderReranker(settings.rerank_model),
            pivoter=OpenAIQueryPivoter(client, settings.chat_model),
            traces=traces,
            rerank_top=settings.rerank_top,
            answer_top=settings.answer_top,
            tau_high=settings.tau_high,
            tau_low=settings.tau_low,
            pivot=pivot,
            trace_session=runtime.session_id,
        )

    def activity_fn(plan: ActivityQueryPlan) -> ActivityReport:
        ids = index.activity_search(plan)
        notes = [note for note_id in ids if (note := repo.get(note_id)) is not None]
        return ActivityReport(caption=_activity_caption(plan, len(notes)), notes=notes)

    searcher = OpenAIWebSearcher(client, settings.chat_model)
    dispatch = partial(
        handle_turn,
        router=OpenAIIntentRouter(client, settings.chat_model),
        ask=ask_fn,
        activity=activity_fn,
        web=searcher.search,
        confidence_floor=settings.router_confidence_floor,
    )

    console.print(
        Panel(
            f"session [bold]{runtime.session_id}[/bold]\n"
            "/save → ingest now · /voice → speak · /quit → close",
            title="second brain",
            border_style="cyan",
        )
    )
    try:
        while True:
            raw = console.input("[bold cyan]you ›[/] ")
            if raw.strip().lower() == "/voice":
                if transcriber is None:
                    console.print("[red]GROQ_API_KEY not set — voice needs it in .env[/red]")
                    continue
                console.print("[dim]recording… press Enter to stop[/dim]")
                try:
                    raw = transcriber.transcribe(record_until_enter())
                except TranscriptionFailure:
                    console.print("[yellow]heard nothing — try again[/yellow]")
                    continue
                except Exception as exc:  # noqa: BLE001 — a mic problem must not kill the session
                    console.print(f"[red]voice capture failed: {exc}[/red]")
                    continue
                console.print(f"[bold cyan]you (voice) ›[/] {raw}")
            if not raw.strip():
                continue
            results = dispatch(runtime, raw)
            for result in results:
                _render_result(result)
            if any(isinstance(r, SessionClosed) for r in results):
                break
    except (KeyboardInterrupt, EOFError):
        # Abrupt exits take the same path as /quit — the crash story
        # and the happy path are one code path.
        console.print()
        _render_result(SessionClosed(notes=runtime.close()))


@app.command()
def ask(question: str) -> None:
    """Ask your notes a question — full funnel: hybrid, reranked, gated."""
    settings = get_settings()
    client = _client(settings)
    result = answer_question(
        question,
        embedder=OpenAIEmbedder(client, settings.embed_model, settings.embed_dim),
        index=SqliteNoteIndex(settings.index_path, settings.embed_dim),
        repo=MarkdownNoteRepository(settings.notes_dir),
        answerer=OpenAIAnswerer(client, settings.chat_model),
        reranker=CrossEncoderReranker(settings.rerank_model),
        pivoter=OpenAIQueryPivoter(client, settings.chat_model),
        traces=JsonlTraceSink(settings.traces_dir),
        rerank_top=settings.rerank_top,
        answer_top=settings.answer_top,
        tau_high=settings.tau_high,
        tau_low=settings.tau_low,
    )
    _render_result(result)


@app.command()
def reindex() -> None:
    """Rebuild the derived index from the canonical Markdown store."""
    settings = get_settings()
    client = _client(settings)
    repo = MarkdownNoteRepository(settings.notes_dir)
    index = SqliteNoteIndex(settings.index_path, settings.embed_dim)
    embedder = OpenAIEmbedder(client, settings.embed_model, settings.embed_dim)
    enricher = OpenAIEnricher(client, settings.chat_model)
    with console.status("reindexing from Markdown…"):
        notes = list(repo.iter_all())
        index.clear()
        index_notes(notes, enricher=enricher, embedder=embedder, index=index)
    console.print(f"[green]Reindexed {len(notes)} notes.[/green]")


@app.command()
def seed(limit: int = typer.Option(0, help="Only the first N sessions (0 = all)")) -> None:
    """Populate the store with the synthetic persona — through real ingestion."""
    settings = get_settings()
    client = _client(settings)
    briefs = all_briefs()
    if limit:
        briefs = briefs[:limit]
    progress = run_seed(
        briefs,
        synthesize=partial(synthesize_openai, client, settings.chat_model, PERSONA),
        transcripts=JsonlTranscriptStore(settings.transcripts_dir),
        repo=MarkdownNoteRepository(settings.notes_dir),
        segmenter=OpenAISegmenter(client, settings.segmenter_model),
        embedder=OpenAIEmbedder(client, settings.embed_model, settings.embed_dim),
        index=SqliteNoteIndex(settings.index_path, settings.embed_dim),
        enricher=OpenAIEnricher(client, settings.chat_model),
    )
    for line in progress:
        console.print(line)
    total = SqliteNoteIndex(settings.index_path, settings.embed_dim).count()
    console.print(f"[green]Store now holds {total} indexed notes.[/green]")


if __name__ == "__main__":
    app()
