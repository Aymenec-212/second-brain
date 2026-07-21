---
created_at: '2026-05-30T20:30:00Z'
entities:
- tinygrid
- grid_env.py
- wrappers.py
- examples
- convert_obs
id: 01KSX98KA03CFBVRE9FVEBW937
language: en
source:
  end_turn: 6
  session_id: seed-ceb7fcbdee356a98
  start_turn: 2
tags:
- implementation
- structure
- design
title: Implementation plan and code organization (single-file env first, clear separation)
type: task
---

Concrete implementation plan and file responsibilities: start with a single-file readable implementation at tinygrid/envs/grid_env.py containing the core Env class and its logic. Keep a strict separation between environment logic and wrappers—place convenience wrappers (e.g., observation flattening, partial-observability views) in tinygrid/wrappers.py. Expose a factory function tinygrid.make(name='TinyGrid-4x4-v0', cfg=...) at package top-level for easy instantiation. Provide helper utilities in examples/ and include a convert_obs(obs) utility for the SB3 example that converts integer grids into an input usable by standard policies (one-hot or embedding + small CNN/MLP). Tests will live in tests/, e.g. tests/test_transitions.py, tests/test_seeding.py, tests/test_vectorized.py. Keep code explicit and small for readability: the single-file env plus a small set of wrappers and helpers. Use numpy.random.default_rng for RNG and structure functions so that reset(seed=...) sets RNG via this RNG object. Add entrypoints in pyproject.toml for any example scripts if useful. The first commit will be a skeleton with these files in place; then implement grid_env.py tonight.