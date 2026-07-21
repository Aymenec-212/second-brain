---
created_at: '2026-04-25T20:30:00Z'
entities:
- contextual Thompson Sampling
- UCB
id: 01KQ35BEA0AYPP1Y73QBEM3RBA
language: en
source:
  end_turn: 6
  session_id: seed-84923c99c7de0aab
  start_turn: 6
tags:
- algorithm
- thompson-sampling
- ucb
- production
- logging
- daily-batch
title: 'Algorithm and production cadence decision: start with daily batch; algorithm
  details and logging'
type: decision
---

Decision: start with daily batch updates (no online per-trip updates initially) to fit current engineering capacity and reduce operational risk. Algorithm plan: use contextual Thompson Sampling (CTS) as the primary algorithm. Context vectors: route_id embedded, hour_bucket, traffic_index, and driver_experience (feature capturing driver familiarity/performance). Baseline comparator: UCB with an exploration bonus term = beta / sqrt(n_r) for route r. Exploration schedule: aggressive initial learning — start with beta = 0.5 for the first two weeks to accelerate data collection, then anneal to beta = 0.1. Candidate filtering: enforce hard constraints before arm selection (filter candidates where distance > baseline_distance * 1.10 or safety_score < 0.9). Logging requirements per served suggestion: candidate_list (filtered), chosen_route_id, override_flag, actual_time, route_distance, per-route daily counts, and context vector. Metrics to monitor during an A/B run (8 weeks from 2026-05-10): mean trip time (seconds) [primary], on-time % (>= 98% guardrail), driver override rate, route utilization entropy (to measure coverage), and a focused edge-case report for the 80 low-data routes. Sample calculations for capacity: 120 drivers * 3 suggestions/day * 5 working days = 1,800 suggestions/week; with 2 arms that is ~900 trips/week/arm; over 8 weeks ~7,200 trips/arm — preliminary reason to expect power to detect ~2% mean-time change if variance is favorable, but this must be validated in simulation.