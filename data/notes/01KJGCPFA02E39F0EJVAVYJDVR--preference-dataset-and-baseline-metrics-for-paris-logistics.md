---
created_at: '2026-02-27T20:30:00Z'
entities:
- Paris logistics assistant
- in-house 7B model
- annotators
- A100
id: 01KJGCPFA02E39F0EJVAVYJDVR
language: en
source:
  end_turn: 2
  session_id: seed-eee7661285d2f721
  start_turn: 0
tags:
- preference-data
- baseline
- annotators
- dataset-split
- resources
title: Preference dataset and baseline metrics for Paris logistics assistant
type: fact
---

I have 2,400 labelled preference pairs collected Jan–Feb 2026 for the Paris logistics assistant, annotated by 12 people. Ops reports ~80% of those preferences concern tone/clarity and ~20% concern factual routing decisions. Mean annotator disagreement across the set is 22%. I will reserve 400 preference pairs for validation (to match the human A/B evaluation set) and use the remaining 2,000 pairs for training experiments. The current baseline win-rate on the 400 A/B human eval set is 48% versus the editor reference; that measurement date is 2026-02-20. The production baseline for critical-intent routing accuracy was recorded on 2026-02-10 and will be used to measure regressions. Infrastructure constraints: four A100 GPUs are available and the compute budget is roughly 8 GPU-days. Risk tolerance is low: any regression that causes incorrect routing for high-priority shipments triggers an immediate rollback. Decision deadline is two weeks out: 2026-03-12. These dataset and baseline numbers are fixed inputs for designing experiments and acceptance criteria.