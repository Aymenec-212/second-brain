---
created_at: '2026-03-20T20:30:00Z'
entities:
- Zookeeper
- KRaft
- schema registry
id: 01KM6F1JA0MSDAWJHVXTR1ECY0
language: en
source:
  end_turn: 4
  session_id: seed-7f779b0857c2f80a
  start_turn: 0
tags:
- ops
- dr
- monitoring
- schema
title: Operational concerns to resolve before choosing streaming
type: fact
---

Major operational concerns identified for running Kafka include cluster management choices (Zookeeper vs KRaft), schema registry governance (Avro/Protobuf), topic sizing and partitioning, partition rebalancing behavior, monitoring and alerting for under‑replicated partitions, consumer lag tracking, rolling upgrade procedures, and disaster recovery across regions. Vendor cost ballparks: Confluent Cloud estimated at ~€1,200/month for a small production cluster; AWS MSK in a similar range but with more operator work. The core worry is that a four‑person team with no dedicated SRE cannot reliably operate a self‑managed Kafka cluster while maintaining current on‑call and incident post‑mortem responsibilities; incidents could plausibly double if we self‑manage. Any plan must include mitigations for this ops risk.