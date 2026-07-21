---
created_at: '2026-03-07T20:30:00Z'
entities:
- Hermes
- Fastlane
- Sentry
- Flipper
- pnpm
id: 01KK4ZW7A0Q7DBFH3MJ2PGS3FX
language: en
source:
  end_turn: 0
  session_id: seed-528e89eeb284ceb5
  start_turn: 0
tags:
- tooling
- ci
- crash-monitoring
- performance
title: Chosen toolchain and platform choices for RN implementation
type: idea
---

Concrete platform and tooling choices to support the React Native implementation: 1) Use Hermes as the JS engine to improve Android startup and runtime performance; 2) Use Fastlane for CI/CD workflows and release automation; 3) Use Sentry for crash monitoring and release health metrics; 4) Integrate profiling and debugging from day one via Flipper and Hermes traces; 5) Use a pnpm monorepo workspace structure so shared TypeScript libraries (validation, business logic, data models) can be reused between web and mobile. The app will be built as a bare RN project (no Expo) to allow custom native modules for maps and the barcode scanner. These choices balance short-term developer velocity (shared TS libs, familiar JS toolchain) and operational needs (native modules, release automation, crash observability).