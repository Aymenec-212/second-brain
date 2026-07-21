---
created_at: '2026-01-10T20:30:00Z'
entities:
- Python
- FastAPI
- PostgreSQL
- PostGIS
- S3
- Docker
- Scaleway
- AWS
- k8s
- gpxpy
id: 01KEMSKZA0N5GQ95PF8S94CBXV
language: en
source:
  end_turn: 0
  session_id: seed-6a7500ae87535981
  start_turn: 0
tags:
- tech-stack
- infrastructure
- deployment
- tools
title: Tech stack and infrastructure choices for MVP
type: decision
---

Locked technology choices for the MVP: backend in Python, FastAPI for the API, PostgreSQL with PostGIS for spatial storage, and S3-compatible storage for GPX files. Local development uses Docker. Deployment options for alpha are either a small managed Kubernetes cluster or a single managed VM (Scaleway or AWS) depending on ops complexity; start with the simplest managed VM if it keeps costs and maintenance lower. Elevation data sources: SRTM (~30 m resolution) or AWS Terrain Tiles as needed. OpenStreetMap (OSM) is the source for roads/highway and surface tags for technicality inference. GPX parsing can use gpxpy or a custom parser; parser must support tracks, waypoints, multiple segments, timestamps, and elevation tags. Instrumentation: Sentry for exceptions and logging (import success/failure, parse errors, feature computation times). Anonymized IDs for alpha, TTL 90 days by default; allow deletion on request.