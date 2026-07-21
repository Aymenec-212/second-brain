---
created_at: '2026-03-07T20:30:00Z'
entities:
- Flipper
- Hermes
- webview
id: 01KK4ZW7A0Q7DBFH3MJ2PGS3FZ
language: en
source:
  end_turn: 4
  session_id: seed-528e89eeb284ceb5
  start_turn: 4
tags:
- risks
- android
- native-modules
- performance
title: Top technical risks and mitigation plan (low-end Android & native modules)
type: idea
---

Primary technical risks for the RN approach: 1) Performance on low-end Android devices (cold start, memory, runtime slowdowns); 2) Unpredictable native module bugs (maps, barcode scanner) that can block delivery. Mitigation plan: a) Integrate a strict performance budget and profiling from day one using Flipper and Hermes traces; measure startup time, frame drops, and memory on representative devices; b) Build and maintain a physical device lab of 15–20 devices that includes the cheapest Android phones expected in the user base so regressions are caught early; c) Isolate risky features as native modules with well-defined JS-native interfaces so the JS UI can ship while native implementations are being stabilized; d) Implement a webview fallback for non-critical flows so native blockers do not stop overall progress. These mitigations prioritize catch-and-fix early, and allow shipping incremental functionality while high-risk native pieces stabilize.