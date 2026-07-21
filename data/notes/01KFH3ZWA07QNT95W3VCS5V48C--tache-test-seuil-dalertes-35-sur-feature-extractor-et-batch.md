---
created_at: '2026-01-21T20:30:00Z'
entities:
- feature-extractor
- batch-trainer
id: 01KFH3ZWA07QNT95W3VCS5V48C
language: fr
source:
  end_turn: 6
  session_id: seed-552fbedefdb54004
  start_turn: 4
tags:
- monitoring
- oncall
- alerting
- metrics
title: 'Tâche : test seuil d’alertes 3→5 sur feature-extractor et batch-trainer (25/01–31/01/2026)'
type: task
---

Plan de test technique : modifier le seuil d’alertes non critiques de 3→5 pour deux services (feature-extractor et batch-trainer) sur la période du 25/01/2026 au 31/01/2026. Objectifs mesurables : réduire le nombre de réveils (actuel 8 wake‑ups/semaine) à ≤2 wake‑ups/semaine et maintenir ou améliorer le MTTR (baseline MTTR = 22 minutes ; objectif MTTR ≤30 minutes). Mesures à collecter : nombre de wake‑ups générés par ces deux services pendant la semaine de test, MTTR observé, taux d’erreurs utilisateurs ou impact client, volume d’incidents reportés. Plan d’exécution : appliquer le changement dans un environnement contrôlé (si possible staging) puis en production avec monitoring serré, avertir l’équipe ops/devs du test et du rollback plan si impact client. Critères d’arrêt : augmentation significative d’erreurs visibles pour les utilisateurs ou perte de SLO. Post‑test : comparer wake‑ups et MTTR à la baseline et décider du rollout plus large ou d’un ajustement.