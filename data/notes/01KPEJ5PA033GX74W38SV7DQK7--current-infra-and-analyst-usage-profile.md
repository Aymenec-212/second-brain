---
created_at: '2026-04-17T20:30:00Z'
entities:
- Postgres
- S3
- Parquet
- Airflow
- Metabase
- Leo
- Maria
- Aisha
id: 01KPEJ5PA033GX74W38SV7DQK7
language: en
source:
  end_turn: 0
  session_id: seed-536417aa4825bf05
  start_turn: 0
tags:
- infra
- analytics
- datasets
title: Current infra and analyst usage profile
type: fact
---

Existing production infrastructure: Postgres is used for OLTP and storing the most recent/live data; raw data lake resides in S3 as Parquet files; Airflow is the orchestration tool; Metabase is used for dashboards and ad-hoc queries. The analysts are a small team of three: Leo, Maria, and Aisha. Their ad-hoc workload is light: roughly 20 ad-hoc queries per day, with concurrency typically 1–3 simultaneous users. Typical datasets explored interactively are between 1–50 GB (compressed); occasional investigations touch up to ~200 GB compressed. Once every few months there is occasional inspection of backups or long-range joins where raw input can be ~500 GB uncompressed but compressed size is usually <=200 GB. The operational constraint is a hard preference to keep infra cost around €200/month and to minimize ongoing ops overhead.