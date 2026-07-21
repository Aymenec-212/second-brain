---
created_at: '2026-02-27T20:30:00Z'
entities:
- DPO
- Reward model
- PPO
- A100
id: 01KJGCPFA02E39F0EJVAVYJDVT
language: en
source:
  end_turn: 4
  session_id: seed-eee7661285d2f721
  start_turn: 3
tags:
- experiments
- compute
- scheduling
- dpo
- rlhf
title: Experiment schedule, compute/time estimates, and parallelization plan
type: task
---

Planned experiment schedule and compute estimates must fit 4 A100s and ~8 GPU-days total. Estimated runtimes: DPO is expected to be fastest — roughly 12–24 hours wall-clock on available hardware. RLHF path breaks into two main steps: (a) train a reward model (RM) on the 2,000 prefs (with cross-validation) — RM training is estimated to add ~1–4 GPU-days depending on optimization and checkpointing choices and risk of overfitting, and (b) PPO fine-tuning which is another ~1–4 GPU-days (PPO time depends on rollout length and batch size). Concrete parallelization plan: start DPO immediately (fast), and start RM development in parallel only if spare compute permits or if we want to overlap to save total calendar time; otherwise postpone RM until DPO results are in. Because the overall compute budget is only ~8 GPU-days, avoid running a full RM+PPO pipeline in parallel with DPO unless short RM runs (sanity checks) are used. Validation plan: use the reserved 400 preference val set and a 400-sample A/B human eval (same set) to measure win-rate changes. If DPO produces >=+8 percentage points and meets safety gates, prefer shipping to minimize moving parts. If it fails routing, pursue targeted RLHF after augmenting routing data. Schedule constraint: final decision by 2026-03-12; targeted RLHF finish date if needed is 2026-03-26.