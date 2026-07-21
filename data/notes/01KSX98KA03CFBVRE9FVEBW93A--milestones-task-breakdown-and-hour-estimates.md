---
created_at: '2026-05-30T20:30:00Z'
entities:
- tinygrid
- v0.1.0
id: 01KSX98KA03CFBVRE9FVEBW93A
language: en
source:
  end_turn: 4
  session_id: seed-ceb7fcbdee356a98
  start_turn: 4
tags:
- milestones
- schedule
- estimates
title: Milestones, task breakdown, and hour estimates
type: task
---

Concrete milestones with time estimates (I will track these against my 12 h/week availability): 1) Core environment and API plus ~6 unit tests — 6 hours. Deliverables: tinygrid/envs/grid_env.py, essential API, tests for transitions, rewards, termination, and seeding. 2) SB3 PPO example and README quickstart — 3 hours. Deliverables: examples/ppo_sb3.py, helper convert_obs(obs) for preprocessing, README with quickstart and usage. 3) CI basics (GitHub Actions)—lint (black, flake8), pytest, coverage reporting—and pre-commit hooks — 3 hours. 4) Packaging and PyPI config, create pyproject.toml (Poetry), configure release job, version bump to v0.1.0 and publish — 2 hours. 5) Optional work: render (rgb_array), benchmarks script, and vectorized wrapper — estimated 8 hours; mark as optional for v0.2 if required. Baseline planned work sums to 14 hours; optional 8 hours. With 12 h/week, baseline fits within one week, optional features can be done the following week. If implementation runs long, drop optional features first (no RGB rendering and no vectorized env for v0.1).