---
created_at: '2026-03-24T20:30:00Z'
entities:
- guilt do
- db.json
- Go
- cobra
- urfave
id: 01KMGRMEA032D2X28AWKCWXJJ1
language: en
source:
  end_turn: 2
  session_id: seed-3c2521cc75457297
  start_turn: 2
tags:
- core-action
- data-model
- escalation
- implementation
- go
title: 'Core action: fast logging behavior, data model, escalation rules, and implementation
  choices'
type: decision
---

Single required core action for v0.1: fast logging via "guilt do <habit>". The command must be a one-liner, complete the data update (streaks/history/last), and print an immediate personalized guilt message. Command examples to support: "guilt do read", "guilt do meditate --when 2026-03-24T08:30", and habit creation like "guilt add \"no-sugar\" --days weekdays". Data model (JSON) lives at ~/.config/cli-guilt/db.json; each habit entry should look like: {"id":"read","name":"Read 30m","schedule":"daily","streak":5,"last":"2026-03-23","history":["2026-03-20","2026-03-21",...]} — the implementation must update streak and history arrays atomically on a successful "do". Escalation rules for MVP: missed 1 day → gentle hint; missed 2–3 days → firmer; missed >=4 days → sharp. Guilt messages must include the user's name, habit, streak info, and a 30-day adherence percentage. Implementation preference: use Go to produce a single static binary and enable easy cross-compiles; use a CLI flags library similar to cobra or urfave for args parsing. Time estimate: ~8–12 hours to implement add/do/status plus tests, ~4 hours for packaging and creating a Homebrew formula. Privacy: local only, no analytics or outgoing network traffic.