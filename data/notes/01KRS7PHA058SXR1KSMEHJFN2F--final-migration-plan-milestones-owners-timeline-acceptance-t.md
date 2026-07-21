---
created_at: '2026-05-16T20:30:00Z'
entities:
- prototype
- core infra
- plugin
- feature parity
- QA
- staged rollout
- decision point
id: 01KRS7PHA058SXR1KSMEHJFN2F
language: en
source:
  end_turn: 9
  session_id: seed-db906d2dad5e0dcc
  start_turn: 0
tags:
- migration-plan
- milestones
- owners
- acceptance
- rollout
title: 'Final migration plan: milestones, owners, timeline, acceptance tests, and
  rollout plan'
type: decision
---

Consolidated migration plan with owners, timeline, acceptance criteria and rollback triggers (target finish before Q3 milestone): Milestone 1 — Prototype (2026-05-16 to 2026-05-30): goals: basic Flutter app shell, Mapbox native SDK proof-of-concept on Android/iOS, simple FFI hook to C++ routing returning routes to Dart. Owners: Jules (lead), Marion (40% on migration), Sam (CI guidance), contractor optional. Deliverables: POC builds on one Android and one iOS device, smoke perf measurements. Milestone 2 — Core infra (2026-05-31 to 2026-06-20): integrate C++ routing via FFI, update Android NDK/CMake and iOS static lib targets in CI, basic offline vector tiles setup. Owners: Sam (CI/build), Jules. Deliverables: CI artifacts (.so/.a), docs for native build. Milestone 3 — Mapbox plugin + feature parity (2026-06-21 to 2026-07-25): fork and patch mapbox_gl (1 week), implement Dart plugin wrappers and native bindings (2 weeks), re-implement BLE, background location, push notifications, vehicle markers, and offline routing integration. Owners: contractor + Jules + Marion; Léa begins perf harness. Deliverables: feature-parity beta app that mirrors RN behavior. Milestone 4 — QA, perf automation, and polish (2026-07-26 to 2026-07-31): Léa leads automated perf runs across device tiers, collect p50/p90/p99 metrics, memory/CPU. Acceptance criteria: map re-render <100 ms, stable 45+ FPS on mid devices, memory <150 MB, CPU <15% on mid devices during benchmark scenarios (10k route updates, 1s GPS bursts, panning/zooming). Decision point: 2026-07-20 hard stop to evaluate whether to continue cutover or pause. If pass, schedule staged rollout starting 2026-08-02: 10% → 50% → 100% over ~2–3 weeks with production metric monitoring. If fail, pause cutover, freeze new features for 4 weeks, maintain RN hotfixes (Marion ~40%), and triage fixes. Budget: request contractor approval (€8,000) by 2026-05-22. Communications: ops + driver team notified 2026-06-01; update runbooks and prepare rollback playbook before decision point.