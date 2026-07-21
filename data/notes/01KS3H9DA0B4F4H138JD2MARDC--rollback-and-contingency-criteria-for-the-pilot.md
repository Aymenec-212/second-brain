---
created_at: '2026-05-20T20:30:00Z'
entities:
- Sam
- Marion
id: 01KS3H9DA0B4F4H138JD2MARDC
language: en
source:
  end_turn: 10
  session_id: seed-6af5ee8a4e680b90
  start_turn: 2
tags:
- contingency
- rollback
- pilot
- safety
title: Rollback and contingency criteria for the pilot
type: decision
---

Rollback criteria: explicitly codified thresholds to stop or revert the pilot to the previous rotation to protect reliability and personal well-being. Abort and revert immediately if any of the following occur during the pilot: (A) Any key metric (pages, MTA, MTTR, Sev1 count) worsens by more than 20% relative to the baseline for the team across the same week; (B) Average sleep rating reported by the on-call cohort falls below 3 (on 1–5 scale) or is <3 for two consecutive weeks; (C) Pages per night exceed 2 for more than two consecutive weeks; or (D) Weekend pages exceed 4 total in a weekend. Operational contingency: if a critical skill gap arises for database incidents or other domain beyond team capacity, activate external DB incident provider as a stopgap (budgeted option) while hiring proceeds. Decision cadence: pilot review on 2026-07-01 to determine next steps; hire decision targeted by 2026-07-15. The rollback rules are designed to be simple, measurable, and enforceable so the team can stop the experiment quickly if it harms reliability or people.