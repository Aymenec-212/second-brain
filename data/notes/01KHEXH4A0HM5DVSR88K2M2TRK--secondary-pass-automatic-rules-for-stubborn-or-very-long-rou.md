---
created_at: '2026-02-14T20:30:00Z'
entities: []
id: 01KHEXH4A0HM5DVSR88K2M2TRK
language: en
source:
  end_turn: 8
  session_id: seed-66e48f8d95d5d45a
  start_turn: 6
tags:
- edge-cases
- secondary-pass
- splitting
- tagging
- qa
title: Secondary-pass automatic rules for stubborn or very long routes
type: decision
---

Secondary-pass rules for routes that remain >500 points after the primary pass: if a route's raw point count >8,000 and primary pass (1–50 m) still yields >500 points, perform an automatic secondary pass. First, split the route into legs by detecting time gaps >30 minutes and treat each leg independently (rerun primary rules on each leg). If any leg still exceeds 500 points, allow a higher epsilon up to 100 m for that leg (or route) but mark the route with a clear flag "auto-squeezed-100m". Keep these auto-second-pass events minimal; they must be logged in detail and included in the daily monitoring report for QA review. If automated measures still fail in extreme cases, the route should be placed on a manual review list, but the goal is to minimize manual QA via the automated split-and-relax flow.