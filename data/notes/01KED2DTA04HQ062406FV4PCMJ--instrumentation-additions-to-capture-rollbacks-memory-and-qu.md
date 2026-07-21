---
created_at: '2026-01-07T20:30:00Z'
entities:
- per-block acceptance histogram
- time-to-rollback distribution
- memory allotment
id: 01KED2DTA04HQ062406FV4PCMJ
language: en
source:
  end_turn: 9
  session_id: seed-080a3566d9e37509
  start_turn: 7
tags:
- instrumentation
- telemetry
- quality
title: Instrumentation additions to capture rollbacks, memory, and quality regressions
type: task
---

Instrumentation to add to each run so Jan 10 decision is unambiguous: - Per-block acceptance histogram (counts by k and by prompt/customer). - Time-to-rollback distribution: how long it takes from draft proposal to detection and handling of a rejection. - Tail latency conditioned on rollbacks (p50/p95/p99 for requests that experienced at least one rollback). - Memory allotment per forward and tracking of transient memory spikes (peak GPU memory per step). - Position-in-context for rollbacks (do rejections happen early in the block or late?). - Log rollback overhead in wall-clock and wasted compute (seconds and % of total compute). - Add an adversarial synthetic set of worst-case prompts (constructed to stress low-acceptance scenarios) and a small human evaluation to surface quality regressions when draft proposals are accepted. Also record per-customer and prompt-length stratified telemetry so acceptance rates are not averaged away across heterogeneous customers.