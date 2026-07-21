---
created_at: '2026-02-20T20:30:00Z'
entities:
- Redis
- cache.evictions.via_pubsub
id: 01KHYBXEA0KEYXYETMGZTRGF4K
language: en
source:
  end_turn: 4
  session_id: seed-d490bfd09772dd8c
  start_turn: 3
tags:
- invalidation
- pubsub
- consistency
- redis
title: 'Invalidation strategy: DEL on write + pub/sub propagation + TTL fallback'
type: decision
---

Final invalidation approach: primary invalidation will be application-level DEL on every write that affects cached keys. On each mutating write (e.g., order status change), the service will (1) DEL the specific Redis key(s) and (2) publish a tiny invalidation message to a lightweight Redis pub/sub channel containing only the key name(s) so other app instances can evict local caches or take action immediately. TTL fallback remains in place to bound staleness in case of missed invalidations. No database triggers or migration-based invalidation will be used. Operational instrumentation: add a metric named cache.evictions.via_pubsub (counter) to confirm pub/sub messages propagate and are processed; also track cache.del-at-write counts and any DEL failures. Messages must be kept minimal (just the key names) to reduce overhead. This combined approach balances immediacy (DEL + pub/sub) with safety (TTL expiry) and avoids coupling to the database.