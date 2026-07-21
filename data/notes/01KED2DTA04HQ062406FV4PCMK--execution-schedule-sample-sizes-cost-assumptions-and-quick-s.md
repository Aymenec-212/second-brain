---
created_at: '2026-01-07T20:30:00Z'
entities:
- Jan 8
- Jan 9
- Jan 10
- €3.5/hr node rate
id: 01KED2DTA04HQ062406FV4PCMK
language: en
source:
  end_turn: 9
  session_id: seed-080a3566d9e37509
  start_turn: 8
tags:
- schedule
- cost-estimate
- benchmark
title: Execution schedule, sample sizes, cost assumptions, and quick sanity math
type: task
---

Planned execution timeline and measurement conventions: - Run dates: start Jan 8 with the 1B draft for k=2 and k=4; optionally run 3B drafts or k=8 on Jan 9 depending on results. - Sample sizes: 100k tokens per configuration, sampled from Oct–Dec 2025 logs and stratified by customer and prompt length. - Review/decision: commit to reviewing and deciding next steps on Jan 10. - Cost conversion: record GPU raw time per run and convert to EUR using the current node rate €3.5/hr to compute cost per 1M tokens (and cost per 1k tokens). - Sanity math / expectation: draft forward is ~5% of a 70B forward. Example expectation: with k=4 and a 70% block acceptance rate, you should expect roughly a ~2× reduction in expensive big-model forwards (paper-like claim), which should translate to a noticeable p95 drop. But real measurement is required — specifically measure rollback frequency and rollback-induced spikes. Decision criteria for adoption remain p95 ≤150 ms and cost ≤€0.15 / 1k tokens, plus low rollback spike incidence.