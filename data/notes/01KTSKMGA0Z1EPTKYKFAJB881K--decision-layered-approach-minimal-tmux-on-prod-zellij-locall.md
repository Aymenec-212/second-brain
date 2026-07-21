---
created_at: '2026-06-10T20:30:00Z'
entities:
- tmux
- zellij
- tmux-resurrect
id: 01KTSKMGA0Z1EPTKYKFAJB881K
language: en
source:
  end_turn: 4
  session_id: seed-40499f1c3ad894fb
  start_turn: 4
tags:
- decision
- architecture
- zellij
- tmux
title: 'Decision: layered approach — minimal tmux on prod, zellij locally; time estimate'
type: decision
---

Final decision is a layered approach: keep a minimal, portable tmux configuration on production servers and use a more modern local tool (zellij) on my laptop for better ergonomics and layouts-as-code. The minimal tmuxrc will be small (~50 lines) and focused on essentials, allowing teammates to attach without extra installs. Locally, zellij will provide YAML layouts, pane presets, and mouse support for development sessions. Pros: no ops changes required, teammates can still attach to server sessions, and local UX improves. Cons: I will need to learn zellij and write layout YAMLs, and install zellij on my laptop. I plan to drop heavy plugins like tmux-resurrect in favor of small, explicit restore scripts for tmux sockets to reduce fragility and cross-server plugin breakage. Rough time estimate (initial implementation): 6 hours total broken down as 2 hours for extracting and testing the minimal tmuxrc on two servers, 3 hours to create zellij layouts for an ML project (ipython, logs tail, editor, git), and 1 hour to write bootstrap scripts and a README for the team. Later I adjusted the overall estimate to ~7 hours total including testing and documentation refinement.