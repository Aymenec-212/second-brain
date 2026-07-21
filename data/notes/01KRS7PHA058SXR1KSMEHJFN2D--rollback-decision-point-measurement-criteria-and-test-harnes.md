---
created_at: '2026-05-16T20:30:00Z'
entities:
- Moto E
- Pixel 5a
- iPhone 12
- automated perf harness
id: 01KRS7PHA058SXR1KSMEHJFN2D
language: en
source:
  end_turn: 6
  session_id: seed-db906d2dad5e0dcc
  start_turn: 6
tags:
- rollback
- testing
- benchmarks
- performance
title: Rollback decision point, measurement criteria, and test harness specifications
type: decision
---

Rollback decision point set to 2026-07-20. If by that date automated benchmarks and device tests do not meet the acceptance criteria (stable 45 FPS on mid devices, map re-render <100 ms, CPU <15%), we pause the cutover and keep React Native as production. Operational rollback actions: freeze new mobile features for 4 weeks while either (A) fix Flutter issues or (B) invest in RN-native fixes; maintain both branches and keep RN hotfixes. Performance measurement plan: run an automated performance harness on three device tiers: low (Moto E), mid (Pixel 5a or equivalent), high (iPhone 12). The harness should simulate realistic driver workloads including 10,000 route updates (to stress polyline updates), background/foreground transitions, 1s GPS bursts, and panning/zooming interactions. Collect FPS, CPU, memory, frame-render latencies, and occurrence of frame drops; aggregate statistics and worst-case percentiles (p50/p90/p99). Rollout if criteria met: staged rollout starting ~2026-08-02 at 10% of users, then 50%, then 100% over 2–3 weeks, monitoring the same metrics in production. Implementation resourcing during rollback: Marion to maintain RN hotfixes (~40% time) while Jules remains focused on migration.