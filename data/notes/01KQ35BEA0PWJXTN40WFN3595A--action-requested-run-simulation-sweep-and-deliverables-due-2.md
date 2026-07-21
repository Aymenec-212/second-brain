---
created_at: '2026-04-25T20:30:00Z'
entities:
- Cairn
id: 01KQ35BEA0PWJXTN40WFN3595A
language: en
source:
  end_turn: 10
  session_id: seed-84923c99c7de0aab
  start_turn: 10
tags:
- task
- simulation
- deliverables
- power-analysis
- notebook
- deadline
title: 'Action requested: run simulation sweep and deliverables due 2026-05-05'
type: task
---

Task assigned: run a simulation sweep over the 2.4M trip logs comparing contextual Thompson Sampling and UCB with exploration bonus = beta / sqrt(n_r) for beta in {0.1, 0.3, 0.5}. Deliverables (due 2026-05-05): (a) expected mean trip-time saved (seconds) for each algorithm/beta with 95% confidence intervals; (b) delta in on-time % (impact on guardrail); (c) change in route utilization entropy (coverage metric); (d) false-positive risk table showing instances where exploration recommends unsafe routes (must be zero in production, but quantify any simulated near-misses and reasons); (e) a short, runnable Python notebook that implements contextual Thompson Sampling and UCB on the provided logs (use Gaussian priors; include the exploration bonus term beta/sqrt(n_r)); and (f) a statistical power check showing required sample size (and expected detection power) to detect a 2% mean-time reduction given the observed variance in the logs. Acceptance criteria: simulations must show no meaningful degradation of on-time % (>=98%), acceptable risk profile for cold routes, and reasonable expected lift before approving the 2026-05-10 A/B rollout. After sims complete, notify Jules and Claire for review.