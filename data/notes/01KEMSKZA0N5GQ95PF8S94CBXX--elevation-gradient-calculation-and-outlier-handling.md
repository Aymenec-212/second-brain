---
created_at: '2026-01-10T20:30:00Z'
entities:
- SRTM
- AWS Terrain Tiles
- DEM
id: 01KEMSKZA0N5GQ95PF8S94CBXX
language: en
source:
  end_turn: 4
  session_id: seed-6a7500ae87535981
  start_turn: 2
tags:
- elevation
- dem
- gradient
- smoothing
- srtm
title: Elevation, gradient calculation, and outlier handling
type: decision
---

Elevation strategy: prefer DEM lookup (SRTM at ~30 m resolution or AWS Terrain Tiles) when GPX elevation tags are missing or when elevation jitter after initial smoothing exceeds 20 m. Preprocessing: apply an 11-point median filter to elevation samples before any gradient calculation to suppress spikes. For gradient computations: clamp gradients above 60% to 60% to avoid extreme outliers dominating score components. When computing gradient distribution, report both percent-of-distance and percent-of-ascent spent above thresholds (10%, 15%, 20%). Use DEM-derived elevations for segments where GPX elevation data is unreliable; record a flag when DEM was used so explainability can show the source. If SRTM resolution causes artifacts on very narrow ridgelines, document and surface as a risk in alpha notes.