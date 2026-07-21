---
created_at: '2026-06-10T20:30:00Z'
entities:
- ~/.tmux/minimal.conf
- ~/.tmux/sockets
- zellij
- tmux-resurrect
id: 01KTSKMGA0CPM2D6326PNEP142
language: en
source:
  end_turn: 8
  session_id: seed-40499f1c3ad894fb
  start_turn: 4
tags:
- checklist
- automation
- documentation
title: Task checklist for minimal tmuxrc, zellij layouts, and team bootstrap
type: task
---

Concrete implementation checklist and acceptance criteria: 1) Create ~/.tmux/minimal.conf (~50 lines) that includes: per-user socket creation under ~/.tmux/sockets, essential keybindings (attach, detach, new window, switch pane), minimal statusline, default-terminal set to tmux-256color with xterm fallback, and no heavy plugin dependencies. Acceptance: minimal.conf loads on Debian/Ubuntu without additional packages and is under 60 lines. 2) Implement restore scripts to replace tmux-resurrect: provide small scripts that re-create named sockets and launch a saved layout or start default windows/panes. Acceptance: after server reboot or socket loss, running ./tmux-restore.sh <project> recreates the basic session layout and returns to work within <2 minutes manual steps). 3) Build initial zellij YAML layouts for local use: ML project layout must include panes for ipython, tail -f logs, editor, and a git/cli pane; store layouts in a git repo and add simple wrapper scripts to launch them. Acceptance: launching zellij layout reproduces the expected panes and starts the agreed commands within 3 seconds locally. 4) Write a README/quickstart for teammates: explain default per-user sockets, how to create and attach to /tmp/tmux-shared-<project>, how to use the minimal tmuxrc, and where to find zellij layouts (for my laptop only). Acceptance: a teammate can attach to a shared session with no more than three commands and basic instructions. 5) Test plan: run the minimal tmuxrc on two production servers during the Wednesday session, and iterate fixes; test shared socket attach with one coworker. Track time spent: aim for the 2h + 3h + 1h split previously estimated and record actual time for future refinements.