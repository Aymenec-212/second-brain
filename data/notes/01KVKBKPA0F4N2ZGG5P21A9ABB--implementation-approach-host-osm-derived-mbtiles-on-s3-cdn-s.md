---
created_at: '2026-06-20T20:30:00Z'
entities:
- OSM
- MBTiles
- S3
- CDN
- Mapbox
- Sam
id: 01KVKBKPA0F4N2ZGG5P21A9ABB
language: en
source:
  end_turn: 6
  session_id: seed-3de9806b270bb9df
  start_turn: 2
tags:
- implementation
- tiles
- mbtiles
- s3
- cdn
- osmtile
title: 'Implementation approach: host OSM-derived MBTiles on S3 + CDN (Sam builds
  pipeline)'
type: task
---

Implementation decision and assigned responsibilities: use OpenStreetMap (OSM) data to avoid recurring per-tile costs from Mapbox or other paid tile providers. Generate MBTiles bundles per city on the backend pipeline that I (Sam) will build. Store MBTiles files on AWS S3 and put them behind a CDN (CloudFront or equivalent) to serve downloads efficiently; use signed URLs for per-account access control. Mobile apps will download MBTiles and use local MBTile access libraries to render tiles. Avoid third-party SDKs that bill per-download. Technical considerations: determine tile zoom levels to balance visual fidelity vs file size for ~50 MB target city packs; implement a pipeline to produce vector (preferred) or raster MBTiles depending on mobile rendering complexity and size. Plan to document processing steps, reproducible builds, and S3 object lifecycle/ cache-control policies. Deliverables: working MBTiles generation pipeline, S3 bucket + CDN config, and signed-url access flow by alpha milestone.