"""Terminal entry point and composition root.

The only place adapters meet ports. Rendering matches on result type:
the core decides *what* happened, presentation decides *how* to show it.
"""

from __future__ import annotations

import typer
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from second_brain.app.session import SessionRuntime
from second_brain.app.turns import handle_turn
from second_brain.config import get_settings
from second_brain.domain.models import ChatReply, Note, SaveAck, SessionClosed, TurnResult
from second_brain.infra.llm.chat import OpenAIChatResponder
from second_brain.infra.llm.segmenter import OpenAISegmenter
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.store.transcripts import JsonlTranscriptStore
from second_brain.infra.trace.jsonl import JsonlTraceSink

app = typer.Typer(help="Second brain — a personal memory assistant.")
console = Console()

@app.callback()
def main() -> None:
    """Second brain — a personal memory assistant."""
    pass



def _build_runtime() -> SessionRuntime:
    settings = get_settings()
    if settings.openai_api_key is None:
        console.print("[red]OPENAI_API_KEY is not set — add it to .env[/red]")
        raise typer.Exit(code=1)
    client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    return SessionRuntime(
        responder=OpenAIChatResponder(client, settings.chat_model),
        segmenter=OpenAISegmenter(client, settings.segmenter_model),
        repo=MarkdownNoteRepository(settings.notes_dir),
        transcripts=JsonlTranscriptStore(settings.transcripts_dir),
        traces=JsonlTraceSink(settings.traces_dir),
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


@app.command()
def chat() -> None:
    """Open a thinking session. /save ingests now, /quit closes."""
    runtime = _build_runtime()
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


if __name__ == "__main__":
    app()