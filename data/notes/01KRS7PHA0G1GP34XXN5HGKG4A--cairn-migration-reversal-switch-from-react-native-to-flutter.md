---
created_at: '2026-05-16T20:30:00Z'
entities:
- Cairn
- React Native
- Flutter
id: 01KRS7PHA0G1GP34XXN5HGKG4A
language: en
source:
  end_turn: 0
  session_id: seed-db906d2dad5e0dcc
  start_turn: 0
tags:
- migration
- react-native
- flutter
- cairn
- performance
title: 'Cairn migration reversal: switch from React Native to Flutter (session 2026-05-16)'
type: fact
---

Session log: On 2026-05-16 I reversed the earlier 2026-03-07 decision and decided to migrate the Cairn mobile app from React Native (RN) to Flutter due to persistent map rendering jank we cannot reliably fix inside RN. Concrete codebase facts: RN codebase ≈45k LOC JavaScript, ~120 modules, and 12 native modules (custom map overlays, an existing offline routing C++ library, BLE integration, background location handling). Product users: drivers and planners. Symptoms that triggered the reversal: map freezes of roughly 200–400 ms during panning/zooming; polyline updates dropping frames during 1s GPS bursts (visible stutter when GPS updates arrive in bursts); CPU spikes on mid-tier devices causing dropped frames and thermal/performance issues. The decision is based on reaching reliable performance targets that RN rendering layer and the existing RN map integrations cannot meet under these constraints.