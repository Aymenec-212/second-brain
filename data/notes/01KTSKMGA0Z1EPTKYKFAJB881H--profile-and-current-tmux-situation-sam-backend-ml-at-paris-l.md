---
created_at: '2026-06-10T20:30:00Z'
entities:
- Sam
- tmux
- tpm
- tmux-resurrect
- tmux-continuum
id: 01KTSKMGA0Z1EPTKYKFAJB881H
language: en
source:
  end_turn: 0
  session_id: seed-40499f1c3ad894fb
  start_turn: 0
tags:
- personal
- tmux
- maintenance
- plugins
title: Profile and current tmux situation (Sam, backend/ML at Paris logistics startup)
type: fact
---

I am Sam, 31, a backend/ML engineer at a Paris logistics startup. I currently maintain a large personal tmux setup: the tmux config is about 1,200 lines and depends on tpm plus plugins including tmux-resurrect and tmux-continuum, with many ad-hoc bindings. Practical problems are high maintenance time (approximately 3 hours per week), slow iteration when tweaking bindings or behavior, a clunky startup feel, and occasional plugin breakage on older production servers. I want a workflow that preserves reliability on production servers while improving local ergonomics and scripting/layout capabilities. My explicit requirements in order of priority are: 1) attachability from minimal Debian/Ubuntu production servers without needing Rust/WASM or non-apt installs, 2) session persistence and easy restore, 3) templated project layouts (layouts-as-code), 4) programmatic control from Python/CLI, and 5) low config maintenance (<30 minutes/week ideally). Candidates I had on the radar included: continuing with tmux (slim/minimal), screen/byobu for compatibility, zellij (modern, YAML layouts, WASM plugins), wezterm mux (local), and moving some workflows into terminal-emulator tabs instead of a multiplexer.