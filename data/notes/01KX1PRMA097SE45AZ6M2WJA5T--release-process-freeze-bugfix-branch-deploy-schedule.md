---
created_at: '2026-07-08T20:30:00Z'
entities:
- Marc
- Ops
id: 01KX1PRMA097SE45AZ6M2WJA5T
language: en
source:
  end_turn: 8
  session_id: seed-f1db84c97011917b
  start_turn: 2
tags:
- release
- ops
- freeze
- branch
- deploy
title: 'Release process: freeze, bugfix branch, deploy schedule'
type: task
---

Final release process and constraints to lock in for the 2026-07-11 deploy: - Feature freeze: no feature merges after 2026-07-09 18:00. Only bugfixes are allowed. - Branching and deploy: Ops (Marc) will prepare a bugfix-only branch and manage the release tagged release/2026-07-11. The deploy window is 2026-07-11 (exact time to be set in the calendar invite). - Blocking criteria: if CA-117 is not resolved (Lucas's hotfix and tests complete) by 2026-07-10 EOD, revert the websocket feature and do not deploy on 2026-07-11. - Communication: I will publish a README for beta testers with known issues and workarounds by 2026-07-09 12:00 and Maya will deliver release notes by the same noon deadline. - Rollback plan: Maya to produce a rollback-safe plan for CA-101 in case index staleness causes issues post-deploy. - CI hygiene: temporarily skip CA-123 (flaky) in CI to keep pipeline reliable during the release. These tasks are timeboxed; Ops handles branch/deploy mechanics, and I own enforcing the freeze.