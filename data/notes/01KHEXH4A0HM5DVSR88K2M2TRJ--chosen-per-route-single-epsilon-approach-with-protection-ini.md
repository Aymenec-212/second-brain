---
created_at: '2026-02-14T20:30:00Z'
entities:
- Ramer–Douglas–Peucker
id: 01KHEXH4A0HM5DVSR88K2M2TRJ
language: en
source:
  end_turn: 6
  session_id: seed-66e48f8d95d5d45a
  start_turn: 4
tags:
- design
- epsilon
- binary-search
- protection
- heuristic
title: Chosen per-route single-epsilon approach with protection, initial-epsilon heuristic,
  and binary search
type: decision
---

Final design decision: use a single epsilon per route (easier downstream guarantees) found by binary search. Protect indices before simplification: delivery stops (3–5 average), geofence anchors, and high-angle points (local turning angle >30°). For angle detection smooth positions with a 3-sample median filter to reduce jitter before computing angles (compute angle using ±3-sample window). Epsilon search bounds: lower = 1 m, upper = 50 m for the primary pass, max iterations = 8. Initial epsilon heuristic to bias search toward appropriate scale: initial_epsilon = 8 m + frac_highway * 20 m, where frac_highway is the fraction of samples labeled highway by median-speed thresholds. For urban-dominant routes the initial guess will be close to 8 m; for highway-heavy routes it increases toward 28 m. During the binary search the process stops early if the simplified count ≤500. Sanity checks: after simplification compute the maximum perpendicular error (meters) and assert it is ≤ final epsilon; log this value per-route.