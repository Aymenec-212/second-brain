# Planted structure in the seed corpus

The seed spec (`src/second_brain/seed/spec.py`) plants everything below on
purpose. This file is the map: Phase 3's gold questions are written against
it, and the demo script draws from it. Dates are the session dates.

## Contradiction pairs (supersedence / temporal reasoning)

1. **Cairn mobile framework** — 2026-03-07 chose React Native → 2026-05-16
   switched to Flutter (map rendering jank). EN/EN.
2. **Analytics store at work** — 2026-04-17 chose DuckDB → 2026-06-05
   switched to ClickHouse (concurrent analyst queries at 40M rows). EN/EN.
3. **Buy vs rent** — 2026-01-18 "attendre 2027" → 2026-05-09 "acheter en
   2026" (taux < 3,4 %). FR/FR.
4. **Marathon goal** — 2026-03-01 target 3h45 → 2026-06-13 revised to 4h00
   (knee). EN/EN.

Good gold questions: "which mobile framework am I using for Cairn?" (newer
must win), "what was my marathon goal in March?" (temporal must find the
older), "est-ce que j'achète ou je continue à louer ?".

## Near-miss distractor sets (precision)

- **Two database decisions**: Cairn → PostgreSQL+PostGIS (2026-01-24) vs
  work pipeline → keep Postgres + Redis cache (2026-02-20) vs analytics →
  DuckDB/ClickHouse. "Which database did I pick for Cairn?" must not
  surface the work decisions.
- **Hydration**: bread at 75 % hydration (2026-02-21, FR) vs run hydration
  500 ml/h + gels (2026-07-04, EN). Cross-lingual near-miss.
- **Two gifts**: Salma's camera ~120 EUR (2026-02-08) vs father's santoku
  ~90 EUR (2026-05-27). "What did I plan for my sister's gift?" must pick
  the right one.

## Cross-lingual plants (FR notes ↔ EN questions, and reverse)

- Apartment cluster is FR-only: "what's my apartment budget?" (expect
  420 000 EUR / 60 000 EUR apport / 1 900 EUR monthly), "which
  neighborhood did I choose?" (Montreuil).
- Cuisine cluster is FR-only: "what hydration worked for my bread?".
- Marathon VMA note is FR: "what was my VMA test result?" (16.5 km/h).
- Reverse direction: "quel framework mobile pour Cairn ?" against EN notes.

## Recent activity plants (activity queries)

Sessions on 2026-07-01, 2026-07-04, 2026-07-06, 2026-07-08, 2026-07-10 —
"what did I work on recently / this month?" has a known answer set.

## Absent topics (abstention)

Never discussed anywhere: scuba diving, cryptocurrency, gardening, guitar,
chess, sailing, skiing, Japanese, pets, poker, home automation, stock
options. Questions about these must abstain (or trigger the web offer in
Phase 5).
