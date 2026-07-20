"""Web search adapter: OpenAI's hosted web_search tool via the Responses API.

No new vendor, no new key — the account already powering chat searches the
web. Provenance is structural: this returns a WebAnswer, presentation
renders it as visibly not-from-notes, and no repository exists anywhere on
this path, so the store cannot be touched by accident.

The tool is FORCED (tool_choice="required") because this route only fires
on an explicit web intent — the user said "search"; a model deciding to
answer from its parameters instead is exactly the failure the live demo
exposed. Instructions carry today's date and forbid clarifying questions.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from openai import OpenAI

from second_brain.domain.models import WebAnswer, WebSource

_INSTRUCTIONS = """\
Today is {today}. You are the web-search arm of a personal assistant.
Search the web and answer strictly from the results.
- Never ask clarifying questions: pick the most reasonable interpretation
  of the request and answer it. If genuinely ambiguous, answer the most
  likely reading and note the assumption in one clause.
- Prefer fresh sources for anything time-sensitive.
- Answer in the language of the request. Lead with the answer; stay concise.
"""


class WebSearchFailure(RuntimeError):
    """The web tool returned nothing usable."""


class OpenAIWebSearcher:
    """Implements the WebSearcher port."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def search(self, question: str) -> WebAnswer:
        response = self._client.responses.create(
            model=self._model,
            tools=[{"type": "web_search"}],  # older SDKs: "web_search_preview"
            tool_choice="required",
            instructions=_INSTRUCTIONS.format(
                today=datetime.now(UTC).date().isoformat()
            ),
            input=question,
        )
        text = getattr(response, "output_text", "") or ""
        if not text.strip():
            raise WebSearchFailure("empty answer from the web tool")
        return WebAnswer(text=text, sources=self._extract_sources(response))

    @staticmethod
    def _extract_sources(response: Any) -> list[WebSource]:
        """Collect url_citation annotations defensively — the Responses
        output shape varies across SDK versions, and a missing title
        should never sink an answer."""
        sources: list[WebSource] = []
        seen: set[str] = set()
        for item in getattr(response, "output", None) or []:
            for part in getattr(item, "content", None) or []:
                for annotation in getattr(part, "annotations", None) or []:
                    if getattr(annotation, "type", "") != "url_citation":
                        continue
                    url = getattr(annotation, "url", "") or ""
                    if url and url not in seen:
                        seen.add(url)
                        title = getattr(annotation, "title", "") or url
                        sources.append(WebSource(title=title, url=url))
        return sources
