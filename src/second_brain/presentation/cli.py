"""Terminal entry point and composition root.

The only place adapters meet ports. Rendering matches on result type:
the core decides *what* happened, presentation decides *how* to show it.
"""

from __future__ import annotations
from functools import partial

import typer
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from second_brain.app.ask import answer_question
from second_brain.app.session import SessionRuntime
from second_brain.app.turns import handle_turn
from second_brain.config import Settings, get_settings
from second_brain.domain.models import (
    Answer,
    ChatReply,
    Note,
    SaveAck,
    SessionClosed,
    TurnResult,
)
from second_brain.domain.retrieval import index_notes
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.answerer import OpenAIAnswerer
from second_brain.infra.llm.chat import OpenAIChatResponder
from second_brain.infra.llm.embeddings import OpenAIEmbedder
from second_brain.infra.llm.segmenter import OpenAISegmenter
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink

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
    )


def _saved_lines(notes: list[Note]) -> str:
    if not notes:
        return "Nothing new to save."
    return "\n".join(f"• {note.title}  [dim]({note.id})[/dim]" for note in notes)


def _render(result: TurnResult) -> None:
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


def _render_answer(answer: Answer) -> None:
    if not answer.grounded:
        console.print(
            Panel(
                answer.text or "Nothing in your notes covers this yet.",
                title="not in your notes",
                border_style="yellow",
            )
        )
        return
    console.print()
    console.print(Markdown(answer.text))
    sources = "\n".join(
        f"• {note.title}  [dim]— {note.created_at.date()} · {note.id}[/dim]"
        for note in answer.sources
    )
    console.print(Panel(sources, title="sources", border_style="blue"))


@app.command()
def chat() -> None:
    """Open a thinking session. /save ingests now, /quit closes."""
    settings = get_settings()
    runtime = _build_runtime(settings, _client(settings))
    console.print(
        Panel(
            f"session [bold]{runtime.session_id}[/bold]\n"
            "/save → ingest now · /quit → close",
            title="second brain",
            border_style="cyan",
        )
    )
    try:
        while True:
            raw = console.input("[bold cyan]you ›[/] ")
            if not raw.strip():
                continue
            result = handle_turn(runtime, raw)
            _render(result)
            if isinstance(result, SessionClosed):
                break
    except (KeyboardInterrupt, EOFError):
        # Abrupt exits take the same path as /quit — the crash story
        # and the happy path are one code path.
        console.print()
        _render(SessionClosed(notes=runtime.close()))


@app.command()
def ask(question: str, k: int = typer.Option(5, help="Candidates to retrieve")) -> None:
    """Ask your notes a question — from a fresh process, no session needed."""
    settings = get_settings()
    client = _client(settings)
    answer = answer_question(
        question,
        embedder=OpenAIEmbedder(client, settings.embed_model, settings.embed_dim),
        index=SqliteNoteIndex(settings.index_path, settings.embed_dim),
        repo=MarkdownNoteRepository(settings.notes_dir),
        answerer=OpenAIAnswerer(client, settings.chat_model),
        traces=JsonlTraceSink(settings.traces_dir),
        k=k,
    )
    _render_answer(answer)


@app.command()
def reindex() -> None:
    """Rebuild the derived index from the canonical Markdown store."""
    settings = get_settings()
    client = _client(settings)
    repo = MarkdownNoteRepository(settings.notes_dir)
    index = SqliteNoteIndex(settings.index_path, settings.embed_dim)
    embedder = OpenAIEmbedder(client, settings.embed_model, settings.embed_dim)
    with console.status("reindexing from Markdown…"):
        notes = list(repo.iter_all())
        index.clear()
        index_notes(notes, embedder=embedder, index=index)
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
    )
    for line in progress:
        console.print(line)
    console.print(f"[green]Store now holds {SqliteNoteIndex(settings.index_path, settings.embed_dim).count()} indexed notes.[/green]")

if __name__ == "__main__":
    app()
