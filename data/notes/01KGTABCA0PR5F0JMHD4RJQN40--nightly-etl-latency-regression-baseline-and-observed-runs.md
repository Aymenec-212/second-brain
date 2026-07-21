---
created_at: '2026-02-06T20:30:00Z'
entities:
- orders_mart
- ETL
id: 01KGTABCA0PR5F0JMHD4RJQN40
language: en
source:
  end_turn: 0
  session_id: seed-4d8543dbcb9985e9
  start_turn: 0
tags:
- etl
- latency
- ops
title: 'Nightly ETL latency regression: baseline and observed runs'
type: fact
---

Nightly ETL pipeline that builds the orders_mart has regressed from ~4 hours to ~7 hours over the last 3 days. Baseline behavior: the pipeline starts at 02:00 and historically finished around 06:00 (approx. 4h). Current behavior: runs now finish around 09:00 (approx. 7h). I first noticed the jump on the run for 2026-02-03, which finished at 09:10. This latency increase is the primary operational symptom prompting investigation and remediation planning.