---
created_at: '2026-01-07T20:30:00Z'
entities:
- 70B model
- 1B draft
id: 01KED2DTA04HQ062406FV4PCMD
language: en
source:
  end_turn: 0
  session_id: seed-080a3566d9e37509
  start_turn: 0
tags:
- speculative-decoding
- inference
- latency
- model-architecture
- 70b
title: 'Speculative decoding: mechanism and why it speeds inference for our 70B model'
type: fact
---

Speculative decoding workflow: run a small, cheap draft model to propose a contiguous block of the next k tokens, then run the large target model (the verifier) to check/accept that entire block instead of generating each token autoregressively. If the verifier accepts the block, the heavy model avoided k sequential autoregressive forwards. Why this can speed up wall-clock inference for our 70B production model: (1) it reduces the number of sequential expensive forward passes on the 70B model (amortizes verifier cost over k tokens); (2) it enables better GPU utilization and batching opportunities on the heavy model because the verifier runs less frequently and can verify blocks in fewer overall forwards; (3) it reduces repeated attention computation over long contexts on the big model since accepted draft tokens skip autoregressive passes on the 70B. In our concrete context the heavy model is 70B and the draft candidate is 1B (runs on same node). The draft is roughly ~5% of the compute of a 70B forward. If drafts are accepted a large fraction of the time, the paper and similar setups report 2–3× wall-clock speedups for comparable hardware and acceptance rates.