---
created_at: '2026-05-20T20:30:00Z'
entities:
- Sam
- Marion
id: 01KS3H9DA0B4F4H138JD2MARDB
language: en
source:
  end_turn: 6
  session_id: seed-6af5ee8a4e680b90
  start_turn: 5
tags:
- kpi
- monitoring
- dashboard
- noise
title: KPIs, noise measurement, and dashboard plan for the pilot
type: decision
---

KPIs to collect weekly during the pilot: total pages per on-call week, MTA (mean time-to-acknowledge) with 15-minute target, MTTR (mean time-to-repair) with 90-minute target, number of Sev1 incidents, number of compensatory days triggered, and average subjective sleep rating (1–5). Noise metric: measure 'noise' as the count of pages that are Sev2 or lower during 19:00–20:30 which required manual intervention; pilot target is 0 such interventions during the dinner window. Also track Slack pings to the on-call during 19:00–20:30 (target <2/week). Dashboard cadence: aggregated weekly numbers plus rolling 4-week trends; present dashboard to Marion on 2026-07-01. Contingency thresholds: if average sleep rating drops below 3 or pages/night >2 for more than two consecutive weeks, pause the pilot and revert. Metrics owner: I (Sam) will own the dashboard and weekly review. These KPIs are deliberately simple to maintain clarity and enable quick decision-making.