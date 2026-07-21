---
created_at: '2026-03-20T20:30:00Z'
entities:
- Confluent Cloud
- Kafka Connect
- S3
- Postgres
- Avro
- Protobuf
id: 01KM6F1JA0MSDAWJHVXTR1ECY2
language: en
source:
  end_turn: 8
  session_id: seed-7f779b0857c2f80a
  start_turn: 0
tags:
- poc
- confluent
- timeline
- connect
title: Preferred PoC plan and production timeline
type: task
---

Preferred proof‑of‑concept plan: spin up a Confluent Cloud development cluster (dev PoC starting 2026-03-23), use Kafka Connect to push data to S3 and Postgres for long‑term storage and materialized views, and deploy a schema registry using Avro or Protobuf. Implement monitoring, dashboards, and a concise runbook during the PoC. Staging for two weeks (target complete by 2026-04-06), then decision by 2026-04-10. If PoC passes, target production cutover to Confluent Cloud by 2026-05-01. Contingency: maintain the nightly batch as a rollback/fallback for critical reports for at least 6 weeks after cutover. The PoC will validate connectors, schema enforcement, retention policies, and basic DR/restore procedures.