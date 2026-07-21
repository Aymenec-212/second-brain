---
created_at: '2026-03-05T20:30:00Z'
entities:
- Rust
- The Rust Book
- rustlings
- Udemy
id: 01KJZV2SA0W4R3VWTAC7ADVP7N
language: en
source:
  end_turn: 4
  session_id: seed-7d14ab2961793f51
  start_turn: 4
tags:
- metrics
- thresholds
- timeline
- resources
- roi
title: Success metrics, decision thresholds, timeline, and study resources for the
  Rust experiment
type: decision
---

Primary success metric: reduce end-to-end nightly simulation runtime from ~5.0 hours to ≤1.5 hours (≥70% reduction) when swapping in the Rust component, measured on the staging cluster under representative load. Secondary metric: developer/maintenance overhead — if onboarding and future changes increase dev time by more than 50% versus current Python baseline, treat that as a negative strike against adoption. Decision rule: if by the 12-week prototype milestone I cannot achieve a reproducible ≥30% improvement in runtime, stop the Rust path and redirect effort to Python optimizations. Formal timeline: start 2026-03-15, prototype complete 2026-06-15, production integration target 2026-09-30 if criteria are met. Planned study resources: The Rust Book, rustlings exercises, and one paid Udemy course. Planned learning budget: ~96 focused hours (8 hrs/week × 12 weeks). I consider this tight but actionable.