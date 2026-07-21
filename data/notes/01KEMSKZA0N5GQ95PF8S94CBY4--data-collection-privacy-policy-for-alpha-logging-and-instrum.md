---
created_at: '2026-01-10T20:30:00Z'
entities:
- Sentry
- Strava
- Reddit
id: 01KEMSKZA0N5GQ95PF8S94CBY4
language: en
source:
  end_turn: 8
  session_id: seed-6a7500ae87535981
  start_turn: 0
tags:
- privacy
- logging
- metrics
- survey
title: Data collection, privacy policy for alpha, logging and instrumentation
type: decision
---

Survey and labeling plan: run a labeling survey in March 2026 targeting ~200 trail runners via Strava clubs and Reddit France trail subs to collect subjective difficulty ratings for calibration. Use these labels to calibrate bucket thresholds and optionally re-weight components. Instrumentation and metrics to collect from day one: number of imports, import success/failure rates, average score, distribution of components, survey click-through and responses, retention (re-imports), and parse/compute latency. Logging: capture import success/failure, parse errors, and feature computation times. Use Sentry for exceptions and error alerting. Privacy and storage: uploaded GPX files are private and encrypted at rest; store only anonymized route metrics for scoring and calibration. Routes are not published or shared publicly unless a share link is explicitly created (sharing deferred). Default anonymized IDs have TTL 90 days; support user-initiated deletion at any time. Alpha privacy text drafted: “Uploaded GPX files are private and encrypted. We store only anonymized route metrics used for scoring. Routes are not shared publicly unless you create a share link. You may delete your GPX at any time from settings.” Budget: €4k contractor, hosting €100/month estimate, incidental €200 for map/elevation API keys if needed.