---
created_at: '2026-02-14T20:30:00Z'
entities:
- Ramer–Douglas–Peucker
- Paris logistics
id: 01KHEXH4A0HM5DVSR88K2M2TRF
language: en
source:
  end_turn: 2
  session_id: seed-66e48f8d95d5d45a
  start_turn: 0
tags:
- dataset
- gps
- paris
- sampling
- noise
- routes
title: Dataset and current simplification baseline for Paris logistics routes (Jan–Feb
  2026)
type: fact
---

Dataset summary for the Paris logistics fleet (collected Jan–Feb 2026): 12,000 routes, sampling roughly 1 Hz. GPS noise is on the order of 5–10 meters. Raw points per route: average ≈3,200, median ≈1,500, with some long routes up to ~12,000 points. Current simplification uses Douglas–Peucker (Ramer–Douglas–Peucker) with a fixed epsilon = 10 m. With epsilon = 10 m the observed median simplified count is about 700 points per route, which exceeds the strict downstream requirement of ≤500 points per route; long routes remain >2,000 points after simplification. These are the baseline numbers to improve against.