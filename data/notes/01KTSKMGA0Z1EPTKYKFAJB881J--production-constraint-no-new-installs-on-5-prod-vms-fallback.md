---
created_at: '2026-06-10T20:30:00Z'
entities:
- Debian
- Ubuntu
- tmux
- screen
- byobu
- ops
id: 01KTSKMGA0Z1EPTKYKFAJB881J
language: en
source:
  end_turn: 2
  session_id: seed-40499f1c3ad894fb
  start_turn: 2
tags:
- production
- ops
- constraints
- compatibility
title: 'Production constraint: no new installs on 5 prod VMs — fallback must be apt-available
  tmux/screen'
type: fact
---

Production constraint is strict: the five production VMs I need to be able to attach from cannot receive ad-hoc installs outside the operating-system package manager. I can request ops changes but they are slow and I don't want to depend on them for day-to-day workflows. Therefore any fallback or baseline solution must be available via apt-get (i.e., tmux or screen/byobu). This constraint drives the compatibility-first decision: keep a minimal, portable multiplexer configuration on production VMs that requires no custom binaries. Teammate workflow matters too: two coworkers occasionally need to attach to shared sessions, so the chosen server-side setup must be straightforward for them to use with minimal instruction.