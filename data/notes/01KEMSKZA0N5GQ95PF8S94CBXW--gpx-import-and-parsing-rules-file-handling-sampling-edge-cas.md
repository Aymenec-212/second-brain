---
created_at: '2026-01-10T20:30:00Z'
entities:
- GPX
id: 01KEMSKZA0N5GQ95PF8S94CBXW
language: en
source:
  end_turn: 6
  session_id: seed-6a7500ae87535981
  start_turn: 0
tags:
- gpx
- import
- parsing
- file-handling
- sampling
title: GPX import and parsing rules (file handling, sampling, edge cases)
type: decision
---

Accepted upload formats: .gpx files and .zip archives containing .gpx. Maximum uploaded file size: 10 MB for alpha. The parser must accept GPX files missing timestamps or elevation tags — still accept and process. For sampling and resampling: primary resampling is spatial at 5 m intervals (resample polyline to ~5 m steps). If spatial resampling is not possible (e.g., no coordinates or degenerate segments), fallback to time-based resampling at 1 Hz. Elevation smoothing: apply an 11-point sliding median filter on elevation before computing gradients to remove GPS noise. Compute and store: total distance, total ascent, total descent, maximum gradient, gradient distribution (percent of route above thresholds 10% / 15% / 20%), max continuous climb segment (>200 m without descent), loop detection (start/end proximity), and estimated time (see Naismith-based estimate). Handling large/multi-day/ultra routes: GPX >100 km or multi-day routes will be rejected for precise scoring in alpha (label as “ultra” or multi-day) to avoid inaccurate scoring; accept but skip scoring. Missing elevation: perform DEM lookup (SRTM/AWS Terrain Tiles) when elevation tags are missing or when elevation jitter >20 m after smoothing.