---
created_at: '2026-01-31T20:30:00Z'
entities:
- PPO
- Schulman et al. 2017
id: 01KGAVZ2A0VRRBBWD94QAZEVW1
language: en
source:
  end_turn: 0
  session_id: seed-ca910916a8082c0c
  start_turn: 0
tags:
- ppo
- objective
- clipping
- intuition
- advantage
- schulman2017
title: PPO L_CLIP objective and clipping intuition
type: idea
---

The PPO clipped surrogate objective I want to keep front-and-center is L_CLIP(θ) = E[min(r(θ) A, clip(r(θ), 1-ε, 1+ε) A)] with r(θ) = π_θ(a|s) / π_old(a|s). Common practical default from Schulman et al. (2017) is ε = 0.2. Intuition: for a sample with positive advantage A>0, the unconstrained term rA encourages increasing r; clipping replaces r by min(r,1+ε) once r exceeds 1+ε, so the objective stops improving beyond that point and the gradient contribution from that sample for further increasing r is zero. Symmetrically for A<0 the objective stops improving when r falls below 1-ε. Functionally, clipping caps how much any single sample can push the policy in the direction that improves the batch surrogate objective. This is a per-sample, per-update hard cap on the advantage-weighted probability ratio — cheap to compute and easy to parallelize, which is why it is attractive in practice.