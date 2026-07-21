---
created_at: '2026-07-20T17:10:57.729357Z'
entities:
- Second Brain app
id: 01KY084SY116Z2EHHJ92DB88DT
language: en
source:
  end_turn: 1
  session_id: 01KY07ZPEKHJBBBVY4VA7DHT7K
  start_turn: 1
tags:
- experiment
- metrics
- a-b-test
title: 'Experiment plan: two-channel flow (daily passive digest + up to 2 push nudges)'
type: task
---

Concrete experiment to validate the model: implement a two-channel flow for a pilot cohort. Channel A — passive daily digest: collect lower-scoring items and show them in a sidebar/digest once per day. Channel B — up to two push nudges per user per day for higher-value items. Scoring for the pilot should be a simple benefit−cost: benefit = spaced-repetition urgency * user-set priority; cost = calendar Busy OR Do Not Disturb (binary for initial run). Delivery rule: if net score exceeds the push threshold and user is not Busy/DND, send up to 2 nudges spaced out through the day; otherwise add to the digest. Run for 2 weeks, then measure: engagement rate (opened / notified), dismiss rate, snooze rate, items reviewed per user, and short-term retention for reviewed items. Also present one in-app question after the pilot: "Was this interruption helpful?" Use responses and behavioral metrics to refine thresholds, throttle rules, and whether to expand channels. This experiment will provide the initial data to calibrate score percentiles and daily/ per-minute caps.