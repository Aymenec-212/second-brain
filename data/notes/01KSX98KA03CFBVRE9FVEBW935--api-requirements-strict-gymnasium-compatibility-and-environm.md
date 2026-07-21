---
created_at: '2026-05-30T20:30:00Z'
entities:
- Gymnasium
- tinygrid
- numpy
id: 01KSX98KA03CFBVRE9FVEBW935
language: en
source:
  end_turn: 2
  session_id: seed-ceb7fcbdee356a98
  start_turn: 0
tags:
- api
- gymnasium
- observation-space
- action-space
title: 'API requirements: strict Gymnasium compatibility and environment interface'
type: fact
---

API and compatibility constraints to implement exactly: the environment must implement the Gymnasium-compatible interface (reset, step, render, close, seed). Use gymnasium.spaces types for observation_space and action_space so libraries like stable-baselines3 accept the env without adapters. Concrete space definitions: action_space = Discrete(5) representing UP, DOWN, LEFT, RIGHT, NOOP. observation_space should be a Box describing integer grid arrays: Box(low=0, high=K, shape=(H, W), dtype=np.int64) where K is the number of cell types; allow a Dict option for debug/stacked info, e.g. {'grid': Box(...), 'agent_pos': Box(...)}. The env should return observations as integer grids (H x W) by default, and provide an option to return flattened vectors. Render should support mode='rgb_array' (optional for v0.1) and mode='human' ASCII fallback. Max episode length default is 200 steps and must be enforced by the env (max_episode_steps). RNG must be deterministic via numpy.random.default_rng(seed); reset(seed=...) should set RNG state reproducibly. Target Python 3.11+; avoid C extensions.