---
created_at: '2026-05-30T20:30:00Z'
entities:
- SyncVectorEnv
- numpy
- SeedSequence
id: 01KSX98KA03CFBVRE9FVEBW938
language: en
source:
  end_turn: 4
  session_id: seed-ceb7fcbdee356a98
  start_turn: 0
tags:
- vectorized
- rng
- performance
- seed
title: Vectorized environments and RNG seeding design (SyncVectorEnv-like lightweight
  wrapper)
type: idea
---

Vectorization and deterministic seeding plan: aim to provide a lightweight SyncVectorEnv-like wrapper (numpy-backed) that can run N envs in parallel in a single process for throughput. The wrapper should mirror Gymnasium.vector behavior sufficiently for standard training loops but avoid full generality to save implementation time. Deterministic RNG across vectorized envs is important: use numpy.random.SeedSequence to derive per-env child seeds from a base seed; instantiate each env's RNG with numpy.random.default_rng(child_seed) so behavior is reproducible and independent per environment. For tests, use explicit seeds 42 and 2026 and for vectorized equivalence tests spawn seeds 42..45 for 4 envs. If building a robust vectorized wrapper costs >16 h, postpone it to v0.2 and provide a simple for-loop example in examples/ showing how to step multiple envs in batch. Performance target: for small grids aim for ~10k steps/sec single-core; add a benchmark script benchmarks/steps_per_sec.py to measure and log the throughput. Ensure the vectorized wrapper shares the same API (reset/step/seed) and offers a deterministic batched seed interface.