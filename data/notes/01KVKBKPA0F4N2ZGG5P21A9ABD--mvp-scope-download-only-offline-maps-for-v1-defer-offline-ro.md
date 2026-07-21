---
created_at: '2026-06-20T20:30:00Z'
entities:
- Cairn
id: 01KVKBKPA0F4N2ZGG5P21A9ABD
language: en
source:
  end_turn: 8
  session_id: seed-3de9806b270bb9df
  start_turn: 5
tags:
- mvp
- offline-maps
- routing
- search
title: 'MVP scope: download-only offline maps for v1; defer offline routing/search'
type: decision
---

MVP definition for offline maps (v1): implement download-only offline maps (tiles + cache + local rendering) — no offline routing or local search/indexing in v1. Rationale: delivering tiles and offline visualization is far faster to implement; offline routing/search requires heavy algorithm work, large index files, and integration complexity that would delay launch. Plan to deliver offline routing and search as part of v2 after validating demand and conversion from v1. For v1, include mechanisms to detect offline and fall back to online services when available, but ensure both stability and privacy constraints. This scope is intended to hit the alpha/beta/public timeline while minimizing engineering risk.