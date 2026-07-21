---
created_at: '2026-02-14T20:30:00Z'
entities:
- Paris logistics
id: 01KHEXH4A0HM5DVSR88K2M2TRG
language: en
source:
  end_turn: 6
  session_id: seed-66e48f8d95d5d45a
  start_turn: 2
tags:
- requirements
- constraints
- delivery
- geofence
title: 'Hard constraint: strict per-route cap 500 + must preserve stops/geofences'
type: decision
---

Requirement decision: every route must be strictly capped at ≤500 points after simplification. A percentile or average-based cap is unacceptable because downstream systems assume a hard limit. In addition, the simplifier must always preserve delivery/stop points (typically 3–5 stops per route) and any mapped geofence anchor points. Preservation must be enforced before simplification (protected indices) to make the process deterministic and simpler to reason about. Angle-based important points (e.g., turns) should also be protected where possible. These preservation rules are non-negotiable; any solution must guarantee those points remain present in the simplified polyline.