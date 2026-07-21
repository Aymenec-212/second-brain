---
created_at: '2026-01-21T20:30:00Z'
entities:
- phone
- Slack
- email digest
id: 01KFH3ZWA07QNT95W3VCS5V48F
language: fr
source:
  end_turn: 8
  session_id: seed-552fbedefdb54004
  start_turn: 8
tags:
- automation
- notifications
- dnd
- phones
title: 'Idée technique : automatiser Do Not Disturb + redirection des notifications
  non‑P1 vers digest'
type: idea
---

Idée d’amélioration opérationnelle pour réduire les interruptions : activer automatiquement le mode Do Not Disturb sur le téléphone et sur Slack pendant les blocs deep‑work hors des alertes de priorité P1, et configurer la redirection des notifications non‑P1 vers un digest email regroupé. Détails techniques envisagés : définir des règles DND horaires (09:00–12:30 M/Tu/Th/F), autoriser uniquement les alertes P1 à sonner/pager, utiliser la plateforme d’alerting pour rerouter P2/P3 vers un digest ou un canal à revue asynchrone, et mettre en place un auto‑reply Slack indiquant "deep work — répondre avant 12:30 sauf P1". Points à vérifier : qui a accès à la configuration des alertes, risque de masquer un incident réel, intégration avec l’outil de paging, et test d’un rollout pour s’assurer qu’il n’impacte pas les SLO. Prochaines étapes : déterminer le responsable implémentation (ops/devops), tester sur deux services la semaine du 25/01 et monitorer wake‑ups et MTTR.