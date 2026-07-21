---
created_at: '2026-04-25T20:30:00Z'
entities:
- Jules
- Claire
id: 01KQ35BEA0PWJXTN40WFN35959
language: en
source:
  end_turn: 8
  session_id: seed-84923c99c7de0aab
  start_turn: 8
tags:
- constraints
- safety
- override
- simulation
- timeline
- deployment
title: Hard constraints, override treatment, simulation sweep and go/no-go timeline
type: decision
---

Firm decision: enforce hard filters in production — never suggest a route that exceeds baseline distance by >10% or has safety_score < 0.9. Driver override policy: overrides remain allowed in the UI; treat an override as an immediate strong negative reward (user decided on -300 seconds as the penalty, which should be mapped to the normalized reward space) and log each override for ops review. Simulation and deployment plan: 1) Run a simulation sweep (beta in {0.1, 0.3, 0.5}) comparing contextual Thompson Sampling vs UCB across the 2.4M logs, with results broken down by route cohort (cold/medium/hot). Produce expected mean-time change, on-time %, route entropy, and a specific risk table for the 80 low-data routes. Deadline for simulation results: 2026-05-05. 2) If simulations meet safety and KPI criteria, schedule an A/B deploy starting 2026-05-10 for 8 weeks with daily batch updates. Communication: simulation results must be reviewed with Product owner Jules and Ops lead Claire before deployment. Operational safeguards: clamp any exploration bonus so it cannot cause candidates to pass hard filters; maintain a rollback plan and monitoring alerts for on-time % drops.