---
created_at: '2026-06-24T20:30:00Z'
entities:
- Google Calendar
- Notion
id: 01KVXN6JA0Y8A3Q8YG4CQ66SVQ
language: fr
source:
  end_turn: 6
  session_id: seed-465c360380dc2bc5
  start_turn: 6
tags:
- revue
- automatisation
- notion
- google calendar
title: 'Rappel hebdo de revue : événement Google Calendar + tâche Notion + automatisation
  de notification'
type: decision
---

Mécanique de revue hebdomadaire pour maintenir la discipline : créer un événement Google Calendar intitulé « Check appel parents (revue) » récurrent chaque lundi à 08:30, durée 10 minutes, début semaine suivant le lancement (commencer 2026-06-29). En parallèle, créer une tâche hebdomadaire automatique dans la page Notion « Journal appels parents » reliée à l'entrée de dimanche. Automatisation attendue : si l'entrée Notion correspondant au dimanche précédent est vide ou n'est pas cochée comme « complété » à 09:00 le lundi, m'envoyer une notification push ponctuelle (sur téléphone) pour compléter l'entrée. Cette automatisation nécessite un outil d'intégration (Zapier/Make/Notion API et service de notifications) ; prévoir configuration technique : trigger = lundi 09:00, condition = entrée non cochée, action = push notification + éventuellement email. Prévoir aussi une exception si j'ai explicitement annulé (SMS envoyé au moins 2h avant) — l'automatisation doit ignorer ces cas. Conserver la tolérance de 2 absences sur 13 semaines ; si la revue constate >2 absences avant 2026-09-24, lancer la réévaluation.