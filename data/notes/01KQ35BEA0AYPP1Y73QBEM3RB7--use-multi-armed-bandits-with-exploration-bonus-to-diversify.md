---
created_at: '2026-04-25T20:30:00Z'
entities:
- Cairn
id: 01KQ35BEA0AYPP1Y73QBEM3RB7
language: en
source:
  end_turn: 0
  session_id: seed-84923c99c7de0aab
  start_turn: 0
tags:
- bandits
- route-optimization
- exploration
- hypothesis
- cairn
- planning
title: Use multi-armed bandits with exploration bonus to diversify Cairn route suggestions
type: idea
---

Idea: apply multi-armed bandit methods to Cairn's route-suggestion system to prevent recycling the same top routes and to learn potentially underused yet better routes. Context: 120 active drivers, ~200 distinct routes in the network, and the app suggests up to 3 alternative routes per trip. Historical dataset: 2.4M logged trips since 2024-01-01; traffic is concentrated — the top 20% of routes account for ~70% of trips; 80 routes have fewer than 20 historical runs (cold). Business constraints: any suggested route must not exceed the baseline route distance by more than +10% and must have safety_score >= 0.9 (hard constraints). Hypothesis: adding a modest exploration bonus will increase route coverage and reduce congestion on popular routes, producing a net reduction in mean trip time (primary KPI) while maintaining on-time percentage >= 98% (guardrail). Candidate algorithms under consideration: contextual Thompson Sampling, UCB with exploration bonus proportional to 1/sqrt(n_r), and epsilon-greedy with decaying epsilon. Operational proposal: start with daily batch model updates and run offline simulations before any live test. Decision intention: run simulations, then open an A/B test starting 2026-05-10 for 8 weeks if simulations look safe.