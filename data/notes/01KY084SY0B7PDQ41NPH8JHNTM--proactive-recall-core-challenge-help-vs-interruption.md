---
created_at: '2026-07-20T17:10:57.729073Z'
entities:
- Second Brain app
id: 01KY084SY0B7PDQ41NPH8JHNTM
language: en
source:
  end_turn: 0
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 0
tags:
- proactive-recall
- ux
- attention
- second-brain
title: 'Proactive recall: core challenge — help vs. interruption'
type: fact
---

I want to add proactive recall to the Second Brain app. The central trade-off is helpfulness (memory retention, habit formation, reduced future search time) versus interruption cost (breaking focus, annoyance). I need an interrupt model that surfaces useful recall prompts without degrading the user experience. Important failure modes to avoid: interrupting during deep work, meetings, driving, or media consumption; over-notifying and increasing dismiss rates; repeating the same topic too often. This will require (a) defining what 'useful' means for each item, (b) measuring current interruptibility signals the app can access, and (c) designing delivery tiers (passive → nudge → interrupt) that map to the computed value. Open questions I need to resolve soon: which platform signals can the app reliably read (calendar busy/free, OS Do Not Disturb, active window/full-screen app, media playback, device location/ driving state), and what initial frequency feels acceptable (per-minute and per-day caps). The goal is to create a conservative default that can be personalized and adapted over time from user feedback and engagement metrics.