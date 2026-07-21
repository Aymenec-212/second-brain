---
created_at: '2026-04-21T20:30:00Z'
entities:
- orders table
id: 01KPRVRJA040F390AW1FABMRAZ
language: en
source:
  end_turn: 4
  session_id: seed-b1386cf507fa6f14
  start_turn: 4
tags:
- queries
- filters
- multi-tenant
- joins
- workload
title: Query patterns, filtering needs, joins, and multi-tenant isolation
type: fact
---

Observed query distribution and functional requirements: about 60% of queries are customer-scoped (customer_id high-cardinality ≈ 200k) and often include a narrow date range (7–30 days). Around 30% are global searches filtered by status (only a few possible values). The remaining 10% are ad-hoc cross-customer analytics. Nearly all production flows require joining returned shipment vectors back to an orders table to fetch fields like price and region before final scoring. Multi-tenant isolation is mandatory: queries must never return or expose vectors from other customers. This can be enforced via per-query filtering (customer_id) or by physically separating tenants, but logical filters are a core requirement for the search stack.