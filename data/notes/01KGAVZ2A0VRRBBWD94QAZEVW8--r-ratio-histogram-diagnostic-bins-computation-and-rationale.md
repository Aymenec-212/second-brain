---
created_at: '2026-01-31T20:30:00Z'
entities:
- PPO
id: 01KGAVZ2A0VRRBBWD94QAZEVW8
language: en
source:
  end_turn: 7
  session_id: seed-ca910916a8082c0c
  start_turn: 6
tags:
- diagnostic
- histogram
- r-distribution
- kl
- debugging
title: 'r-ratio histogram diagnostic: bins, computation, and rationale'
type: task
---

Add a histogram of the probability ratio r = π_new(a|s) / π_old(a|s) per epoch to capture tail behavior that fraction_clipped alone might miss. Suggested bins to log (can be coarse): [0, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.0+] — record counts and normalized frequencies per epoch and per-minibatch. Log summary stats: mean r, median r, 90th and 99th percentiles, and the max observed r. Rationale: even if the fraction of ratios outside [1-ε,1+ε] is small, a heavy tail (many samples with r ≫ 1+ε or ≪ 1-ε) can cause large KL or parameter shifts. The histogram will help diagnose whether clipping is silencing many extreme samples or whether there are persistent tails that require changing ε, reducing lr, increasing batch size, adding KL-penalty, or switching to TRPO. Implementation note: compute r using stored old_logprob and current_logprob (r = exp(new_logprob - old_logprob)) in a numerically stable way; log both counts and the fraction outside the clip interval each epoch so I can correlate tails with KL spikes and performance drops.