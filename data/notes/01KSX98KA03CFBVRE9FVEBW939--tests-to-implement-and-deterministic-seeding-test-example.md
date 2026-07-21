---
created_at: '2026-05-30T20:30:00Z'
entities:
- pytest
- tinygrid
- tests/test_seeding.py
- tests/test_vectorized.py
id: 01KSX98KA03CFBVRE9FVEBW939
language: en
source:
  end_turn: 6
  session_id: seed-ceb7fcbdee356a98
  start_turn: 0
tags:
- testing
- seeding
- unit-tests
- vectorized
title: Tests to implement and deterministic-seeding test example
type: task
---

Testing checklist and concrete example for seeding determinism: implement unit tests that cover transition correctness, reward shapes, episode termination conditions, deterministic seeding behavior, and equivalence between single-env stepping and the vectorized wrapper. Specific seeding test pattern to implement in tests/test_seeding.py: 1) env = make('TinyGrid-4x4-v0'); obs1 = env.reset(seed=42); seq1 = [env.step(0)[0] for _ in range(10)] 2) env2 = make('TinyGrid-4x4-v0'); obs2 = env2.reset(seed=42); seq2 = [env2.step(0)[0] for _ in range(10)] 3) assert seq1 == seq2. For vectorized equivalence (tests/test_vectorized.py): instantiate 4 independent single envs seeded with 42..45, run them in lockstep for several steps and record observations/terminations/rewards; then instantiate SyncVector wrapper seeded with a base seed and compare outputs after the same sequence of actions. Also test that max_episode_steps (default 200) triggers done=True at the expected step. Use pytest and assert deterministic behavior. Coverage target for CI is >= 80%.