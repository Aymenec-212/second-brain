---
created_at: '2026-03-07T20:30:00Z'
entities:
- Sam
- Cairn
- React Native
- Expo
- Flutter
id: 01KK4ZW7A0H4HEPCRSF82FM5MX
language: en
source:
  end_turn: 0
  session_id: seed-528e89eeb284ceb5
  start_turn: 0
tags:
- react-native
- decision
- mobile
- framework
- cairn
title: 'Decision: Choose React Native (bare) for Cairn mobile — chosen 2026-03-07'
type: decision
---

Decision recorded: use React Native (bare, not Expo) for the Cairn mobile app. Date of decision: 2026-03-07. Main reasons: the team already has an existing TypeScript web codebase and two frontend engineers comfortable with JS/TS, which enables faster reuse of validation and business logic and much faster iteration. Familiarity and ramp-time considerations outweigh Flutter's raw performance advantages for the MVP timeline. Target product milestone is an MVP delivery cycle ending 2026-09-30. Chosen approach: bare React Native so native modules for maps and barcode scanner can be implemented as needed. Action: log the decision string 'React Native — chosen 2026-03-07' in the product repository immediately so the choice is discoverable by engineering and product teams. This is a deliberate tradeoff: accept slightly less out-of-the-box performance than Flutter, but prioritize developer velocity, shared TypeScript logic, and lower short-term hiring cost and ramp time.