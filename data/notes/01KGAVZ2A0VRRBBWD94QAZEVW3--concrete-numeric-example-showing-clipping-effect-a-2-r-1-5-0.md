---
created_at: '2026-01-31T20:30:00Z'
entities:
- PPO
id: 01KGAVZ2A0VRRBBWD94QAZEVW3
language: en
source:
  end_turn: 0
  session_id: seed-ca910916a8082c0c
  start_turn: 0
tags:
- example
- ppo
- clipping
- calculation
title: Concrete numeric example showing clipping effect (A=2, r=1.5, ε=0.2)
type: fact
---

Worked example to keep in mind when explaining to the team: let advantage A = 2, observed ratio r = 1.5, and ε = 0.2. Unclipped contribution to the surrogate would be r·A = 1.5·2 = 3.0. Clipping caps r at 1+ε = 1.2, so the surrogate uses 1.2·2 = 2.4 instead. Practically, the per-sample objective stops improving as r increases above 1.2, so the gradient contribution from that sample with respect to policy parameters for further increasing r is zero. This shows how clipping caps per-sample policy improvement. Important caveat: even if many samples are clipped individually, the parameter update can still be large in aggregate (many small changes can sum to a large parameter shift) and the overall (mean or max) KL divergence between π_old and π_new can still grow significantly.