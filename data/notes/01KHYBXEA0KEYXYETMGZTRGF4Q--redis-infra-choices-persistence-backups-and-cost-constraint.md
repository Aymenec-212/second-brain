---
created_at: '2026-02-20T20:30:00Z'
entities:
- Redis
- RDB
- AOF
id: 01KHYBXEA0KEYXYETMGZTRGF4Q
language: en
source:
  end_turn: 8
  session_id: seed-d490bfd09772dd8c
  start_turn: 7
tags:
- infrastructure
- redis
- cost
- ha
title: Redis infra choices, persistence, backups, and cost constraint
type: decision
---

Infrastructure decision for managed Redis: choose multi-AZ managed Redis with one primary and one replica for high availability (automatic failover). Size the cluster to provide approximately 4 GB usable memory initially; pick the smallest managed instance that meets that usable-memory requirement. Persistence & backups: enable RDB snapshots only (to reduce write amplification), disable AOF. Eviction policy: volatile-lru. Backups: configure daily snapshots. Cost constraint: target delta infra cost < €250/month. If initial managed Redis quotes exceed that cap by more than 20%, re-evaluate to a smaller instance class and compensate with tighter TTLs or narrower cache scope. Operational notes: ensure the managed offering supports pub/sub semantics required for invalidation messages and that failover preserves pub/sub behavior sufficiently for the planned use. Confirm backup retention policy aligns with operational requirements and storage costs before final procurement.