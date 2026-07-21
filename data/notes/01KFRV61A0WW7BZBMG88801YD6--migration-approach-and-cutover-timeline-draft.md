---
created_at: '2026-01-24T20:30:00Z'
entities:
- MongoDB
- CSV
- NDJSON
- Sam
- Antoine
- Nico
id: 01KFRV61A0WW7BZBMG88801YD6
language: en
source:
  end_turn: 8
  session_id: seed-d2bad5a2a44349e1
  start_turn: 2
tags:
- migration
- timeline
- staging
- data-migration
title: Migration approach and cutover timeline (draft)
type: task
---

Migration approach: export current MongoDB collections to CSV or NDJSON and write id-preserving import scripts that populate normalized Postgres schemas. Include automated integrity checks (row counts, sampling of joined records, checksums) after import. Use a staging cluster for dry-runs and validation before touching production data. Timeline (locked by owners): schema draft by 2026-01-29 (owner: Sam), import scripts ready by 2026-02-05 (owner: Sam), dry-run on staging on 2026-02-10, client changes and dual-write implementation complete by 2026-02-12 (owner: Antoine), start production dual-write on 2026-02-15, and target cutover (stop Mongo reads, serve from Postgres) on 2026-03-01. During the dual-write window, keep Mongo running as a read fallback and run continuous data parity checks. The import scripts must preserve original IDs to simplify switching and rollback. The plan assumes two weeks of dual-write testing and at least one successful dry-run on staging before production dual-write.