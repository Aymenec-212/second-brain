---
created_at: '2026-01-24T20:30:00Z'
entities:
- GiST
- SP-GiST
- BRIN
- btree
- geography
- PostGIS
- Cairn
id: 01KFRV61A0WW7BZBMG88801YDA
language: en
source:
  end_turn: 6
  session_id: seed-d2bad5a2a44349e1
  start_turn: 0
tags:
- indexing
- schema
- spatial
- scaling
title: Indexing and data model constraints for spatial + relational workloads
type: fact
---

Schema and indexing constraints for Cairn: normalize core entities (users, routes, events) and store event geometry as the PostGIS 'geography' type to ensure accurate distance calculations over the earth's surface. Index plan: create GiST (or SP-GiST where appropriate) spatial indexes on geography/geometry columns for nearest-neighbor and polygon queries; use BRIN indexes on large time-series event tables to support efficient time-range queries and to keep index size small for append-heavy workloads; add btree indexes on foreign-key columns (route_id, user_id) used in joins. Anticipated data growth: ~20M geolocated events in year one, with ~2x annual growth. Average monthly write rate ~1.6M events/month in year one; partitioning (monthly range partitions) will help maintenance and archival. Design schema to preserve Mongo IDs on import if feasible to simplify cross-checks and rollback. These index choices prioritize fast spatial queries and manageable maintenance costs as data grows.