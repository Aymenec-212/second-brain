---
created_at: '2026-01-07T20:30:00Z'
entities:
- Oct–Dec 2025 customer logs
id: 01KED2DTA04HQ062406FV4PCME
language: en
source:
  end_turn: 2
  session_id: seed-080a3566d9e37509
  start_turn: 1
tags:
- acceptance-rate
- dataset
- oct-dec-2025
title: Current unknowns and a gut acceptance-rate guess for k=4 on Oct–Dec 2025 logs
type: fact
---

Acceptance rate on our domain (real customer logs from Oct–Dec 2025) is currently unknown — we haven't measured it end-to-end yet. A rough, informal estimate from quick label runs is a block-accept rate of about 0.6–0.8 for k=4 on in-domain prompts, but this is handwavy and must be validated. Dataset notes: the full dataset is about 1M tokens of real prompts/responses from Oct–Dec 2025. For experiments, plan to sample 100k tokens stratified by customer and prompt length to get a representative evaluation of acceptance behavior. Key unknowns to measure: per-k acceptance rate, distribution of where rejections occur within blocks, and how acceptance correlates with prompt length, customer, and rare tokens or adversarial patterns.