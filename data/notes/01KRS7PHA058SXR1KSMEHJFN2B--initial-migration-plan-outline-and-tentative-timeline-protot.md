---
created_at: '2026-05-16T20:30:00Z'
entities:
- React Native
- Flutter
- FFI
id: 01KRS7PHA058SXR1KSMEHJFN2B
language: en
source:
  end_turn: 2
  session_id: seed-db906d2dad5e0dcc
  start_turn: 2
tags:
- timeline
- plan
- prototype
- milestones
title: Initial migration plan outline and tentative timeline (prototype → infra →
  parity → QA)
type: idea
---

High-level plan skeleton: prototype → core infra → feature parity → QA & staged rollout. Initial timeline proposed: prototype 2 weeks (2026-05-16 to 2026-05-30), core infrastructure 3 weeks (to 2026-06-20), feature parity 4 weeks (to 2026-07-18), QA & polish 1 week (to 2026-07-25). This initial schedule assumed reuse of the existing C++ routing library via FFI and straightforward map SDK integration for vector/offline tiles. These assumptions are explicit risks: if FFI integration or map SDK plugin work is more complex, timelines will shift. The user’s target deadline for finishing migration and staged rollout before the next Q3 milestone is 2026-08-01; the original timeline was optimistic and contingent on those reuse assumptions.