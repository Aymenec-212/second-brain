---
created_at: '2026-07-20T17:10:57.729300Z'
entities:
- spaced repetition
- reranker
id: 01KY084SY116Z2EHHJ92DB88DS
language: en
source:
  end_turn: 1
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 1
tags:
- model
- scoring
- context
- delivery
title: 'Interruption decision framework: benefit − cost scoring and delivery tiers'
type: idea
---

Design an interruption decision as an explicit score = Benefit − Cost, and use that score to choose a delivery channel. Benefit components: item importance (user-set priority or inferred from tags/frequency/deadline), decay risk (time since last review, spaced repetition urgency), and interest (past engagement with similar prompts or explicit preferences). Cost components: interruptibility (calendar Busy/DND, active full-screen app, media playing, driving state, battery level, location), and annoyance propensity (recent dismiss rate, time of day). Map score ranges to delivery tiers: passive (sidebar, daily digest) for low net value; gentle nudge (timed notification, glanceable widget, snooze option) for moderate value; immediate interrupt (push, sound, modal) only for very high net value. Add context sensing that is low-friction: read calendar/DND, detect full-screen/video/audio, check driving state if mobile. Personalization: let users set aggressiveness (gentle / balanced / pushy) and quiet hours, and run a short "teaching" period where we ask quick post-interruption feedback to tune thresholds. Start with conservative adaptation rules (suppress during Busy/DND, reduce frequency when dismissals spike) and measure engagement, dismiss, snooze, and retention improvement to iterate.