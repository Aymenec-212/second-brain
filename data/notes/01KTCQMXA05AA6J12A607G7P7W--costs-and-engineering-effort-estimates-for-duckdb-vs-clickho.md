---
created_at: '2026-06-05T20:30:00Z'
entities:
- DuckDB
- ClickHouse
- ClickHouseCloud
- Altinity
id: 01KTCQMXA05AA6J12A607G7P7W
language: en
source:
  end_turn: 4
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- cost
- ops
- budget
title: Costs and engineering effort estimates for DuckDB vs ClickHouse
type: fact
---

Cost and effort estimates: continuing to serve analytics from a single large VM running DuckDB is estimated at ~€200/month. Using a managed ClickHouse cluster (3-node, RF=2) is estimated at ~€1,400/month which fits the stated budget cap of €1,500/month. Initial ops effort estimates varied during planning: an early note estimated ~3 engineer-days for ops setup; the finalized migration plan allocates 5 engineer-days total (3 days infra + 2 days schema/ingest/tests). Budget and engineer-day caps are firm: monthly hosting ≤ €1,500 and migration work ≤ 5 engineer-days. These estimates assume managed ClickHouse to reduce ongoing ops load; additional costs (network egress, S3 storage for backups, Metabase concurrency) are not yet itemized and are an open cost risk to be added to the budget.