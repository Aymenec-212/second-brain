---
created_at: '2026-03-24T20:30:00Z'
entities:
- cli-guilt
- guilt
- sam
- GitHub
- Homebrew
id: 01KMGRMEA032D2X28AWKCWXJJ0
language: en
source:
  end_turn: 0
  session_id: seed-3c2521cc75457297
  start_turn: 0
tags:
- project
- planning
- cli
- privacy
- release
title: 'cli-guilt: project overview, goals, and constraints'
type: decision
---

Project name: working title "cli-guilt" (CLI binary named guilt). Goal: ship MVP v0.1 by 2026-04-07 (two-week target). Personal time budget: approximately 12–16 hours total for the MVP. Core product intent: a tiny terminal habit tracker that gives short, gently guilt-tripping messages. Hard constraints: single static binary, no network telemetry or analytics, config and DB stored locally under ~/.config/cli-guilt/, MIT license, publish source on GitHub at sam/cli-guilt, and provide a Homebrew tap/formula. UX constraint: keep the UI minimal and fast — invoking guilt with no args should default to showing today's status; any primary command should run within ~5s on a normal laptop. Deliverables for v0.1: working add/do/status/history/set-tone commands, default habits preinstalled in a sample config, README with exact usage examples, tag release v0.1.0 on 2026-04-07. Privacy requirement reiterated: everything local only; do not include telemetry or remote template fetching. This note documents the high-level scope, constraints, timeline, and where the project will be published.