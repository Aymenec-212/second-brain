---
created_at: '2026-03-24T20:30:00Z'
entities:
- Sam
- set-tone
- --quiet
- --simulate
id: 01KMGRMEA032D2X28AWKCWXJJ2
language: en
source:
  end_turn: 4
  session_id: seed-3c2521cc75457297
  start_turn: 4
tags:
- personalization
- templates
- tone
- defaults
- cli
title: Personalization, templates, tones, default habits, and CLI flags
type: decision
---

Guilt messages must be personalized locally: use the user's name "Sam" and include a stat line. Message templates should support placeholders like {name},{habit},{streak},{missed},{pct30}. Default tone is gentle; allow per-user tone selection via the command "guilt set-tone gentle|stern|shame" stored in the local config. Provide three pre-configured habits for the alpha build committed as defaults: 1) read (daily), 2) meditate (daily 10m), 3) no-sugar (weekdays). CLI helper flags: --quiet to suppress guilt message output for scripting, and --simulate to render the guilt message without modifying the DB (useful for testing templates). Tests required: unit tests for schedule logic (detecting misses, computing streaks), and tests for message rendering (templates populate and color codes are correct). Plan to ship v0.1.0 on 2026-04-07 to GitHub sam/cli-guilt with a README containing exact commands and a sample config.