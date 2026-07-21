---
created_at: '2026-06-05T20:30:00Z'
entities:
- network egress
- Metabase
- ClickHouseCloud
- S3
id: 01KTCQMXA05AA6J12A607G7P85
language: en
source:
  end_turn: 9
  session_id: seed-1837740b73faff57
  start_turn: 9
tags:
- risks
- costs
- metabase
- testing
title: Open risks and unanswered items to address before cutover
type: idea
---

Open risks and questions to resolve before migration: 1) Network egress and ingest costs are not yet quantified. Estimate costs for transferring bulk Parquet files from S3 into ClickHouse and recurring egress (if any) for analyst queries and backups, and add a line-item to the monthly budget. 2) Metabase connection concurrency limits are unknown; test Metabase driver connection pooling and maximum concurrent connections now to ensure Metabase will issue the concurrent query patterns used in validation (10–12 concurrent). 3) Validate that the managed ClickHouse service's RBAC and backup features meet corporate compliance and that S3 backup lifecycle policies are in place for the 1-year raw and 3-year aggregated retention. 4) Confirm that paging/escalation notifications to Julien will work with the managed ClickHouse alerting or whether an external pager (PagerDuty) integration is required. Action items: add egress cost estimate to budget, run Metabase concurrency test, check ClickHouseCloud RBAC/backup capabilities, and confirm paging integrations.