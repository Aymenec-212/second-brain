---
created_at: '2026-04-02T20:30:00Z'
entities:
- PagerDuty
- Thomas
id: 01KN7Y6XA0HB2RNW296ET3MXYM
language: fr
source:
  end_turn: 4
  session_id: seed-9a873c331bacdc3a
  start_turn: 1
tags:
- on-call
- pagerduty
- feature-phone
- séparation
title: Plan on-call et décision d'un feature phone dédié
type: decision
---

Contraintes on-call : fréquence approximative 2 fois par mois avec nécessité de recevoir les alertes PagerDuty et un appel si c'est urgent. Compromis choisi : garder le téléphone principal hors de la chambre mais acheter un feature phone économique (~30€ budget) dédié à l'on-call, avec la SIM on-call installée et posé dans le couloir. Configuration du téléphone principal concernant les appels : autoriser uniquement les appels de Thomas (manager) et les alertes PagerDuty ; toutes les autres notifications Slack/génériques seront muettes la nuit. En situation d'urgence, PagerDuty et appels passent via le feature phone pour minimiser les interruptions sur le téléphone principal tout en répondant aux obligations on-call.