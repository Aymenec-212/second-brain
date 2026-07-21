---
created_at: '2026-03-24T20:30:00Z'
entities:
- config/default.json
- ~/.config/cli-guilt/config.json
- sam/cli-guilt
- MIT
id: 01KMGRMEA032D2X28AWKCWXJJ3
language: en
source:
  end_turn: 6
  session_id: seed-3c2521cc75457297
  start_turn: 6
tags:
- defaults
- config
- readme
- ui
- repo
title: Default config behavior, README examples, UI color mapping, and repository
  metadata
type: decision
---

Default-install behavior: include a committed sample default config at config/default.json in the repository. On first run, the program should atomically copy config/default.json to ~/.config/cli-guilt/config.json if the config file is missing. README must show exact CLI examples and exact one-line outputs for common tasks, including: "guilt do read  # logs today and prints guilt message", "guilt status   # table: habit | streak | last | 30d%", "guilt history read --days 30  # CSV or pretty table", and "guilt set-tone stern". UI details: use ANSI colors — gentle mapped to dim green/yellow, stern to bright yellow, and shame to bold bright red. All single-line outputs must be <=120 characters. Example canonical output format for a successful do: a green checkmark prefix, habit name, a "— logged <date>." clause, then the guilt message in the tone color, then stats in dim gray parentheses. Repository metadata: publish on GitHub at sam/cli-guilt, license MIT, tag release v0.1.0 on 2026-04-07. The README should also document config keys: name (Sam), tone (gentle), timezone, and the locations of db.json and templates file.