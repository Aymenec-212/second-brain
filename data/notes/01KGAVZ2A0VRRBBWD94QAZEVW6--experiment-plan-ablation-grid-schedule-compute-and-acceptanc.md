---
created_at: '2026-01-31T20:30:00Z'
entities:
- ppo/clip-trust-region-jan31
- ppo-trustregion-jan26
- ParTrans-v0
- TRPO
id: 01KGAVZ2A0VRRBBWD94QAZEVW6
language: en
source:
  end_turn: 4
  session_id: seed-ca910916a8082c0c
  start_turn: 2
tags:
- experiment
- ablation
- schedule
- acceptance-criteria
- wandb
title: 'Experiment plan: ablation grid, schedule, compute, and acceptance criteria'
type: task
---

Concrete experiment plan to run as the first pass: - Ablation grid: ε ∈ {0.1, 0.2, 0.3} × lr ∈ {1e-4, 3e-4, 1e-3}. Keep batch=2048, minibatch=64, epochs=10, seeds=5. - Metrics to measure per experiment: mean episodic return over time; AUC@1M (primary); time-to-90%-of-final; standard deviation across seeds (stability); mean and max KL per-update; fraction_clipped per epoch; wallclock per 1M timesteps. - Acceptance criteria / escalation: prefer PPO-clip if AUC@1M ≥ baseline_AUC * 1.05 (≥5% improvement) and std_return ≤ baseline_std * 0.9 (≥10% reduction) after 1M timesteps across seeds. If not met, run KL-penalty variant with β ∈ {0.1,1,10} and, if needed, fallback to TRPO. - Practical safeguards: use KL-based early stopping within an update if mean_KL_epoch > 0.03 (stop the remaining epochs on the current batch and proceed to next rollout); log mean and max KL and fraction clipped each epoch. - Compute and schedule: run_start = 2026-02-01, run_end = 2026-02-14; GPUs: 8 (2 nodes × 4 GPUs). Branch for code: ppo/clip-trust-region-jan31. WandB project: 'ppo-trustregion-jan26'. Save checkpoints every 200k timesteps and keep best-by-AUC.