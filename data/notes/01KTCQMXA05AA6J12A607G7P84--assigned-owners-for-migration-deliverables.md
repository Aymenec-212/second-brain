---
created_at: '2026-06-05T20:30:00Z'
entities:
- Sam
- Alice
- Julien
- Metabase
- ClickHouseCloud
id: 01KTCQMXA05AA6J12A607G7P84
language: en
source:
  end_turn: 8
  session_id: seed-1837740b73faff57
  start_turn: 4
tags:
- owners
- roles
- migration
title: Assigned owners for migration deliverables
type: fact
---

Owner assignments for the migration: Sam is the migration lead and will own schema translation, orchestration of the bulk load and the cutover. Alice (data analyst) will validate query correctness and performance and provide sign-off before cutover. Julien (ops) will manage the ClickHouse account, configure alerts/monitoring, handle backups to S3, and respond to escalations. Additional responsibilities: Sam coordinates Metabase connection update on cutover date (2026-06-19) and communicates the change to analysts; Julien is responsible for paging rules and ensuring RBAC and backups are configured on the managed ClickHouse service.