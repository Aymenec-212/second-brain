---
created_at: '2026-03-05T20:30:00Z'
entities:
- Rust
- Python
- Numba
- Cython
id: 01KJZV2SA0W4R3VWTAC7ADVP7M
language: en
source:
  end_turn: 2
  session_id: seed-7d14ab2961793f51
  start_turn: 2
tags:
- experiment
- rust
- timeline
- prototype
- benchmark
title: 'Decision: run a 3-month Rust experiment as the primary test this spring'
type: decision
---

I committed to a practical, time-boxed experiment: run a 3-month Rust experiment starting mid-March and ending mid-June, with the explicit objective of producing a prototype of the route simulator core in Rust, benchmarking it against the current Python implementation and an optimized Python variant (Numba/Cython), and making a go/no-go integration decision. Time allocation is 8 hours/week for 12 weeks (~96 hours). The criterion for continuing to production is measurable win within this year; if the Rust prototype demonstrates the targeted runtime improvements and reasonable dev/maintenance cost, plan to integrate to production by 2026-09-30. If the prototype fails to show sufficient improvement, fallback is to invest remaining effort into Python performance work. The experiment is framed to protect short-term product impact while giving deliberate time to explore a systems path that could pay off for Staff-level skills.