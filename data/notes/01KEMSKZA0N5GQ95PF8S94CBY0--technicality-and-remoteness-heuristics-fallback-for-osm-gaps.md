---
created_at: '2026-01-10T20:30:00Z'
entities:
- OpenStreetMap
id: 01KEMSKZA0N5GQ95PF8S94CBY0
language: en
source:
  end_turn: 6
  session_id: seed-6a7500ae87535981
  start_turn: 6
tags:
- technicality
- osm
- fallback
- gps
title: Technicality and remoteness heuristics; fallback for OSM gaps (GPS-derived
  roughness)
type: decision
---

OSM surface mapping is primary for the technicality component, but gaps and missing surface tags are common — plan explicit fallback heuristics. Surface score design: internal scale 0–50 where smoother surfaces map to 0 and very technical surfaces (rock/boulder) map toward 50. Apply modifiers based on highway/track type (footway, path, track). If surface tag missing, infer from highway/tracktype using a small lookup table for ~10 common tags (e.g., track -> dirt/compacted default, footway/path -> mixed). GPS-derived roughness fallback: compute a numeric roughness metric from the GPX itself to reduce dependence on OSM. Roughness components: (a) elevation residual standard deviation after the 11-point median smoothing, (b) lateral jitter along the track (stddev of cross-track displacement after resampling), and (c) speed jitter (stddev of instantaneous speed after smoothing). Combine these normalized metrics into a 0–50 GPS-derived technicality score. Use GPS-derived technicality when OSM surface is missing or flagged unreliable; blend (e.g., max(OSM_score, GPS_score) or weighted combination) to keep conservative technicality estimates. For remoteness, rely on OSM highways distance but note OSM coverage gaps in very remote regions as a known risk.