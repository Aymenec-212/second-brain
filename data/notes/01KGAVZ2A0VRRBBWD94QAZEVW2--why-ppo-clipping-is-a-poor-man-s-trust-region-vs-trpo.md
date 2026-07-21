---
created_at: '2026-01-31T20:30:00Z'
entities:
- PPO
- TRPO
id: 01KGAVZ2A0VRRBBWD94QAZEVW2
language: en
source:
  end_turn: 0
  session_id: seed-ca910916a8082c0c
  start_turn: 0
tags:
- trust-region
- trpo
- kl
- ppo
- interpretation
title: Why PPO clipping is a 'poor man's trust region' (vs TRPO)
type: idea
---

Characterize PPO-clip as a 'poor man's trust region' precisely: clipping enforces a hard cap on each sample's contribution in probability-ratio space, but it is not a KL constraint and does not implement a metric-aware projection in policy-parameter space. TRPO explicitly constrained the expected KL (E[KL(π_old || π_new)] ≤ δ, e.g., δ≈0.01–0.03) and used natural-gradient-flavored steps (conjugate gradient, trust-region projection) that respect the policy manifold geometry. PPO-clip instead performs a local, per-sample projection in ratio-space: it prevents any sample from contributing improvement beyond r ∈ [1-ε,1+ε], which often produces similar practical stability without the compute and implementation complexity of TRPO. The caveat is that clipping is a heuristic: it can leave aggregate/average KL unbounded and cannot guarantee worst-case KL behavior across the batch or dataset.