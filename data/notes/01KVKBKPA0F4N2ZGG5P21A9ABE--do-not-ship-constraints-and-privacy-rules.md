---
created_at: '2026-06-20T20:30:00Z'
entities:
- Mapbox
- third-party SDKs
id: 01KVKBKPA0F4N2ZGG5P21A9ABE
language: en
source:
  end_turn: 8
  session_id: seed-3de9806b270bb9df
  start_turn: 8
tags:
- constraints
- privacy
- compliance
- do-not-ship
title: '''Do not ship'' constraints and privacy rules'
type: decision
---

Absolute do-not-ship constraints to enforce pre-launch: 1) Do not use any paid per-download tile provider or third-party SDK that charges per-user downloads — this would create variable costs and break marginal economics. 2) Do not ship offline routing in v1; route/index functionality must be explicitly scheduled for v2. 3) Do not collect or upload user GPS tracks by default; any sharing of GPS tracks requires explicit opt-in from the user. 4) Keep the launch price at 4.99 EUR/month with no immediate discounts. Enforce these constraints in acceptance criteria for each Jira ticket and gating criteria for release review meetings.