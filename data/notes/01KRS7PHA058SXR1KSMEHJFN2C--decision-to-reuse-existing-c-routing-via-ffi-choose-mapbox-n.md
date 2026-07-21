---
created_at: '2026-05-16T20:30:00Z'
entities:
- C++ offline routing
- FFI
- Android NDK
- CMake
- iOS static lib
- Mapbox
- mapbox_gl
- Dart
id: 01KRS7PHA058SXR1KSMEHJFN2C
language: en
source:
  end_turn: 4
  session_id: seed-db906d2dad5e0dcc
  start_turn: 4
tags:
- routing
- ffi
- mapbox
- map-plugin
- native-build
title: Decision to reuse existing C++ routing via FFI; choose Mapbox native SDKs and
  fork mapbox_gl
type: decision
---

Decision: reuse the existing C++ offline routing library via FFI rather than rewriting it in Dart. Implementation implications: keep a single native routing implementation and integrate it with Flutter through platform and FFI bindings. Build/CI changes required: modify Android NDK/CMake build in CI to produce and link .so artifacts for the Flutter Android target and add iOS static library targets (.a) for the Flutter iOS build (matching how the library is currently produced for RN native modules). For mapping, choose Mapbox native SDKs (iOS and Android) because they support vector tiles and offline usage. Flutter’s existing mapbox_gl plugin is incomplete; plan to fork mapbox_gl and patch where necessary. Schedule impact: allocate 1 week to fork the mapbox_gl repo and set up CI/branches, plus 2 weeks to implement robust Dart plugin wrappers for the patched Mapbox native SDKs. This plugin work pushes the feature-parity phase out by one week and moves the realistic finish date to 2026-08-01.