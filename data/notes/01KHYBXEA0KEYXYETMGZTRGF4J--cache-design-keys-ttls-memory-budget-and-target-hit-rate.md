---
created_at: '2026-02-20T20:30:00Z'
entities:
- Redis
id: 01KHYBXEA0KEYXYETMGZTRGF4J
language: en
source:
  end_turn: 2
  session_id: seed-d490bfd09772dd8c
  start_turn: 0
tags:
- cache-design
- keys
- ttls
- pricing
- orders
title: 'Cache design: keys, TTLs, memory budget, and target hit rate'
type: fact
---

Cache design details for the initial implementation: cache only specific read endpoints (GET /orders/:id/status and GET /pricing?route=...). Key design: one key per order id for order status (e.g., orders:status:{order_id}); one key per pricing query using a deterministic hash of the pricing query parameters (e.g., pricing:hash:{sha256(params)}). TTL policy: 30 seconds for order status keys, 5 minutes for pricing keys. Eviction policy: volatile-lru (so only keys with TTLs are considered for eviction). Memory budget: target 4 GB usable memory on Redis initially (sizing to cover expected working set and headroom). Performance target: aim for a cache hit rate between 80% and 90% on these hot endpoints. No schema changes in Postgres and no data movement—Redis is strictly a read-side cache. These choices prioritize low staleness for order status while allowing longer-lived pricing responses to amortize compute; TTLs and hash-based keys are chosen to keep key space manageable and to avoid complex namespace logic.