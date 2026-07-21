---
created_at: '2026-07-20T17:10:57.729444Z'
entities:
- calendar
- do not disturb
- active window
- location
- driving
id: 01KY084SY116Z2EHHJ92DB88DX
language: en
source:
  end_turn: 3
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 1
tags:
- task
- integration
- context
title: 'Task: inventory available interruptibility signals the app can read'
type: task
---

I need to inventory which interruptibility signals the Second Brain app can already access because that determines how sophisticated the interruption model can be quickly. Target signals to check for each platform (mobile and desktop): calendar busy/free and event metadata (title, attendees); OS-level Do Not Disturb status; active window / full-screen detection and a list of active foreground apps; system media playback state (audio/video playing); location and driving detection (e.g., CarPlay / Android Auto or OS driving mode); battery level and low-power mode; and whether a meeting is in progress (from calendar). Action items: (1) for iOS/Android, document which of these are available via current permissions/APIs; (2) for macOS/Windows, check whether the app can detect full-screen apps and Do Not Disturb; (3) list any permission prompts that will be necessary (calendar access, location, media state) and draft in-product permission rationale. This inventory is required before implementing context suppression and for selecting the initial cost model (binary Busy/DND vs. graded interruptibility).