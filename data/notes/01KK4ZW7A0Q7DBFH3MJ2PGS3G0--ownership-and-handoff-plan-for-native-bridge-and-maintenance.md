---
created_at: '2026-03-07T20:30:00Z'
entities:
- Sam
- contractor
- full-time mobile hire
- native-bridge
id: 01KK4ZW7A0Q7DBFH3MJ2PGS3G0
language: en
source:
  end_turn: 6
  session_id: seed-528e89eeb284ceb5
  start_turn: 6
tags:
- ownership
- handoff
- native-bridge
- hiring
title: Ownership and handoff plan for native bridge and maintenance
type: decision
---

Ownership and long-term maintenance plan for native bridge code: initial ownership will be split between Sam and the contracted engineer during the build phase. Sam will author a native-bridge contract document by 2026-03-10 that specifies the API surface, performance SLAs, and required tests; the contractor will implement the interfaces. All native and JS bridge code, native test suites, and a concise onboarding document will live in the monorepo to make future handoffs easier. Planned handoff: hire a full-time mobile engineer in Q1 2027 who will take over maintenance and ongoing native work. Contingency: if necessary, scope a small retainer with the contractor (suggested €2k/month) for up to six months post-launch to provide continuity until the FTE is onboarded. Also allow webview fallbacks for non-critical flows if a native blocker emerges before the handoff.