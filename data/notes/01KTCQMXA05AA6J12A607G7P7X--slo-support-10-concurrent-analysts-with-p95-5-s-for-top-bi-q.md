---
created_at: '2026-06-05T20:30:00Z'
entities:
- Sam
- Alice
- Julien
- Metabase
id: 01KTCQMXA05AA6J12A607G7P7X
language: en
source:
  end_turn: 2
  session_id: seed-1837740b73faff57
  start_turn: 2
tags:
- slo
- performance
- concurrency
title: 'SLO: support 10 concurrent analysts with p95 < 5 s for top BI queries'
type: decision
---

Service-level objective (SLO) decision: commit to supporting 10 concurrent analysts with p95 < 5 seconds for the top BI queries used in day-to-day work. This target is judged realistic based on ClickHouse PoC results (p95 ~1.8 s at 12 concurrent on a 3-node test cluster). Acceptance tests must validate the SLO under real analyst query patterns and concurrency (10 concurrent, with testing up to 12 concurrent to verify headroom). The SLO is the main pass/fail criterion for cutover; if the p95 exceeds 5 s for the set of top queries under 10 concurrent, the plan is to revert to DuckDB (via Metabase connection rollback) within a 48-hour window.