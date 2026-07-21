---
created_at: '2026-06-24T20:30:00Z'
entities: []
id: 01KVXN6JA0Y8A3Q8YG4CQ66SVS
language: fr
source:
  end_turn: 10
  session_id: seed-465c360380dc2bc5
  start_turn: 10
tags:
- sms
- automatisation
- annulation
- réscheduling
title: 'Automatisation d''annulation <2h : SMS de notification + proposition de 3
  créneaux'
type: decision
---

Règle automatique en cas d'annulation de ma part moins de 2 heures avant l'appel : déclencher en automatique l'envoi d'un SMS aux parents avec le texte standardisé : « Désolé, je dois annuler l'appel de ce soir. On se reprogramme ? » et inclure automatiquement une proposition de trois créneaux possibles pour rattrapage (p. ex. proposer 3 dimanches/soirs alternatifs ou prochains jours disponibles). Technique : nécessite connexion du calendrier à un service d'envoi SMS (Zapier/SMS gateway/IFTTT) et une condition trigger = événement supprimé ou mis comme annulé <2h avant start_time. Prévoir aussi que ce SMS soit loggé automatiquement dans l'entrée Notion du jour comme « annulation envoyée » pour garder trace. Cette règle réduit l'impact émotionnel pour les parents et maintient l'intention de replanifier rapidement.