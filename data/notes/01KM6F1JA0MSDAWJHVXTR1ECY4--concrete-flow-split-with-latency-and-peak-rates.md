---
created_at: '2026-03-20T20:30:00Z'
entities:
- GPS telemetry
id: 01KM6F1JA0MSDAWJHVXTR1ECY4
language: en
source:
  end_turn: 2
  session_id: seed-7f779b0857c2f80a
  start_turn: 2
tags:
- workloads
- telemetry
- sla
- analytics
title: Concrete flow split with latency and peak rates
type: fact
---

Concrete split of event flows and their requirements: 1) Vehicle GPS telemetry — requires P99 <200ms; peak average ~500 events/sec with spikes up to ~900 events/sec during morning surge; producers are mobile devices through edge gateways. 2) Delivery status updates (picked, en route, delivered) — target latency <5s; peak ~100 events/sec. 3) Billing/analytics events — daily batch acceptable; current volume ~1.2M events/day. 4) SLA alerts for exceptions (e.g., missed pickup) — prefer <1s latency but very low volume (~5 events/sec). Only telemetry and SLA alerts need true streaming low latency; status updates can be hybrid, and analytics can remain in batch.