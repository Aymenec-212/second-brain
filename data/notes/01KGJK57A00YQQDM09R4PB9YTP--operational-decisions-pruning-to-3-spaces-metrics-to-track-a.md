---
created_at: '2026-02-03T20:30:00Z'
entities:
- Google Calendar
- Obsidian
- Obsidian Sync
- Dataview
- Templater
- Projects.md
id: 01KGJK57A00YQQDM09R4PB9YTP
language: en
source:
  end_turn: 6
  session_id: seed-ac94c5b2e089ecd5
  start_turn: 6
tags:
- operations
- metrics
- pruning
- post-mortem
title: Operational decisions, pruning to 3 spaces, metrics to track, and post-mortem
  schedule
type: decision
---

Operational decisions for the experiment: 1) Calendar reminder: create a recurring Google Calendar event on Mondays at 09:00 named 'Notes Review' for 30 minutes as a hard reminder. 2) Obsidian quick-capture shortcut on the phone home screen for instant capture. 3) Prune the vault to three explicit spaces only: Inbox, Projects (Projects.md plus per-project notes), and Reference/Evergreen. 4) Decision rules recap: do-it-now if task <2 minutes; delete if clearly irrelevant; promote to project and record a single next action if further work is needed; make an evergreen note only if it can be linked to an existing note or future project. Weekly metrics to track (concrete logging fields): captured (n), processed (n), average time per note (minutes), Inbox count (n), links created (n), weekly-review done (Y/N), projects with next-actions (n), time spent (minutes). Targets: processed >= captured; processed <= 20/week; Inbox <= 5 by week 3; links >= 5/week; weekly reviews completed 4/4 over the 30 days. Post-mortem scheduled for 2026-03-12 to decide whether to continue, simplify, or revert. I will run a 90-minute initial cleanup on 2026-02-09 to reduce the backlog to <200 notes before starting the 30-day trial.