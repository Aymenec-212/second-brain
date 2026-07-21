---
created_at: '2026-01-10T20:30:00Z'
entities:
- FastAPI
id: 01KEMSKZA0N5GQ95PF8S94CBY1
language: en
source:
  end_turn: 4
  session_id: seed-6a7500ae87535981
  start_turn: 2
tags:
- api
- endpoints
- backend
- design
title: Minimal alpha API endpoints and explainability payload
type: decision
---

Alpha API endpoints to implement (minimal): - POST /api/v1/import — multipart upload of .gpx or .zip (client-side validation for file type and <=10 MB). Returns a route ID and initial parse status. - GET /api/v1/route/{id} — returns JSON with route metadata, raw component metrics (distance km, ascent m, max gradient %, technical score, remoteness score, altitude), normalized 0–100 component values, weighted contributions, final numeric score 0–100 and difficulty bucket, estimated duration, flags (DEM used, GPS-derived technicality used, multi-day/ultra skip). - GET /api/v1/route/{id}.gpx — serves the original uploaded GPX file (encrypted at rest). - GET /api/v1/health — simple health check. Explainability requirement: the GET /route payload must include component breakdown suitable for UI bars and an exportable image (contractor will implement PNG export client-side). Keep API stateless and simple; no auth for alpha (account-less import flow) but log anonymized import IDs and enable deletion on request.