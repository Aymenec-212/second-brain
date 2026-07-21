---
created_at: '2026-04-21T20:30:00Z'
entities: []
id: 01KPRVRJA040F390AW1FABMRAX
language: en
source:
  end_turn: 2
  session_id: seed-b1386cf507fa6f14
  start_turn: 2
tags:
- priorities
- sla
- cost
- ops
- recall
title: Operational priorities and ranking
type: decision
---

Ranked priorities for any solution: 1) latency — meeting the p95 target (goal <50 ms) is the top priority; 2) total cost ≤ €2,000/month is the next constraint; 3) low operational overhead (≤10 hours/week) is important given a two-engineer team; 4) accurate recall (recall@10 ≥ 0.9) is required for business utility. Any architecture choice must be evaluated primarily against latency, then cost, then ops burden, then recall. If a solution violates a higher-priority constraint it is unacceptable even if it improves lower-priority metrics.