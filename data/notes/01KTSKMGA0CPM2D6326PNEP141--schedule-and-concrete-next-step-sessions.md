---
created_at: '2026-06-10T20:30:00Z'
entities:
- tmuxrc
- zellij
- README
id: 01KTSKMGA0CPM2D6326PNEP141
language: en
source:
  end_turn: 8
  session_id: seed-40499f1c3ad894fb
  start_turn: 8
tags:
- schedule
- tasks
- implementation
title: Schedule and concrete next-step sessions
type: task
---

I scheduled two focused work blocks to implement the plan. First session: Wednesday 2026-06-16 at 14:00 CET — extract the minimal tmuxrc (~50 lines) and test it on two production-like servers. Testing checklist for that session: verify per-user sockets under ~/.tmux/sockets, confirm attach/reattach workflows for myself and a teammate (create one shared /tmp/tmux-shared-<project> socket and test attach), ensure default-terminal fallback works, and replace or temporarily disable tmux-resurrect to validate restore scripts. Second session: Saturday 2026-06-20 at 09:00 CET — create zellij YAML layouts and bootstrap scripts on my laptop. Zellij layouts to produce: an ML project preset including an ipython REPL pane, a logs tail pane, an editor pane (VS Code / nvim), and a git/console pane. Also write small restore/bootstrap scripts and a short README explaining how to use the minimal tmuxrc, how to create a shared socket, and the local zellij workflows. Total time budget allocated across the two sessions is ~7 hours.