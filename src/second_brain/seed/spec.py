"""Seed spec: one persona, six simulated months, planted structure.

Tooling, not product — but the structure is deliberate: contradiction
pairs, near-miss distractors, cross-lingual plants, and recent-activity
sessions are all here so that Phase 3's gold questions have known answers.
The companion map lives in evals/planted.md.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from pydantic import BaseModel

from second_brain.domain.models import Language

PERSONA = """\
Sam, 31, backend/ML engineer at a Paris logistics startup. Thinks about
tech mostly in English; about money, family, food, and life mostly in
French. Direct and concrete: keeps numbers, names, and dates. Uses these
sessions to think out loud, weigh options, and record decisions.
"""


class SessionBrief(BaseModel):
    date: datetime
    language: Language
    cluster: str
    brief: str


# (iso date, language, brief) — grouped by cluster for readability.
Beat = tuple[str, str, str]

CLUSTERS: dict[str, list[Beat]] = {
    "cairn": [  # side project: trail-running route planner
        ("2026-01-10", "en", "Concept for 'Cairn', a trail-running route planner. MVP scope: GPX import, route difficulty scoring, sharing later."),
        ("2026-01-24", "en", "DECISION: PostgreSQL + PostGIS over MongoDB for Cairn — geo queries and joins matter more than schema flexibility."),
        ("2026-02-14", "en", "GPS trace simplification: Douglas-Peucker, epsilon trade-offs, target under 500 points per route."),
        ("2026-03-07", "en", "DECISION: React Native for the Cairn mobile app — familiarity wins over Flutter's performance story."),
        ("2026-05-16", "en", "REVERSAL of 2026-03-07: switching Cairn from React Native to Flutter after map rendering jank; sketch the migration plan."),
        ("2026-06-20", "en", "Cairn beta: feedback from 12 testers, top ask is offline maps. DECISION: freemium, premium at 4.99 EUR/month."),
    ],
    "pipeline": [  # work: data pipeline redesign
        ("2026-02-06", "en", "Postmortem thinking: nightly ETL latency grew from 4h to 7h; suspicion is unindexed joins in the orders mart."),
        ("2026-02-20", "en", "DECISION at work: keep Postgres, add a Redis cache for hot lookups — no database migration."),
        ("2026-03-20", "en", "Batch vs streaming: Kafka evaluation notes; worried the team of 4 cannot operate it."),
        ("2026-04-17", "en", "DECISION: DuckDB for the analysts' ad-hoc queries — cheap, simple, single-node."),
        ("2026-06-05", "en", "REVERSAL of 2026-04-17: DuckDB to ClickHouse after benchmarking 40M rows — concurrent analyst queries were the killer."),
    ],
    "appart": [  # apartment purchase deliberation (French only)
        ("2026-01-18", "fr", "Réflexion logement : rester locataire encore un an, le marché parisien est trop cher, viser plutôt 2027."),
        ("2026-03-14", "fr", "Budget appartement précisé : 420 000 EUR max, apport 60 000 EUR, mensualité cible 1 900 EUR."),
        ("2026-04-11", "fr", "Quartiers : 19e arrondissement vs Montreuil — comparaison ; penchant pour Montreuil (maisons, ligne 9, prix)."),
        ("2026-05-09", "fr", "REVERSAL du 2026-01-18 : finalement acheter en 2026 — les taux sont repassés sous 3,4 % et une annonce rare est apparue à Montreuil."),
        ("2026-06-27", "fr", "Simulation de prêt : 3,35 % sur 25 ans ; passer par le courtier recommandé par Karim."),
    ],
    "marathon": [  # training arc, bilingual
        ("2026-03-01", "en", "Marathon plan: Valencia on December 6, target 3h45, four sessions a week."),
        ("2026-04-04", "fr", "Test VMA : 16,5 km/h ; calcul des allures cibles pour les séances."),
        ("2026-05-23", "fr", "Douleur au genou droit (syndrome de l'essuie-glace ?) ; réduire le volume, prendre rendez-vous kiné."),
        ("2026-06-13", "en", "REVISION of 2026-03-01: keeping Valencia but dropping the goal from 3h45 to 4h00 because of the knee."),
        ("2026-07-04", "en", "Back to running. Hydration strategy for long runs: a gel every 40 minutes, 500 ml per hour."),
    ],
    "ml": [  # learning arc
        ("2026-01-31", "en", "PPO intuition notes: the clip objective as a poor man's trust region."),
        ("2026-02-27", "en", "RLHF vs DPO: DPO skips the reward model; when preference data is small, simplicity might win."),
        ("2026-04-25", "en", "Idea: multi-armed bandits for Cairn's route suggestions — exploration bonus for less-run routes."),
        ("2026-05-30", "en", "DECISION: build 'tinygrid', a small gridworld repo, to test RL algorithms hands-on."),
    ],
    "cuisine": [  # French cooking arc
        ("2026-01-15", "fr", "Levain : premier démarrage raté, trop liquide ; repartir sur un mélange 50/50 seigle et T65."),
        ("2026-02-21", "fr", "Pain réussi : hydratation 75 %, autolyse d'une heure, cuisson en cocotte à 240 °C."),
        ("2026-04-18", "fr", "Tarte au citron de grand-mère Aïcha : meringue italienne, zestes de trois citrons, fond précuit."),
        ("2026-06-06", "fr", "DECISION cuisine : pizza napolitaine — chercher un four Ooni d'occasion autour de 250 EUR."),
    ],
    "carriere": [  # career thinking, bilingual
        ("2026-04-08", "en", "Recruiter ping from fintech 'Klarwave': senior role around 92k vs current 78k. Worth exploring?"),
        ("2026-05-02", "fr", "Réflexion equity vs salaire : risque d'une série B, valeur réelle du télétravail, fatigue des process."),
        ("2026-06-18", "en", "DECISION: stay at the current job — negotiated +10% and a 4-day week trial starting September."),
    ],
    "divers": [  # one-offs and recents
        ("2026-02-08", "fr", "Cadeau pour l'anniversaire de ma soeur Salma : un appareil photo argentique (~120 EUR) et des pellicules."),
        ("2026-03-28", "en", "Lisbon long weekend, May 1-4: flights at 140 EUR, airbnb in Alfama, one day trip to Sintra."),
        ("2026-05-27", "fr", "Cadeau fête des pères : un couteau japonais santoku (~90 EUR), à faire graver si possible."),
        ("2026-06-29", "fr", "Discours pour le mariage de Karim : l'anecdote de la panne à Porto, éviter les blagues sur son ex."),
        ("2026-07-08", "en", "Weekly review: triage of Cairn beta bugs, marathon week summary, plan the apartment visit follow-up."),
        ("2026-07-10", "fr", "Point budget de juillet : 480 EUR de dépenses imprévues (kiné + cadeau), ajuster l'enveloppe sorties."),
    ],
}

FILLERS: list[Beat] = [
    ("2026-01-07", "en", "Quick take on a paper about speculative decoding — why it speeds up inference."),
    ("2026-01-21", "fr", "Journal : semaine chargée, deux astreintes ; envie de mieux protéger mes matinées."),
    ("2026-02-03", "en", "Thinking about note-taking systems and why mine never stick."),
    ("2026-02-17", "fr", "Retour sur un documentaire d'alpinisme ; ce que l'engagement veut dire."),
    ("2026-03-05", "en", "Should I learn Rust this year? Weighing it against going deeper in Python."),
    ("2026-03-17", "fr", "Journal : dîner avec Karim et Salma, discussion sur les cadeaux et les vacances."),
    ("2026-03-24", "en", "Small idea: a CLI habit tracker that guilt-trips me gently."),
    ("2026-04-02", "fr", "Réflexion : réduire le téléphone le soir, règle des 30 minutes avant de dormir."),
    ("2026-04-21", "en", "Notes on vector databases hype vs plain Postgres — when is pgvector enough?"),
    ("2026-04-29", "fr", "Journal : week-end pluvieux, beaucoup de lecture, un peu de levain."),
    ("2026-05-06", "en", "Debrief of the Lisbon trip: what worked, what to do differently next city break."),
    ("2026-05-13", "fr", "Idée : cours de cuisine avec Salma pour son anniversaire l'an prochain ?"),
    ("2026-05-20", "en", "Thinking about on-call culture and what a humane rotation looks like."),
    ("2026-06-02", "fr", "Journal : reprise course douce 20 minutes, genou correct, moral en hausse."),
    ("2026-06-10", "en", "Quick eval of terminal multiplexers and my endless tmux config yak-shave."),
    ("2026-06-24", "fr", "Réflexion : appeler mes parents plus souvent, rythme hebdo le dimanche."),
    ("2026-07-01", "en", "Half-year review: Cairn shipped a beta, knee setback, apartment hunt got serious."),
    ("2026-07-06", "fr", "Journal : canicule à Paris, télétravail le matin, course à 7 h."),
]

ABSENT_TOPICS = [
    "scuba diving / plongée sous-marine",
    "cryptocurrency / crypto-monnaies",
    "gardening / jardinage",
    "playing guitar",
    "chess",
    "sailing / voile",
    "skiing holidays",
    "learning Japanese",
    "pets / animaux de compagnie",
    "poker",
    "home automation / domotique",
    "stock options trading",
]


def all_briefs() -> list[SessionBrief]:
    briefs: list[SessionBrief] = []
    for cluster, beats in CLUSTERS.items():
        for iso, lang, brief in beats:
            briefs.append(_make(iso, lang, cluster, brief))
    for iso, lang, brief in FILLERS:
        briefs.append(_make(iso, lang, "journal", brief))
    return sorted(briefs, key=lambda b: b.date)


def session_id_for(brief: SessionBrief) -> str:
    """Deterministic per brief — what makes `sb seed` resumable."""
    digest = hashlib.md5(f"{brief.date.isoformat()}|{brief.brief}".encode()).hexdigest()
    return f"seed-{digest[:16]}"


def _make(iso: str, lang: str, cluster: str, brief: str) -> SessionBrief:
    date = datetime.fromisoformat(iso).replace(hour=20, minute=30, tzinfo=UTC)
    return SessionBrief(date=date, language=Language(lang), cluster=cluster, brief=brief)
