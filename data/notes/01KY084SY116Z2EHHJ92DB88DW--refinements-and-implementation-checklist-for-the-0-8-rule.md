---
created_at: '2026-07-20T17:10:57.729414Z'
entities:
- reranker
id: 01KY084SY116Z2EHHJ92DB88DW
language: en
source:
  end_turn: 3
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 3
tags:
- implementation
- calibration
- ux
- personalization
title: Refinements and implementation checklist for the 0.8 rule
type: task
---

I will tighten the 0.8-side-note rule with a set of refinements and concrete defaults to behave well in the wild. Calibration: run a script to compute the reranker score distribution and percentiles from historical data so 0.8 maps to the intended top-X% of items; adjust threshold if necessary. Context suppression: even for ≥0.8, suppress delivery during calendar Busy, Do Not Disturb, full-screen video/audio, or driving. Temporal throttles (defaults to start with): max 1 side-note per 30–60 minutes and max 2–4 side-notes per day; avoid surfacing two consecutive items from the same tag to reduce repetition. Short-term feedback adaptation: track immediate dismisses; if a user dismisses side-notes faster than T seconds or dismisses >3 prompts in 24 hours, increase their personal threshold by +0.05 or lengthen the throttle window for 48 hours (reduce frequency by 50%). Graded urgency: reserve a higher tier (e.g., score > 0.95) for more interruptive presentation (push with sound) and use 0.8–0.95 for subtle side-notes. Transparency and controls: show why an item was surfaced ("Last reviewed 21 days ago" or "High priority: Project X") and provide controls: snooze for X hours, "don’t remind about this topic", "show less like this", and a global aggressiveness slider (gentle / balanced / pushy) plus quiet hours. Next implementation steps: (1) write the calibration script and compute percentiles, (2) implement context checks and throttle logic, (3) add per-user short-term feedback counters, and (4) draft UI copy for the side-note explanation and controls (or ask for a copy to be drafted). Open question: do I want the system to automatically nudge threshold after N dismissals, or only after explicit negative feedback? I'll decide after seeing pilot metrics.