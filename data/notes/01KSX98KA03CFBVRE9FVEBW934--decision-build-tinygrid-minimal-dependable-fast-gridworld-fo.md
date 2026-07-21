---
created_at: '2026-05-30T20:30:00Z'
entities:
- tinygrid
- Sam
- '2026-05-30'
id: 01KSX98KA03CFBVRE9FVEBW934
language: en
source:
  end_turn: 6
  session_id: seed-ceb7fcbdee356a98
  start_turn: 0
tags:
- project
- decision
- tinygrid
- roadmap
title: 'Decision: build tinygrid — minimal, dependable, fast gridworld for RL'
type: decision
---

Decision log (2026-05-30): I, Sam (31, backend/ML engineer at a Paris logistics startup), decided to build a small gridworld library called "tinygrid" to use as a hands-on, minimal environment for testing RL algorithms. Core goals are explicit: keep the project minimal, dependable, and fast to iterate on. Baseline scope for v0.1.0: a pure-Python + numpy implementation targeting Python 3.11+; strict Gymnasium-compatible API (reset, step, render, close, seed); a couple default environments (TinyGrid-4x4-v0 and TinyGrid-8x8-v0); action space Discrete(5); observations as integer grids (H x W) or flattened vectors; max_episode_steps default 200. I will prioritize deterministic RNG behavior and reproducible unit tests. Timeline and commitment: prototype in 1 week (2026-05-30 -> 2026-06-06), polish/docs/CI/packaging in a second week to target release v0.1.0 by 2026-06-14. I can allocate ~12 hours/week. If scope grows, I will cut optional features (notably RGB rendering and the vectorized env) and defer them to v0.2. Next concrete step: create the GitHub repo skeleton tonight and start implementing tinygrid/envs/grid_env.py.