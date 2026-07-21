---
created_at: '2026-01-10T20:30:00Z'
entities:
- OpenStreetMap
id: 01KEMSKZA0N5GQ95PF8S94CBXZ
language: en
source:
  end_turn: 4
  session_id: seed-6a7500ae87535981
  start_turn: 2
tags:
- normalization
- thresholds
- metrics
- scaling
title: Normalization functions and numeric thresholds (distance, ascent, gradient,
  remoteness, surface)
type: decision
---

Normalization choices locked for alpha: - Distance: linear mapping from 0–50 km → 0–100, clamp at 50 km. - Ascent: log-scale mapping to compress extremes: ascent_norm = 100 * log1p(ascent_m) / log1p(3000). This makes 3,000 m of ascent map to ~100. - Max gradient: linear mapping 0–60% → 0–100, clamp at 60%. - Technicality (surface): map internal surface score in range 0–50 to [0–100] linearly (so surface 50 → 100). The surface score mapping is an internal 0–50 scale (examples: asphalt=0, compacted small value, dirt higher, rocky/boulder toward 30–50). - Remoteness: compute median distance (meters) from route points to nearest OSM highway of types primary/secondary/tertiary/unclassified/residential; rem_norm = clamp(100 * log1p(median_dist) / log1p(5000), 0, 100) so ~5 km → ~100. - Altitude: simple binary-ish contribution: altitude_score adds for high altitude (above 1,500 m increases difficulty); encode as altitude_norm in 0–100 with a small weight (w6=0.05). Buckets remain 0–25/26–50/51–75/76–100. These normalization rules are the authoritative transforms for alpha; record them for reproducibility and explainability.