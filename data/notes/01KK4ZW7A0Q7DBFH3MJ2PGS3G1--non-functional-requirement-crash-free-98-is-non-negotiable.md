---
created_at: '2026-03-07T20:30:00Z'
entities:
- Sentry
- device lab
id: 01KK4ZW7A0Q7DBFH3MJ2PGS3G1
language: en
source:
  end_turn: 8
  session_id: seed-528e89eeb284ceb5
  start_turn: 8
tags:
- nfr
- crash-rate
- sentry
- quality
title: 'Non-functional requirement: crash-free >98% is non-negotiable'
type: fact
---

Declared non-functional requirement: crash rate is the one metric that will not be compromised. Target: crash-free users > 98% for every release. Operational enforcement: integrate Sentry release health and block merges when crash-free metric in staging falls below 98%; require mandatory end-to-end smoke tests to run on the physical device lab before any release. Startup time and memory consumption are important but can be relaxed in short-term tradeoffs if necessary; crashes are a trust breaker for driver users and thus must be strictly monitored and prevented. This requirement will be enforced through CI gating and manual device-lab smoke testing prior to pushes to production.