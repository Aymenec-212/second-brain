---
created_at: '2026-02-03T20:30:00Z'
entities:
- Dataview
- Templater
- Obsidian
id: 01KGJK57A00YQQDM09R4PB9YTR
language: en
source:
  end_turn: 9
  session_id: seed-ac94c5b2e089ecd5
  start_turn: 9
tags:
- metrics
- automation
- dataview
- templater
title: 'Open decision: manual entry vs automated collection of weekly metrics'
type: task
---

Pending decision to make before the first weekly review: should weekly metrics in the 'Weekly Review YYYY-WW' Templater note be entered manually or populated by an automated script that pulls created/modified dates and backlink counts? Options and trade-offs to consider: automated collection (Dataview/DataviewJS) reduces manual entry friction and improves accuracy for things like created dates and backlink counts, but it requires initial setup and occasional debugging; manual entry keeps the template simple and forces reflection but adds friction and may reduce compliance. Next step: decide which approach to take before 2026-02-10 (experiment start). If choosing automation, specify which fields will be auto-populated (suggestion: created/modified counts, Inbox count, backlinks created, and links created) and implement small Dataview queries or a DataviewJS snippet during the initial cleanup session on 2026-02-09.