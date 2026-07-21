---
created_at: '2026-01-31T20:30:00Z'
entities:
- PPO
id: 01KGAVZ2A0VRRBBWD94QAZEVW4
language: en
source:
  end_turn: 2
  session_id: seed-ca910916a8082c0c
  start_turn: 0
tags:
- failure-modes
- ppo
- stability
- remedies
title: Failure modes for PPO-clip and straightforward mitigations
type: idea
---

List of common failure modes to watch for and pragmatic mitigations: 1) Advantage scale / high variance: raw large-magnitude advantages make clipping less effective and can lead to unstable updates. Mitigation: normalize advantages per-batch (subtract mean, divide by std) before computing the objective. 2) Very small batch size or too many epochs over the same batch: leads to overfitting to the batch so clipped ratios are not protective. Mitigation: keep reasonably large batch (e.g., 2048 timesteps) and limit epochs (e.g., 10) or use early stopping. 3) Non-stationary data / old policy mismatch: if the data in the replay is stale relative to the policy, ratios can explode. Mitigation: avoid stale data and keep rollouts in lock-step with updates. 4) Excessively large learning rate: parameter updates then move far even when many ratios are clipped. Mitigation: sweep lr; baseline 3e-4 but test lower/higher. 5) Inappropriate ε: too large (≥0.3) weakens clipping; too small (≈0.05) makes optimization overly conservative. Mitigation: sweep ε (e.g., 0.1, 0.2, 0.3) and monitor KL and performance. Also proactively log mean and max KL, fraction of clipped ratios, and ratio histograms to identify tail effects.