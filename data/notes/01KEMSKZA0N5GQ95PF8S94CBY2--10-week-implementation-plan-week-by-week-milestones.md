---
created_at: '2026-01-10T20:30:00Z'
entities:
- Cairn
id: 01KEMSKZA0N5GQ95PF8S94CBY2
language: en
source:
  end_turn: 4
  session_id: seed-6a7500ae87535981
  start_turn: 4
tags:
- plan
- milestones
- schedule
title: 10-week implementation plan (week-by-week milestones)
type: task
---

Week-by-week plan to reach alpha on 2026-03-15 (10 weeks total from 2026-01-11): - Week 1–2 (Jan 11–Jan 24): infrastructure + API skeleton, GPX parser, resampling, elevation smoothing. - Week 3–4 (Jan 25–Feb 7): implement feature computations (distance, ascent, gradient distributions), OSM joins for technicality, basic DEM integration. - Week 5 (Feb 8–Feb 14): implement scoring function with explainability payload, unit tests for metrics and transforms. - Week 6 (Feb 15–Feb 21): contractor integration and simple React UI for import flow and result page. - Week 7 (Feb 22–Feb 28): prepare labeling survey, instrumentation (metrics counters), privacy text, and opt-out/delete flow. - Week 8 (Mar 1–Mar 7): bug fixes, performance tuning, cost verification (S3/API usage). - Week 9 (Mar 8–Mar 14): internal alpha testing, invite friends and Strava contacts for early feedback. - Week 10 (Mar 15): alpha launch. Priority: keep scope tight, skip map tiles beyond a single simplified polyline or static tile image for UI to fit €4k contractor budget.