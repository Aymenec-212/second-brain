---
created_at: '2026-03-20T20:30:00Z'
entities:
- Confluent
id: 01KM6F1JA0MSDAWJHVXTR1ECY5
language: en
source:
  end_turn: 4
  session_id: seed-7f779b0857c2f80a
  start_turn: 4
tags:
- oncall
- budget
- operations
title: Current on‑call capacity, incident estimate for Kafka, and budget preferences
type: fact
---

Current on‑call rota: four engineers rotating roughly one week each per month. Current incidents outside business hours: ~3/month. Projection: Kafka‑related incidents could plausibly double if self‑managed. Budget constraints reiterated: commit up to €1,500/month without exec sign‑off; expenditures above €2,000/month need CFO discussion. Preference is to use managed Confluent for operational safety and schema tooling. As a safety net, keep the nightly batch pipeline as a fallback for critical reports for at least six weeks post cutover, and invest in automated monitoring and concise runbooks to limit ops load.