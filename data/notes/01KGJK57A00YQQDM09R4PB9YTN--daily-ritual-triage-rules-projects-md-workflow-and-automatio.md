---
created_at: '2026-02-03T20:30:00Z'
entities:
- Projects.md
- Obsidian
- Dataview
id: 01KGJK57A00YQQDM09R4PB9YTN
language: en
source:
  end_turn: 4
  session_id: seed-ac94c5b2e089ecd5
  start_turn: 4
tags:
- daily-ritual
- triage
- projects
- automation
title: Daily ritual, triage rules, Projects.md workflow, and automation need
type: decision
---

Minimal daily ritual I will commit to: 1) On the phone, quick-capture any idea into the Obsidian Inbox using a home-screen shortcut — max 90 seconds per capture. 2) At night, do a 1-minute triage pass over new Inbox notes. Triage rules: mark a note as #reference if it is passive reference material; convert to a project stub if it contains a next-action; delete immediately if clearly garbage. Execution rule for next-actions: if the next action takes <2 minutes, do it immediately (do-it-now). If the next action takes >2 minutes, add the item to Projects.md with a single explicit next action and a deadline. Projects.md lives at the vault root and is the single source of truth for active work. Weekly review (Sunday, 30 minutes): process the Inbox to zero; move items into Projects.md or the Reference/Evergreen folder; convert worthwhile items into evergreen notes and link them to relevant existing notes/projects. Automation request: surface unlinked evergreen/reference notes older than 14 days so I can link or fold them. Plan to implement this with Dataview queries (community plugins enabled).