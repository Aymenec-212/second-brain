---
created_at: '2026-02-20T20:30:00Z'
entities:
- SRE
- Sam
- infra
id: 01KHYBXEA0KEYXYETMGZTRGF4S
language: en
source:
  end_turn: 9
  session_id: seed-d490bfd09772dd8c
  start_turn: 9
tags:
- signoff
- ops
- sre
- stakeholders
title: 'Open task: confirm sign-off and production rollout owner / pager contacts'
type: task
---

Outstanding operational question to resolve before production rollout: confirm who formally signs off on the rollout and who will run/own the production rollout steps and on-call pager responsibilities for critical alerts. Current plan: I (Sam) own the application implementation and execution of the feature-flagged rollout; infrastructure will provision the managed Redis. But sign-off authority (who gives the green light at each rollout step) and the production incident contact (which SRE rotation/pager will handle critical alerts during rollout) are not yet finalized. Action items: (1) list sign-off approvers (product manager, SRE lead, infra lead), (2) assign the SRE pager contact and rotation for the rollout window 2026-02-23 to 2026-03-13, (3) confirm Slack channel and pager routing for warnings vs criticals. Target to close these confirmations before enabling production alerts at the 20% rollout step.