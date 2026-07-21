---
created_at: '2026-03-20T20:30:00Z'
entities:
- Kafka
id: 01KM6F1JA0MSDAWJHVXTR1ECXZ
language: en
source:
  end_turn: 2
  session_id: seed-7f779b0857c2f80a
  start_turn: 0
tags:
- kafka
- throughput
- topics
- partitions
- latency
title: 'Kafka evaluation: scope, topics, partitions, and ingestion expectations'
type: fact
---

Early Kafka sizing from the evaluation: scope is ~40 topics and roughly 200 partitions across environments. Expected peak ingestion for the real‑time flows is about 500 events/sec with spikes up to ~900 events/sec during morning surge; overall steady‑state ingestion across all flows is ~5k events/min. Latency requirements are heterogeneous: some flows (vehicle GPS telemetry) need P99 <200ms, others (delivery status updates) can tolerate up to 5s, and analytics can remain daily batch. SLA/exception alerts should be near‑real‑time (<1s preferred) but are low volume. These numbers will drive topic partitioning, retention, and consumer sizing decisions.