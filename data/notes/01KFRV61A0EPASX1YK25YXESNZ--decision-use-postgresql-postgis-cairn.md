---
created_at: '2026-01-24T20:30:00Z'
entities:
- PostgreSQL
- PostGIS
- MongoDB
- Cairn
- Sam
- Antoine
- Nico
id: 01KFRV61A0EPASX1YK25YXESNZ
language: en
source:
  end_turn: 8
  session_id: seed-d2bad5a2a44349e1
  start_turn: 0
tags:
- database
- postgis
- decision
- cairn
- geo
title: 'Decision: Use PostgreSQL + PostGIS (Cairn)'
type: decision
---

I decided to standardize Cairn's primary datastore on PostgreSQL with the PostGIS extension rather than continuing on MongoDB. The core reasons are technical priorities: spatial queries (nearest-neighbor, within-polygon, accurate distance calculations) and relational joins between routes, users, and annotations are central to product functionality and require mature, native spatial functions (ST_Distance, ST_Within, etc.) and index support. ACID semantics matter for billing-like joins and reliable route annotation transactions; MongoDB's schema flexibility and sharding are attractive but secondary. MongoDB would force complex client-side joins or $lookup-heavy workflows and lacks the same proven spatial indexing and operators we need. Expected data volume (approx. 20M geolocated events in year one, doubling ~2x/year) and SLA requirements (typical nearest p95 <200ms) push toward a relational store with strong spatial indexing and query planning. Team constraints (two backend/ML engineers: Sam and Antoine; one infra engineer: Nico) and operational capacity also favor a proven, managed Postgres deployment to reduce operational burden. This decision is locked: proceed with Postgres+PostGIS for Cairn and move forward with a concrete migration and operational plan.