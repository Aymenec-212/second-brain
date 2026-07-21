---
created_at: '2026-02-21T20:30:00Z'
entities:
- Google Sheet
id: 01KJ0YA5A0Z5DB925GCYEN85A8
language: fr
source:
  end_turn: 6
  session_id: seed-d208127dca95f59d
  start_turn: 4
tags:
- documentation
- google_sheet
- suivi
- expérimentation
- photos
title: Schéma de suivi dans Google Sheet — colonnes et métadonnées à enregistrer
type: task
---

Structure de la ligne à ajouter au carnet (Google Sheet) pour chaque essai — colonnes demandées : date, farine, marque_farines (ex : Le Moulin), eau_temp (°C), levain_age (ex : rafraîchi 8 h avant), hydratation (%), autolyse (durée), BF_time/temp (ex : 1,5 h @24 °C), cold_retard_h (nombre d'heures au frigo), final_proof (durée), bake_time (ex : 20+25), score (note /10), commentaires. Colonnes additionnelles demandées : variante_testée (ex : cold retard vs BF long) et photo (cellule pour coller un lien vers la photo). Comportement attendu : remplir systématiquement la ligne le jour du test avec toutes les variables (marque farine, température de l'eau, activité du levain, poids final, temps exacts), coller le lien photo et indiquer clairement la variante testée pour pouvoir filtrer et comparer rapidement. Cette structure permettra d'analyser l'effet des variations (p. ex. hydratation 78 % ultérieurement) et d'assurer reproductibilité en semaine et le partage éventuel.