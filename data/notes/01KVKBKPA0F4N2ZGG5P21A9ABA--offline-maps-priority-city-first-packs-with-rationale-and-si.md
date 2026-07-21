---
created_at: '2026-06-20T20:30:00Z'
entities:
- Cairn
- testers
id: 01KVKBKPA0F4N2ZGG5P21A9ABA
language: en
source:
  end_turn: 2
  session_id: seed-3de9806b270bb9df
  start_turn: 0
tags:
- offline-maps
- scope
- product-priority
title: 'Offline maps priority: city-first packs with rationale and size estimates'
type: decision
---

Decided to prioritize city-level offline packs as the launch scope for offline maps. Rationale: of 12 beta testers, 9 explicitly requested offline maps, but only 3 required full-country downloads — indicating most users want local city coverage. City-first minimizes per-user download size (~50 MB per city pack typical) and reduces initial hosting costs. Country or regional packs are larger (roughly 200–400 MB depending on resolution and data included) and better deferred to later phases. City-first enables faster delivery, smaller device storage impact, and simpler UX for discovering and purchasing packs. This scope provides a clearer path to conversion experiments (smaller friction points) and keeps the backend pipeline manageable for initial rollout.