---
created_at: '2026-03-24T20:30:00Z'
entities:
- config/templates.json
- ✓
- ✗
id: 01KMGRMEA032D2X28AWKCWXJJ4
language: en
source:
  end_turn: 8
  session_id: seed-3c2521cc75457297
  start_turn: 8
tags:
- templates
- messages
- ansi
- testing
title: Exact message templates and color/character choices for gentle/stern/shame
type: decision
---

Exact templates and color/character rules to commit to config/templates.json so they are editable later. Gentle (missed=1): prefix is green checkmark U+2713, message text color: dim yellow, stats color: dim gray. Exact wording: "✓ Read — logged 2026-03-24. Sam — missed yesterday. One small step now? (streak 6, 30d: 83%)". Stern (missed=2): prefix is yellow exclamation mark "!" (colored bright yellow), message wording: "! Read — two days off. Start now or it becomes three. (streak 4, 30d: 67%)". Shame (missed>=4): prefix is red X U+2717, message wording: "✗ Read — 4 days off. You know better. Pick one minute and begin. (30d: 40%)". All three must be constrained to a single line and <=120 characters. Store these exact strings (with placeholders for habit/date/stats) in config/templates.json. Tests should assert the rendered strings match these exact templates when populated with deterministic sample data and that the correct ANSI escape codes surround the intended parts (prefix symbol color, message color, and dim-gray stats). This note is the authoritative source for the initial templates and color/character assignments.