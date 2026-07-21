---
created_at: '2026-03-24T20:30:00Z'
entities:
- guilt
- db.json
- config/default.json
- Homebrew
- v0.1.0
id: 01KMGRMEA032D2X28AWKCWXJJ5
language: en
source:
  end_turn: 9
  session_id: seed-3c2521cc75457297
  start_turn: 0
tags:
- implementation
- testing
- packaging
- release
- todo
title: MVP implementation tasks, tests, packaging, and next steps (actionable checklist)
type: task
---

Actionable checklist to reach v0.1 by 2026-04-07 (two-week window) within the 12–16 hour personal estimate: 1) Initialize git repo sam/cli-guilt and add MIT license. 2) Commit config/default.json with three default habits and config/templates.json containing the exact templates from the authoritative note. 3) Implement JSON DB storage at ~/.config/cli-guilt/db.json with atomic writes and the documented habit schema. 4) Implement core commands: add, do, status, history, set-tone — prioritize "guilt do <habit>" first so fast logging works end-to-end. 5) Implement schedule logic to compute streaks, missed-days, and 30-day adherence percent. 6) Implement ANSI-colored one-line output with the exact prefixes and colors; enforce <=120-char output. 7) Wire CLI parsing using Go (cobra or urfave), compile static binary for macOS/Linux. 8) Tests: unit tests for schedule logic and streak calculations; rendering tests that assert exact strings and ANSI escapes (use --simulate mode to aid deterministic rendering). 9) Packaging: create a Homebrew formula/tap and test installation locally; estimate ~4 hours. 10) README: include exact example commands and outputs, config locations, and release notes. 11) Release: tag v0.1.0 and publish on GitHub on 2026-04-07. Prioritization: start with items 2–6 so "guilt do" behaves correctly within the first half of the time budget, then implement tests and packaging. Immediate next step I planned: initialize the git repo and add default config and templates so first-run behavior works; then implement the "do" command and template rendering with tests.