---
created_at: '2026-05-20T20:30:00Z'
entities:
- Sam
- Nora
- Leïla
- PagerDaemon
id: 01KS3H9DA0B4F4H138JD2MARDJ
language: en
source:
  end_turn: 10
  session_id: seed-6af5ee8a4e680b90
  start_turn: 4
tags:
- actions
- implementation
- deadlines
- alerts
title: Immediate engineering action items to implement before pilot
type: task
---

Action list with owners and deadlines to prepare the team for the pilot: (1) Implement alert severity field and routing configuration in PagerDaemon so only Sev1 SMS during 19:00–20:30 — owner: Sam, due 2026-05-27. (2) Finalize severity-to-condition mappings (CPU >90% for >5m => Sev2; memory OOM => Sev1; DB unavailable => Sev1) and store them in alert documentation — owner: Sam, due 2026-05-27. (3) Nora to collect and update runbooks with escalation steps and links to logs — due 2026-05-28. (4) Leïla to deliver a 60-minute training aligning the team on the runbooks and handover process — scheduled 2026-05-28. (5) Publish weekend pairing schedule (Jonas: first two weekends with Sam; Marc: third; Leïla: fourth) — owner: Sam, publish by 2026-05-25. (6) Produce and share handover template and example handover (10-min async + 5-min live conditional) — owner: Sam, due 2026-05-30. (7) Create and share the pilot dashboard template; Sam to run weekly updates during the pilot. Completing these tasks on time is required to start the pilot on 2026-06-01.