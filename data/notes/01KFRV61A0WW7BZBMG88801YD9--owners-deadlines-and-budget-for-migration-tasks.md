---
created_at: '2026-01-24T20:30:00Z'
entities:
- Sam
- Antoine
- Nico
- AWS RDS
id: 01KFRV61A0WW7BZBMG88801YD9
language: en
source:
  end_turn: 8
  session_id: seed-d2bad5a2a44349e1
  start_turn: 8
tags:
- owners
- deadlines
- budget
- migration
title: Owners, deadlines, and budget for migration tasks
type: task
---

Assign clear owners and deadlines for migration work. Sam (me) owns schema design and import scripts: schema draft due 2026-01-29; import scripts due 2026-02-05. Nico (infra) owns RDS provisioning, PgBouncer setup, backups, and initial monitoring: due 2026-02-03. Antoine owns validation tests and client-side changes to support dual-write: due 2026-02-12. Key milestone dates: dry-run on staging 2026-02-10, begin production dual-write 2026-02-15, cutover (final switch to Postgres reads) target 2026-03-01. Budget: initial RDS estimate ~€450/month; add ~€120/month if a read-replica is provisioned. The migration plan assumes team capacity matches these dates; if any owner is delayed, update the timeline and inform the others immediately. Require manual sign-off from Sam or Nico before progressing each stage that affects production reads/writes.