---
created_at: '2026-01-10T20:30:00Z'
entities:
- React
- OSM
id: 01KEMSKZA0N5GQ95PF8S94CBY3
language: en
source:
  end_turn: 8
  session_id: seed-6a7500ae87535981
  start_turn: 6
tags:
- ui
- contractor
- mobile
- design
- scope
title: Contractor UI scope for €4k, mobile-first and quick delivery checklist
type: task
---

Contractor scope (aim for ~2 weeks of work, mobile-first): required pages/components: - Landing + Import page with drag-and-drop and file picker (mobile-friendly), client-side validation for size/type. - Import progress state and error messages. - Route result page: compact mobile score card showing numeric score, bucket, and component breakdown (distance, ascent, max gradient, technicality, remoteness, altitude) with small visual bars and numeric values. - PNG export of the score breakdown as a shareable social card. - Link/button to download original .gpx. Minimal map: a simplified static polyline rendering (use an OSM static tile or draw SVG polyline without full slippy map tiles) to avoid heavy tile costs and time. Accessibility and responsive layout required (mobile-first). Non-required to keep scope: auth, route sharing links (deferred to v1.1), offline maps, user accounts. Ask contractor to implement compact error states, and basic styling theme to be easily adjustable.