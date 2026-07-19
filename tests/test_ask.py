"""Funnel and ask-pipeline tests — deliberately lean, fully offline.

Pure pieces (RRF, gate) are tested directly; the pipeline is tested for
its deterministic dispatch rules with a token-overlap FakeReranker. Answer
quality belongs to the real system and the Phase 3 eval harness.
"""

from collections.abc import Sequence
from pathlib import Path

import pytest

from second_brain.app.ask import answer_question
from second_brain.domain.contracts import AnswerDraft
from second_brain.domain.models import (
    Abstention,
    Answer,
    HedgedAnswer,
    Language,
    Note,
    NoteType,
    SearchHit,
    SourceSpan,
)
from second_brain.domain.retrieval import (
    GateZone,
    ScoredNote,
    gate_candidates,
    index_notes,
    rrf_fuse,
)
from second_brain.infra.index.sqlite import SqliteNoteIndex
from second_brain.infra.llm.answerer import InvalidAnswer, check_citations
from second_brain.infra.llm.fakes import (
    FakeEmbedder,
    FakeEnricher,
    FakePivoter,
    FakeReranker,
)
from second_brain.infra.store.markdown import MarkdownNoteRepository
from second_brain.infra.trace.jsonl import JsonlTraceSink


class StubAnswerer:
    def __init__(self, draft: AnswerDraft) -> None:
        self._draft = draft
        self.calls: list[tuple[str, list[str]]] = []

    def answer(self, question: str, notes: Sequence[Note]) -> AnswerDraft:
        self.calls.append((question, [note.id for note in notes]))
        return self._draft


def make_note(note_id: str, title: str, body: str) -> Note:
    return Note(
        id=note_id,
        title=title,
        language=Language.EN,
        type=NoteType.DECISION,
        source=SourceSpan(session_id="s-001", start_turn=0, end_turn=1),
        body=body,
    )


CAIRN_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAA"
PIPELINE_ID = "01BRZ3NDEKTSV4RRFFQ69G5FAB"
BREAD_ID = "01CRZ3NDEKTSV4RRFFQ69G5FAC"

CAIRN = make_note(
    CAIRN_ID,
    "Database choice for Cairn",
    "Chose postgresql with postgis for the cairn side project database.",
)
PIPELINE = make_note(
    PIPELINE_ID,
    "Work pipeline caching",
    "Keep postgresql at work and add a redis cache database for hot lookups.",
)
BREAD = make_note(
    BREAD_ID, "Sourdough bread", "Hydration 75 percent worked for the sourdough."
)


def hits(*pairs: tuple[str, float]) -> list[SearchHit]:
    return [SearchHit(note_id=i, score=s) for i, s in pairs]


def test_rrf_rewards_presence_in_both_legs() -> None:
    dense = hits((CAIRN_ID, 0.9), (PIPELINE_ID, 0.8))
    lexical = hits((CAIRN_ID, 5.0), (BREAD_ID, 4.0))
    fused = rrf_fuse(dense, lexical)
    assert fused[0].note_id == CAIRN_ID  # in both legs → wins


def test_rrf_is_deterministic_on_ties() -> None:
    a = rrf_fuse(hits((CAIRN_ID, 1.0)), hits((PIPELINE_ID, 1.0)))
    b = rrf_fuse(hits((CAIRN_ID, 1.0)), hits((PIPELINE_ID, 1.0)))
    assert [h.note_id for h in a] == [h.note_id for h in b]


def scored(*pairs: tuple[Note, float]) -> list[ScoredNote]:
    return [ScoredNote(note=n, score=s) for n, s in pairs]


def test_gate_three_zones() -> None:
    high = gate_candidates(
        scored((CAIRN, 0.9), (BREAD, 0.1)), tau_high=0.6, tau_low=0.2, max_notes=5
    )
    assert high.zone is GateZone.ANSWER
    assert [s.note.id for s in high.notes] == [CAIRN_ID]  # weak candidate dropped

    mid = gate_candidates(scored((CAIRN, 0.4)), tau_high=0.6, tau_low=0.2, max_notes=5)
    assert mid.zone is GateZone.HEDGED

    low = gate_candidates(scored((CAIRN, 0.1)), tau_high=0.6, tau_low=0.2, max_notes=5)
    assert low.zone is GateZone.ABSTAIN
    assert low.notes == []


def funnel_deps(tmp_path: Path) -> dict:
    embedder = FakeEmbedder()
    index = SqliteNoteIndex(tmp_path / "index.db", embedder.dimensions)
    repo = MarkdownNoteRepository(tmp_path / "notes")
    for note in (CAIRN, PIPELINE, BREAD):
        repo.save(note)
    index_notes(
        [CAIRN, PIPELINE, BREAD],
        enricher=FakeEnricher(),
        embedder=embedder,
        index=index,
    )
    return {
        "embedder": embedder,
        "index": index,
        "repo": repo,
        "reranker": FakeReranker(),
        "pivoter": FakePivoter(),
        "traces": JsonlTraceSink(tmp_path / "traces"),
    }


def test_distractor_demoted_and_context_narrowed(tmp_path: Path) -> None:
    deps = funnel_deps(tmp_path)
    stub = StubAnswerer(
        AnswerDraft(answer="PostgreSQL + PostGIS.", cited_note_ids=[CAIRN_ID], grounded=True)
    )
    result = answer_question(
        "database for the cairn project",
        answerer=stub,
        tau_high=0.6,
        tau_low=0.5,
        **deps,
    )
    assert isinstance(result, Answer)
    (_, shown_ids) = stub.calls[0]
    assert CAIRN_ID in shown_ids
    assert PIPELINE_ID not in shown_ids  # near-miss distractor gated out
    assert [n.id for n in result.sources] == [CAIRN_ID]


def test_weak_top_score_abstains_without_answerer(tmp_path: Path) -> None:
    deps = funnel_deps(tmp_path)
    stub = StubAnswerer(AnswerDraft(answer="unused", grounded=False))
    result = answer_question(
        "quantum entanglement lecture notes",
        answerer=stub,
        tau_high=0.6,
        tau_low=0.5,
        **deps,
    )
    assert isinstance(result, Abstention)
    assert stub.calls == []  # gate abstained before any answerer tokens


def test_mid_zone_returns_hedged(tmp_path: Path) -> None:
    deps = funnel_deps(tmp_path)
    stub = StubAnswerer(
        AnswerDraft(answer="Maybe postgres.", cited_note_ids=[CAIRN_ID], grounded=True)
    )
    result = answer_question(
        "database for the cairn project",
        answerer=stub,
        tau_high=1.5,  # unreachable: everything confident becomes hedged
        tau_low=0.2,
        **deps,
    )
    assert isinstance(result, HedgedAnswer)
    assert 0.0 < result.top_score < 1.5


def test_ungrounded_draft_downgrades_to_abstention(tmp_path: Path) -> None:
    deps = funnel_deps(tmp_path)
    stub = StubAnswerer(
        AnswerDraft(answer="The notes mention Cairn but not that.", grounded=False)
    )
    result = answer_question(
        "database for the cairn project",
        answerer=stub,
        tau_high=0.3,
        tau_low=0.1,
        **deps,
    )
    assert isinstance(result, Abstention)
    assert "Cairn" in result.message  # the model's own explanation is surfaced


def test_citation_rules_still_hold() -> None:
    allowed = {CAIRN_ID}
    check_citations(
        AnswerDraft(answer="ok", cited_note_ids=[CAIRN_ID], grounded=True), allowed
    )
    with pytest.raises(InvalidAnswer):
        check_citations(
            AnswerDraft(answer="bad", cited_note_ids=["01FAKE"], grounded=True), allowed
        )
    with pytest.raises(InvalidAnswer):
        check_citations(AnswerDraft(answer="bad", cited_note_ids=[], grounded=True), allowed)
