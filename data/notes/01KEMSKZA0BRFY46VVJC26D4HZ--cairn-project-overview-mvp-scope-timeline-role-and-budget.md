---
created_at: '2026-01-10T20:30:00Z'
entities:
- Cairn
- Strava
- Reddit
id: 01KEMSKZA0BRFY46VVJC26D4HZ
language: en
source:
  end_turn: 0
  session_id: seed-6a7500ae87535981
  start_turn: 0
tags:
- project
- timeline
- mvp
- budget
- roles
title: Cairn project overview — MVP scope, timeline, role, and budget
type: fact
---

Project name: Cairn — a trail-running route planner. I'm the sole developer for backend and ML (31, backend/ML engineer at a Paris logistics startup) and will hire a React contractor for the UI. MVP scope: GPX import + deterministic route difficulty scoring. Sharing/export is postponed to v1.1 (target 2026-06-01). Timeline: alpha ready by 2026-03-15 (10 weeks from 2026-01-10) and public beta by 2026-04-15. Time budget: I can allocate ~10 hours/week. Contractor/UI budget: €4,000 for the UI slice (estimated two weeks of work). Hosting estimate for alpha: €50–100/month; anticipate S3 bandwidth and tiles could push to <€200/month with ~1,000 users in first 3 months. Key alpha success metrics to track: (1) 1,000 unique GPX imports in first 3 months, (2) Spearman rho between mean user rating and model score > 0.6, (3) 25% retention (users import another route). These goals guide feature and instrumentation priorities.