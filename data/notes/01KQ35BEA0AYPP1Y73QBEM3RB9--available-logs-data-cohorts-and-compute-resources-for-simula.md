---
created_at: '2026-04-25T20:30:00Z'
entities:
- Redshift
- Spark
- Jules
- Claire
id: 01KQ35BEA0AYPP1Y73QBEM3RB9
language: en
source:
  end_turn: 4
  session_id: seed-84923c99c7de0aab
  start_turn: 4
tags:
- data
- logging
- infra
- redshift
- spark
title: Available logs, data cohorts, and compute resources for simulation and training
type: fact
---

Data availability: full trip-level logs (2.4M trips since 2024-01-01) include route_id, start_time, driver_id, ETA_pred, actual_time, distance_m, traffic_index, weather_code, safety_score, and override_flag when drivers reject a suggested route. Logs are synced daily to Redshift. Route usage cohorts: 80 routes are cold (<20 runs), 60 routes are medium (20–200 runs), and the remainder have >200 runs. Compute/storage: Spark cluster is available for large-scale offline simulation and daily batch retrain jobs. Operational stakeholders: Product owner Jules and Ops lead Claire must receive and approve simulation results before any live deploy. Treatment of driver override: override_flag is present in logs and should be treated as a strong negative signal during simulation and modeling (user later decided it will be an immediate negative reward). Data engineering note: build pipelines to compute baseline_time per (route_id, hour_bucket) and daily per-route counts; ensure privacy and retention policies for driver-level IDs are respected in simulation.