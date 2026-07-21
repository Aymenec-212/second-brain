---
created_at: '2026-05-20T20:30:00Z'
entities:
- Sam
id: 01KS3H9DA0B4F4H138JD2MARDG
language: en
source:
  end_turn: 6
  session_id: seed-6af5ee8a4e680b90
  start_turn: 6
tags:
- outsourcing
- db
- fallback
- cost
title: External DB incident provider fallback option
type: idea
---

Idea/fallback: contract an external provider to handle critical database incidents overnight as a stopgap while the team is small or while hiring an SRE. Cost estimate: approximately €1,000/month. Use case: provider handles high-severity database incidents off-hours that the team cannot safely cover without compromising sleep/family time. Include this option as part of the pilot proposal and present a short cost-benefit comparison: recurring external provider cost vs. increased on-call pay (e.g., €100–150/week per engineer) vs. accelerated SRE hire (one-time hiring and recurring salary). If pilot KPIs indicate database incidents are the main driver of pages or long MTTRs, list the external provider as a near-term mitigation to avoid repeated severe nights while recruiting.