---
created_at: '2026-03-20T20:30:00Z'
entities:
- Airflow
- Postgres
- Alice
- Ben
- Claire
id: 01KM6F1JA0MSDAWJHVXTR1ECXY
language: en
source:
  end_turn: 4
  session_id: seed-7f779b0857c2f80a
  start_turn: 0
tags:
- pipeline
- batch
- team
- airflow
- postgres
title: Current nightly batch pipeline, scale, and team constraints
type: fact
---

Current production pipeline is a single Airflow DAG that runs nightly at 02:00 and processes approximately 1.2M events in ~45 minutes, exporting results to Postgres for analytics. The engineering team is four people: myself (backend/ML), Alice, Ben, and Claire. There is no dedicated SRE. On-call is a rotating duty among the four engineers (roughly one week per person per month). Today we experience about three infrastructure incidents per month outside business hours (examples: DB failover, Airflow job failures), and that cadence is already painful for the current rota. Any change to a higher‑operational‑overhead platform needs to account for this limited operational capacity and the lack of a separate SRE role.