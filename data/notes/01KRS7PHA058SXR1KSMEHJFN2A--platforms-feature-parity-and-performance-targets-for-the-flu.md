---
created_at: '2026-05-16T20:30:00Z'
entities:
- Mapbox
- offline vector tiles
- C++ offline routing
- BLE
- background location
id: 01KRS7PHA058SXR1KSMEHJFN2A
language: en
source:
  end_turn: 2
  session_id: seed-db906d2dad5e0dcc
  start_turn: 1
tags:
- requirements
- performance
- platforms
- feature-parity
title: Platforms, feature parity and performance targets for the Flutter migration
type: fact
---

Platform scope: support iOS and Android first; web/desktop deferred to a later phase. Feature parity requirements to preserve at cutover: offline vector tiles, the existing C++ offline routing library, background location monitoring (including background GPS at 1s update cadence), BLE integration, push notifications, and custom vehicle markers/overlays used by drivers. Performance targets defined for the migration: map re-render latency on route changes <100 ms, stable 45+ FPS on mid devices, memory footprint <150 MB, CPU utilization <15% on mid-class devices (examples given as Pixel- or iPhone-mid class). These targets are the quantitative acceptance criteria for the migration and will be used in automated benchmarks and device testing.