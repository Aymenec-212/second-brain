---
created_at: '2026-02-27T20:30:00Z'
entities:
- deterministic test suite
- production logs
- canary
id: 01KJGCPFA02E39F0EJVAVYJDVW
language: en
source:
  end_turn: 8
  session_id: seed-eee7661285d2f721
  start_turn: 7
tags:
- safety
- testing
- monitoring
- rollout
title: Safety testing suites, monitoring, and rollback triggers
type: task
---

Safety test setup: run both deterministic and sampled production tests. Deterministic suite: 200 canonical high-priority scenarios created on 2026-02-15 covering known routing edge cases. Production sample: 1,000 recent production queries sampled from Feb 2026. Acceptance for deployment: zero misroutes in the 1,000 sampled recent-production queries and zero single misrouting in a 24-hour simulated batch of 1,000 high-priority cases. Post-deploy monitoring: log all model outputs for 14 days and perform automated pairwise comparisons against 5,000 recent production queries to detect regressions. Rollout policy: if DPO passes tests, perform a 5% traffic canary for 48 hours and monitor thresholds; only proceed to full rollout after 7 days with no regressions. Rollback triggers: any absolute drop >0.5 percentage points in critical-intent accuracy relative to the 2026-02-10 production baseline, or any confirmed misrouting on high-priority shipments as defined above, requires immediate rollback and investigation. Keep deterministic test suite, sample selection procedure, and logging time windows explicitly recorded to reproduce results.