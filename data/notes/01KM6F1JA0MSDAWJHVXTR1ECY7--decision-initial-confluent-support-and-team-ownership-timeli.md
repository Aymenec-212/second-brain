---
created_at: '2026-03-20T20:30:00Z'
entities:
- Confluent
- Alice
- Ben
- Claire
id: 01KM6F1JA0MSDAWJHVXTR1ECY7
language: en
source:
  end_turn: 8
  session_id: seed-7f779b0857c2f80a
  start_turn: 8
tags:
- confluent
- support
- roles
- timeline
- budget
title: 'Decision: initial Confluent support and team ownership, timeline and budget
  carve‑out'
type: decision
---

Concrete team decision and ownership: purchase Confluent support for the first three months of production to provide an external escalation path while the team ramps. Execution plan: start with a Confluent Cloud dev PoC (2026-03-23), move to two‑week staging (complete 2026-04-06), make a final decision by 2026-04-10, and aim for production cutover on 2026-05-01. Internal ownership: I will lead the PoC and runbook creation; Alice will build dashboards; Ben will configure Kafka Connectors; Claire will vet consumer libraries and client integration. Team commitment: everyone accepts on‑call notifications, but Confluent will be the primary external escalation for the initial three months. Budget: reserve €1,500/month in Q2 for managed Kafka; anything beyond that requires exec sign‑off. Rollback plan: maintain nightly batch for critical reports for at least six weeks after cutover if issues arise.