---
created_at: '2026-02-20T20:30:00Z'
entities:
- Postgres
- Redis
id: 01KHYBXEA0KEYXYETMGZTRGF4R
language: en
source:
  end_turn: 4
  session_id: seed-d490bfd09772dd8c
  start_turn: 0
tags:
- risks
- consistency
- observability
title: Risks, mitigations, and acceptance criteria
type: idea
---

Key risks identified and planned mitigations: 1) Staleness risk: cached values may be stale. Mitigation: keep TTLs short (30s for order status, 5m for pricing) and require no caching for billing/payment endpoints; use DEL-on-write + pub/sub to proactively evict keys on updates. 2) Multi-instance invalidation races: possible race where one instance writes and another reads before the DEL or pub/sub takes effect. Mitigation: DEL-on-write executed synchronously with the write path; pub/sub provides rapid propagation; TTL fallback bounds staleness. 3) Operational/HA risk: managed Redis failure or failover behavior could impact cache availability. Mitigation: choose multi-AZ with replica and monitor Redis availability; ensure app degrades gracefully to Postgres reads on cache miss. 4) Cost risk: managed Redis may exceed €250/month. Mitigation: re-evaluate instance size and tighten TTLs if initial quotes exceed the cost threshold. Acceptance criteria for full rollout: cache hit rate within the 80–90% target or otherwise validated improvement, cached-endpoint p95 <50 ms, Postgres CPU reduced by ~30% during peaks (or at least 20% reduction at 50% rollout with no regressions), and error rate not increased above +0.5%.