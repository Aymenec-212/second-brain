---
created_at: '2026-02-27T20:30:00Z'
entities:
- routing prefs
- annotators
- senior PMs
id: 01KJGCPFA02E39F0EJVAVYJDVV
language: en
source:
  end_turn: 6
  session_id: seed-eee7661285d2f721
  start_turn: 6
tags:
- labeling
- routing
- augmentation
- quality
title: Routing preference augmentation sprint plan and quality gates
type: task
---

If DPO fails on routing, execute a targeted labeling sprint to collect +1,000 routing-focused preference pairs. Plan two 3-day sprints staffed by 6 annotators (per sprint) with a throughput target of ~83 preference pairs per annotator per day to reach the target within schedule. Budget allocated for this augmentation is €3,000. Quality gates: create a gold-set of 200 routing-focused pairs; each annotator must exceed 85% agreement on this gold-set to pass. If any annotator fails the agreement gate, their labels are rejected and a fallback expert review is triggered: two senior product managers will review and adjudicate low-quality labels. The augmented +1,000 routing-focused prefs will be used to retrain or fine-tune either the DPO or RM/PPO pipeline depending on which path is chosen; target to complete augmentation and the targeted RLHF run by 2026-03-26. Track annotator performance, sprint pacing, and cost burn daily during the sprints.