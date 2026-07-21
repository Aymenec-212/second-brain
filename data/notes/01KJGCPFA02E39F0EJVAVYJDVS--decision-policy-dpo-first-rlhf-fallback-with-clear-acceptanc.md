---
created_at: '2026-02-27T20:30:00Z'
entities:
- DPO
- RLHF
- Reward model
- PPO
- Paris logistics assistant
id: 01KJGCPFA02E39F0EJVAVYJDVS
language: en
source:
  end_turn: 9
  session_id: seed-eee7661285d2f721
  start_turn: 0
tags:
- decision
- dpo
- rlhf
- release-policy
- deadlines
title: 'Decision policy: DPO-first, RLHF fallback with clear acceptance criteria'
type: decision
---

Decision: run Direct Preference Optimization (DPO) first on the in-house 7B Paris logistics assistant using the 2,000 training preferences and 400 held-out validation preferences; if DPO meets both quality and safety gates, ship; otherwise fall back to a targeted RLHF workflow. Acceptance criteria to ship after DPO: (1) validation human-eval win-rate increases by at least 8 percentage points versus baseline (baseline 48% → target >=56% on the 400 A/B set), (2) no more than a 0.5 percentage-point absolute drop in critical-intent accuracy compared to the production baseline (2026-02-10), and (3) zero misrouting failures in a 1,000-case high-priority sample and zero single misrouting in a 24-hour simulated batch of 1,000 such cases. Rollout policy: if DPO passes, do a canary at 5% traffic for 48 hours, monitor the above thresholds, then full roll after 7 days with no regressions. If DPO fails specifically on routing (but improves tone), trigger the routing-augmentation plan (+1,000 routing-focused prefs) and run RLHF with the targeted data, aiming to finish the RLHF path by 2026-03-26. Keep all dates, counts and thresholds recorded exactly as above.