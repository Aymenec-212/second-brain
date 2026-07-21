---
created_at: '2026-07-08T20:30:00Z'
entities:
- Lucas
- Maya
- team
id: 01KX1PRMA097SE45AZ6M2WJA5R
language: en
source:
  end_turn: 0
  session_id: seed-f1db84c97011917b
  start_turn: 0
tags:
- cairn
- bugs
- triage
- security
- ci
- postmortem
title: 'Cairn bug triage summary: CA-117, CA-101, CA-123, CA-130'
type: fact
---

I maintain an active bug triage list for the Cairn beta with four current items and their impacts, owners, and immediate next steps. CA-117: authentication token leak during websocket reconnection. Reproducible on staging after three reconnects. Impact: P0 (security-level). Owner: Lucas. Action: hotfix to rotate token on reconnect and add a regression test. Proposed ETA: 2026-07-10 EOD. Likely release blocker. CA-101: search indexing returns stale results after bulk import. Repro is intermittent. Impact: P1. Owner: Maya. Workaround: run the reindex job. Planned fix scoped into the next sprint with target 2026-07-15. CA-123: flaky CI test that is order-dependent. Impact: P2. No single owner assigned — team-level. Immediate action: mark/skip flaky test in CI to stop noise; investigate root cause later. CA-130: rare data corruption in a batch job when a DB timeout coincides with a retry. Impact: P1 and requires a postmortem and mitigation plan. Tentative postmortem date noted. These are the facts I need available when deciding release blocks and assigning final owners and deadlines.