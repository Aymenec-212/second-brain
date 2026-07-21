---
created_at: '2026-04-25T20:30:00Z'
entities: []
id: 01KQ35BEA0AYPP1Y73QBEM3RB8
language: en
source:
  end_turn: 2
  session_id: seed-84923c99c7de0aab
  start_turn: 2
tags:
- metrics
- reward
- normalization
- kpi
- on-time
title: 'Reward signal: raw seconds saved per trip and normalization plan (check mapping)'
type: fact
---

Primary reward signal: raw seconds saved per trip (continuous) — chosen because it is sensitive and can detect small improvements. Secondary guardrail: on-time percentage must stay >= 98%. Baseline definition: compute baseline_time per (route_id, hour_bucket) as the historical median actual_time for that route-context. Raw delta = baseline_time - actual_time. Clamping: clamp raw delta to the interval [-600, +300] seconds so large regressions are heavily penalized and very large gains are bounded. Normalization plan described in the decision: transform the clamped delta to a [0,1] reward to feed bandit algorithms. The stated mapping was "divide by 600 and shifting (so -600 -> 0, +300 -> 1)". Note: this description is inconsistent mathematically (mapping -600 to 0 and +300 to 1 requires an affine map over a 900-second span, not a simple division by 600). Action item (open question): confirm the exact affine transform to use. Suggested explicit mapping to avoid ambiguity: reward = (clamped_delta + 600) / 900, which maps -600 -> 0 and +300 -> 1. Reporting: always surface both the normalized reward and the raw seconds saved plus on-time % in dashboards and simulation outputs.