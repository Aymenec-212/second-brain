---
created_at: '2026-07-21T12:57:19.106346Z'
entities:
- Proton Drive
- Nextcloud
- iCloud
- Proton
id: 01KY2C1302J6C1BZTFZEGBKN1H
language: en
source:
  end_turn: 1
  session_id: 01KY2BF89B5QKW3ZEM8EBDQNAG
  start_turn: 0
tags:
- privacy
- encryption
- proton
- nextcloud
- icloud
title: Privacy- and security-focused cloud options and constraints
type: fact
---

If privacy and security are primary requirements for my second brain, I must distinguish between provider-managed encryption and true end-to-end encryption (E2EE). Provider-managed encryption secures data at-rest and in-transit but the provider can decrypt data (useful for features like server-side search). E2EE ensures only I hold the keys; this prevents provider access but limits server-side features. Concrete privacy-focused options: Proton Drive (offers E2EE and is suitable for strong privacy without self-hosting) and self-hosted Nextcloud (I control the server, data residency, and can add encrypted storage). iCloud has good Apple privacy practices and integrates tightly with Apple devices but is not E2EE across all services; it is still provider-managed and governed by Apple terms. Self-hosting on a VPS or on-prem NAS gives the strongest control but requires handling backups, updates, and security hardening. Decision criteria: choose E2EE or self-hosting if I cannot accept provider access; choose reputable provider-managed encryption (Proton, Apple, etc.) if I want less maintenance and some server-side functionality.