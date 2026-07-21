---
created_at: '2026-01-31T20:30:00Z'
entities:
- ppo/clip-trust-region-jan31
- ppo-trustregion-jan26
- ParTrans-v0
id: 01KGAVZ2A0VRRBBWD94QAZEVW7
language: en
source:
  end_turn: 6
  session_id: seed-ca910916a8082c0c
  start_turn: 6
tags:
- checklist
- repo
- config
- experiment
title: Experiment config checklist to paste into repo (copy for configs)
type: task
---

I will copy this checklist verbatim into the experiment config in the repo: - branch: ppo/clip-trust-region-jan31 - run_start: 2026-02-01, run_end: 2026-02-14 - env: ParTrans-v0 - seeds: [11,13,17,23,29] - gpus: 8 (2 nodes x 4 GPUs) - baseline hparams: batch_timesteps=2048, minibatch=64, epochs=10, lr=3e-4, ε=0.2, advantage_norm=True - ablation grid: ε ∈ {0.1,0.2,0.3}, lr ∈ {1e-4,3e-4,1e-3} - diagnostics/logs: mean_return@1k, AUC@100k, mean_KL@epoch, max_KL@epoch, frac_clipped@epoch, wallclock@1M - KL estimate: mean_KL_batch = mean(old_logprob - new_logprob) per minibatch - early-stop rule (within-epoch): if mean_KL_epoch > 0.03 stop further epochs on this batch - checkpoint: save every 200k timesteps, retain best by AUC@1M - acceptance criteria: choose PPO-clip if AUC@1M >= baseline_AUC*1.05 and std_return <= baseline_std*0.9; otherwise test KL-penalty β ∈ {0.1,1,10} then TRPO fallback - repo notes: commit code and config to branch, tag run in WandB project 'ppo-trustregion-jan26'  (I will paste this block verbatim into the run config files.)