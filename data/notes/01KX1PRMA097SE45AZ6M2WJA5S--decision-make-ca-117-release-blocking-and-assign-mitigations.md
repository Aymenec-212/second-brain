---
created_at: '2026-07-08T20:30:00Z'
entities:
- Lucas
- Maya
- Marc
- team
id: 01KX1PRMA097SE45AZ6M2WJA5S
language: en
source:
  end_turn: 2
  session_id: seed-f1db84c97011917b
  start_turn: 1
tags:
- release
- blocker
- cairn
- security
- assignments
title: 'Decision: Make CA-117 release-blocking and assign mitigations'
type: decision
---

Decision: CA-117 (auth token leak in websocket reconnection) is a release-blocking P0 and must be fixed before the 2026-07-11 deploy. Concrete mitigations and assignments: Lucas is responsible for a hotfix that rotates the token on reconnect, plus unit and staging tests; ETA 2026-07-10 EOD. If Lucas cannot complete this hotfix by that deadline, the websocket feature must be reverted and the deploy blocked. CA-130 (rare data corruption) is high priority but not blocking the 2026-07-11 deploy; I scheduled a postmortem on 2026-07-15 and will produce mitigation steps after that review. Additional immediate assignments: Maya must prepare a rollback-safe plan for CA-101 and draft release notes; the team will skip/mark CA-123 flaky test in CI today. These are the binding decisions I will use to lock the release.