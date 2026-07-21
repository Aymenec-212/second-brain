---
created_at: '2026-01-24T20:30:00Z'
entities:
- AWS RDS
- PostgreSQL
- PostGIS
- db.t3.medium
- Sam
- Nico
id: 01KFRV61A0WW7BZBMG88801YD5
language: en
source:
  end_turn: 2
  session_id: seed-d2bad5a2a44349e1
  start_turn: 2
tags:
- infra
- rds
- managed
- cost
title: 'Decision: Managed AWS RDS Postgres with PostGIS'
type: decision
---

I chose a managed AWS RDS PostgreSQL instance with the PostGIS extension enabled rather than self-hosting Postgres on Kubernetes. The rationale: faster operational startup, automated backups, point-in-time recovery (PITR), managed read replicas, and reduced ops burden given our small infra team (Nico) and two backend engineers. Initial cost target is approximately €400–€500/month for a baseline instance roughly equivalent to db.t3.medium plus storage and IOPS; budget add-on for a read replica is estimated at ~€120/month if needed. Using RDS buys time and stability for the migration, letting the team focus on schema, indexing, and application changes rather than managing Postgres HA and backup mechanics from day one. Plan to enable PostGIS extension on the managed instance and validate all PostGIS features in staging before production cutover.