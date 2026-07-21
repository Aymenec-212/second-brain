---
created_at: '2026-01-10T20:30:00Z'
entities:
- Naismith
id: 01KEMSKZA0N5GQ95PF8S94CBXY
language: en
source:
  end_turn: 4
  session_id: seed-6a7500ae87535981
  start_turn: 0
tags:
- scoring
- heuristic
- weights
- explainability
title: Difficulty scoring design — deterministic formula, weights, and buckets (explainability-first)
type: decision
---

Scoring approach: deterministic heuristic (no ML for alpha) and explainability-first — the route page must show component contributions so users see why a route scored e.g. 72. Formula (locked for alpha): score = clamp(100 * (w1*distance_norm + w2*ascent_norm + w3*max_gradient_norm + w4*technical_norm + w5*remoteness_norm + w6*altitude_norm), 0, 100). Initial weights locked: w1..w6 = {0.15, 0.35, 0.2, 0.15, 0.1, 0.05}. Buckets: 0–25 = easy, 26–50 = moderate, 51–75 = hard, 76–100 = very hard. Explainability payload: for each route return raw component values (km, m ascent, max gradient %, technical surface score, remoteness metric, altitude) plus their normalized 0–100 contribution and the weighted contribution; display as numeric values and small visual bars on the route page. The priority is clarity: keep component meanings stable; calibration will use labeled survey responses to adjust thresholds and possibly weights later.