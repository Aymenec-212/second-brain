---
created_at: '2026-07-06T20:30:00Z'
entities:
- product
- support
- Docker v1.14.2
- rollback.sh
id: 01KWWHZ6A0TNG6FJGBVZ6HK7AV
language: fr
source:
  end_turn: 4
  session_id: seed-b66da2d1155af981
  start_turn: 2
tags:
- déploiement
- communication
- fallback
- infrastructure
title: 'Décision : message Slack 08:00 — proposer repoussage du deploy à 17:00 + fallback
  canary 5%'
type: decision
---

Je vais envoyer un message Slack à 08:00 pour aligner product et support sur le plan du jour : télétravail 8:30–12:30, run 7:00–7:50, proposition de repousser le déploiement ML à 17:00 pour limiter les risques liés à la chaleur et à la charge. Contraintes connues : équipe product a réunion à 16:00, support prévoit un pic d'activité à 18:00 selon le rota. Si product insiste pour garder la fenêtre matin, je maintiens 11:30 mais réduis la portée initiale du rollout : canary à 5% d'abord, avec health checks serrés. Message Slack inclura explicitement le plan de rollback pour rassurer : tag Docker v1.14.2 prêt et script rollback.sh testé. Action connexe : patcher le cron heavy job (job CPU-bound) et le déplacer après 19:00 pour éviter concurrence de ressources au moment du déploiement. Ce message vise à obtenir un vote/OK rapide et à documenter le fallback opérationnel.