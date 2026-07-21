---
created_at: '2026-04-17T20:30:00Z'
entities:
- Claire
- Sam
- DuckDB
- Metabase
- Prometheus
- Alertmanager
- '#infra Slack'
id: 01KPEJ5PA033GX74W38SV7DQKC
language: en
source:
  end_turn: 6
  session_id: seed-536417aa4825bf05
  start_turn: 4
tags:
- on-call
- runbook
- incident-response
- alerts
title: On-call schedule and DuckDB incident runbook
type: task
---

On-call rota and incident runbook for DuckDB: Claire is primary on-call on weekdays 09:00–18:00 CET; I (Sam) take evenings and weekends as secondary. Alerts will be routed to #infra Slack via Prometheus and Alertmanager. The incident runbook for memory/OOM or runaway queries: 1) Identify and cancel the runaway query via Metabase or by SSH-ing to the VM and killing the query/process. 2) Check the DuckDB process memory usage and whether swap is being used; free swap if it is heavily used. 3) Restart the DuckDB service if the process is unresponsive. 4) If the incident recurs for the same workload, raise the Docker/VM memory_limit to 48 GB (from 64 GB physical target, or tune limits) and re-run the problematic Airflow DAG or job in a controlled environment. 5) If interactive scans exceed 200 GB compressed regularly, pre-aggregate that workload or move it to ClickHouse. Set a query_timeout of 600 seconds for ad-hoc connections to prevent multi-hour scans. These steps will be documented and validated during the load-test phase.