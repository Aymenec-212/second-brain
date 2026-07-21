---
created_at: '2026-02-20T20:30:00Z'
entities:
- Postgres
- Redis
- Sam
id: 01KHYBXEA0KEYXYETMGZTRGF4H
language: en
source:
  end_turn: 8
  session_id: seed-d490bfd09772dd8c
  start_turn: 0
tags:
- architecture
- postgres
- redis
- cache
- decision
- performance
title: 'Decision: keep Postgres; add Redis read-side cache for hot lookups (no DB
  migration)'
type: decision
---

Decision summary made 2026-02-20: keep the existing Postgres database and add a managed Redis read-side cache to serve hot lookups only; explicitly do not perform any database migration or move data out of Postgres. The immediate performance goals are to reduce p95 latency for targeted hot endpoints from ~250 ms to under 50 ms, and to lower Postgres CPU usage by roughly 30% during peak traffic (current peak ~800 read QPS). The implementation is feature-flagged: I (Sam, backend/ML engineer) will implement the cache client logic; infrastructure will provision a managed Redis instance (primary + replica). The rollout window is a roughly three-week gradual deployment starting 2026-02-23 and ending ~2026-03-13. Track metrics (cache hit rate, p95 latency for cached endpoints, Postgres CPU, and endpoint error rate) during rollout. Cost target: keep the incremental monthly infra cost under €250; re-evaluate if initial quotes exceed that by more than 20%. This decision is scoped narrowly: only read-side caching for specific endpoints; no schema changes, no DB triggers, and no changes that affect billing or other critical consistency guarantees.