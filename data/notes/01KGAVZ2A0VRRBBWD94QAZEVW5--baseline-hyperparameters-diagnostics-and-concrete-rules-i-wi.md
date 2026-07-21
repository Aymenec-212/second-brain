---
created_at: '2026-01-31T20:30:00Z'
entities:
- ParTrans-v0
id: 01KGAVZ2A0VRRBBWD94QAZEVW5
language: en
source:
  end_turn: 4
  session_id: seed-ca910916a8082c0c
  start_turn: 2
tags:
- baseline
- hyperparameters
- diagnostics
- kl
- logging
title: Baseline hyperparameters, diagnostics, and concrete rules I will commit to
type: decision
---

Baseline training hyperparameters and diagnostics to use as the team's default: - batch_timesteps = 2048; minibatch_size = 64; epochs_per_batch = 10. - optimizer lr (baseline) = 3e-4; epsilon (clip) = 0.2; advantage_norm = True (normalize advantages per-batch). - seeds: [11,13,17,23,29] (fixed). Diagnostics and logging to compute every epoch/minibatch: - mean_return(t) logged per 1k timesteps. - AUC computed at 100k intervals (AUC@1M is primary metric). - mean_KL@epoch and max_KL@epoch, where per-minibatch KL estimate = mean(old_logprob - new_logprob) across samples in the minibatch; take mean and max across minibatches for the epoch. - fraction_clipped@epoch = fraction of samples where r ∉ [1-ε,1+ε]. - wallclock time per 1M timesteps. - save checkpoints every 200k timesteps and keep the best checkpoint by AUC@1M. Operational targets: aim for mean KL per update ≈ 0.01; perform in-epoch early stopping (see next note) when KL indicates runaway updates.