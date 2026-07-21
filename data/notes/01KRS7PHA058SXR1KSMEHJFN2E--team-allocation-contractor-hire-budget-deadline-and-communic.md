---
created_at: '2026-05-16T20:30:00Z'
entities:
- Jules
- Marion
- Léa
- Sam
- contractor
- Mapbox plugin
id: 01KRS7PHA058SXR1KSMEHJFN2E
language: en
source:
  end_turn: 8
  session_id: seed-db906d2dad5e0dcc
  start_turn: 8
tags:
- team
- hiring
- budget
- communications
- ci
title: Team allocation, contractor hire, budget deadline, and communications plan
type: task
---

Team composition and allocation: Jules (mobile lead) will be full-time on the migration. Marion (mobile) will start at roughly 60% RN maintenance / 40% migration and flip to 40% RN / 60% migration after the prototype phase. Léa (QA) will own perf automation and invest ~1.5 weeks building the perf harness. I (Sam) will handle backend/CI build changes for NDK/CMake and iOS static library targets, plus deployment pipelines. Hiring: budget exists to hire a contractor (2 weeks) to accelerate Mapbox plugin work and native bindings; contractor cost ~€8,000. Budget approval must be requested by 2026-05-22 to onboard the contractor in time for the plugin sprint. Communications: notify operations and the driver team on 2026-06-01 about the migration plans, expected impacts, and scheduled testing windows. Prepare and update runbooks for background-location behavior and battery impacts, and draft a rollback playbook listing steps to redeploy RN builds, how to flip feature flags, and who performs each action.