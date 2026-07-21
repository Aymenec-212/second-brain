---
created_at: '2026-05-20T20:30:00Z'
entities:
- Sam
- PagerDaemon
id: 01KS3H9DA0B4F4H138JD2MARD9
language: en
source:
  end_turn: 4
  session_id: seed-6af5ee8a4e680b90
  start_turn: 3
tags:
- alerts
- routing
- severity
- automation
title: Technical design for dinner window and severity definitions
type: task
---

Technical plan: enforce the 19:00–20:30 protected dinner window both by routing and by policy. Implementation details: add a numeric severity field to all alerts; set routing rules so only alerts tagged Sev1 get SMS during 19:00–20:30 while Sev2 and below are Slack-only or buffered. Concrete severity thresholds defined for the pilot: CPU >90% sustained for >5 minutes => Sev2; memory OOM events => Sev1; database unavailability (loss of quorum / unavailable primary) => Sev1. Routing automation: use PagerDaemon to enforce the SMS/Slack routing and automated escalations. Implementation deadline: I will implement routing by 2026-05-27. Monitoring: ensure alerts include the numeric severity and that runbook links are included. Acceptance check: during a pre-pilot test window confirm Sev1 SMS arrives, Sev2 does not SMS during dinner window, and alerts contain severity metadata. Document the routing rules and thresholds in a single alert-routing spec stored in the team repo before 2026-05-27.