---
created_at: '2026-05-20T20:30:00Z'
entities:
- Nora
- Marion
- PagerDaemon
id: 01KS3H9DA0B4F4H138JD2MARDE
language: en
source:
  end_turn: 10
  session_id: seed-6af5ee8a4e680b90
  start_turn: 9
tags:
- escalation
- sla
- incident
- postmortem
title: Escalation SLAs and post-incident process
type: decision
---

Escalation SLAs to include in runbooks and automation: for Sev1 incidents acknowledge within 15 minutes. If the incident is not resolved within 30 minutes escalate to the on-call lead (Nora) by phone. If unresolved after 90 minutes escalate to Marion. Automate these escalations using PagerDaemon by 2026-05-27. Additionally require a post-incident check-in: within 72 hours the team conducts a debrief to determine root causes and whether follow-up actions (changes to alerts, runbooks, or code) are required. All Sev1s must have a short incident summary in the incident log and an assigned owner for any follow-up action with an ETA. Document the escalation ladders and timing in each runbook and ensure PagerDaemon's escalation policy mirrors the documented SLAs. These rules reduce ambiguity under stress and ensure managerial awareness for prolonged outages.