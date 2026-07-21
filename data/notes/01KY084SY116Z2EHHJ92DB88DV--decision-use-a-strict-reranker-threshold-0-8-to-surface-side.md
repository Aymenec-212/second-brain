---
created_at: '2026-07-20T17:10:57.729390Z'
entities:
- reranker
- side-note
id: 01KY084SY116Z2EHHJ92DB88DV
language: en
source:
  end_turn: 2
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 2
tags:
- decision
- reranker
- threshold
title: 'Decision: use a strict reranker threshold (0.8) to surface side-notes'
type: decision
---

I decided to gate proactive recall with a strict reranker threshold: surface items as 'side-notes' only if the reranker score is ≥ 0.8. This is intended as a simple, explainable rule to limit volume and keep interruptions high-value. I treat the 0.8 threshold as a starting point, not final: it must be calibrated against historical score distributions to ensure it corresponds to the intended frequency (e.g., top 5% of items). I will also combine this decision with contextual suppression and throttling so that a 0.8 item won't necessarily interrupt in Busy/DND/full-screen or driving. Immediate next steps: run a batch job on past reranker outputs to compute percentiles for raw scores, estimate how many 0.8+ events per user per week would occur, and choose throttle windows (per-minute and per-day) before enabling live side-notes.