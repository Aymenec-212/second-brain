---
created_at: '2026-02-20T20:30:00Z'
entities:
- orders
- payments
- invoices
- websocket /ws/tracking
id: 01KHYBXEA0KEYXYETMGZTRGF4M
language: en
source:
  end_turn: 2
  session_id: seed-d490bfd09772dd8c
  start_turn: 1
tags:
- endpoints
- security
- billing
- cache-exempt
title: Explicit endpoints to exclude from caching (never cached)
type: fact
---

List of endpoints that must never be served from the cache (to be marked cache-exempt in the RFC and implementation): all mutating endpoints — POST, PUT, DELETE that change orders or payments — must not use cached reads around them. Specifically listed: POST /orders, POST /payments, POST /payments/confirm. Read endpoints that are billing-sensitive must also be excluded: GET /payments/* and GET /invoices. Real-time tracking endpoints delivered over websockets must never be cached: websocket path /ws/tracking. Allowed cached endpoints remain GET /orders/:id/status and GET /pricing only. Also, as a rule, any endpoint related to billing or payment confirmation is off-limits for caching given the unacceptable risk of staleness for money-related operations. The implementation should include a centralized cache-exempt matcher (exact paths and wildcard patterns) to avoid accidental caching.