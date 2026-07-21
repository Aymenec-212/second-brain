---
created_at: '2026-03-20T20:30:00Z'
entities:
- Confluent Cloud
- Aiven
- MSK
- k8s
- Redis
- WebSockets
id: 01KM6F1JA0MSDAWJHVXTR1ECY1
language: en
source:
  end_turn: 0
  session_id: seed-7f779b0857c2f80a
  start_turn: 0
tags:
- options
- architecture
- streaming
- batch
title: Alternatives being considered for streaming vs batch
type: idea
---

Four architectural options under consideration: 1) Managed Kafka (Confluent/Aiven/MSK) — pay for operational support and faster launch. 2) Self‑managed Kafka on Kubernetes — lower direct vendor cost but high ops risk and maintenance burden. 3) Keep the nightly batch pipeline and implement targeted push mechanisms (WebSockets or Redis streams) only for the few real‑time requirements, avoiding full streaming infrastructure. 4) Hybrid: deploy managed Kafka for the latency‑sensitive real‑time flows (telemetry, SLA alerts) while keeping daily batch for analytics and non‑latency‑sensitive events. The hybrid option aims to limit scope and operational complexity while providing the critical real‑time guarantees.