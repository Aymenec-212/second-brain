---
created_at: '2026-06-10T20:30:00Z'
entities:
- tmux
- ~/.tmux/sockets
- /tmp/tmux-shared-<project>
id: 01KTSKMGA0Z1EPTKYKFAJB881M
language: en
source:
  end_turn: 6
  session_id: seed-40499f1c3ad894fb
  start_turn: 6
tags:
- tmux
- sockets
- configuration
- compatibility
title: Socket policy and terminal-capability fallback
type: decision
---

I will use per-user tmux sockets by default to avoid socket name collisions and unexpected shared state. Concretely: place per-user sockets under ~/.tmux/sockets and make the default startup create sockets there. For occasional pair sessions, provide an explicit environment variable or small CLI flag that creates a shared socket at /tmp/tmux-shared-<project> (naming convention documented in the README) so a coworker can attach without changing their tmuxrc. For terminal capability, set default-terminal to tmux-256color in the minimal tmuxrc but include a fallback to xterm if tmux-256color is unavailable on older servers. This balances safe single-user defaults with an explicit, discoverable path for ad-hoc sharing.