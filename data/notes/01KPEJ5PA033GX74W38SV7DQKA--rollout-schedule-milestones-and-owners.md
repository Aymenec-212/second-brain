---
created_at: '2026-04-17T20:30:00Z'
entities:
- Sam
- Claire
- Airflow
- Metabase
id: 01KPEJ5PA033GX74W38SV7DQKA
language: en
source:
  end_turn: 8
  session_id: seed-536417aa4825bf05
  start_turn: 2
tags:
- plan
- milestones
- owners
- timeline
title: Rollout schedule, milestones, and owners
type: task
---

Concrete rollout timeline and owners: - Provision the production VM (8 vCPU / 64 GB / 1 TB NVMe) immediately; target complete by 2026-04-30. - Implement the Airflow DAG that nightly writes partitioned Parquet to S3 and produces the nightly DuckDB DB file by 2026-04-30. - Connect Metabase to DuckDB via JDBC by 2026-05-05. - Execute an internal load-test with 3 analysts (Leo, Maria, Aisha) to simulate typical concurrency by 2026-05-10. - Communicate the data freshness and DuckDB scope to the analytics team by 2026-05-10 (so they do not expect near-real-time results). - Go-live with DuckDB-backed Metabase by 2026-05-15. - Conduct weekly check-ins through 2026-06-01 to validate performance assumptions and budget. Owners: Claire is primary infra lead for provisioning and monitoring; I (Sam) am secondary and responsible for DAG implementation and coordinating tests. Alerts and on-call procedures will be set up before go-live.