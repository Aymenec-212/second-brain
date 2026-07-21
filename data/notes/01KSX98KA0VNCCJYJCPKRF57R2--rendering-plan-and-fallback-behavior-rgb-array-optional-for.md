---
created_at: '2026-05-30T20:30:00Z'
entities:
- PIL
- numpy
- tinygrid
id: 01KSX98KA0VNCCJYJCPKRF57R2
language: en
source:
  end_turn: 4
  session_id: seed-ceb7fcbdee356a98
  start_turn: 4
tags:
- rendering
- rgb
- pillow
- ascii
title: Rendering plan and fallback behavior (rgb_array optional for v0.1)
type: idea
---

Rendering design and fallback decisions: prefer a simple RGB renderer that maps integer cell values to colors and returns an HxW(x3) uint8 numpy array for mode='rgb_array'. Implementation approach: use a small palette dict mapping ints to RGB tuples, draw each grid cell as a colored rectangle (either using Pillow to create an image and resize up for visibility, or constructing an array directly) and return the resulting numpy array. Provide mode='human' that falls back to printing an ASCII map (useful in CI or when no display available). Rendering is optional for v0.1.0: if implementing rgb_array would push the project beyond the baseline estimate, postpone RGB rendering to v0.2 and keep the ASCII human mode only. If implemented, document the mapping and provide a simple color palette and scaling factor parameter for visualization in examples/.