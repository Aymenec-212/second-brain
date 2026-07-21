---
created_at: '2026-04-04T20:30:00Z'
entities: []
id: 01KND30BA085H3SGPV7C33CW1D
language: fr
source:
  end_turn: 3
  session_id: seed-d7312064f3523c2f
  start_turn: 1
tags:
- préférences
- arrondi
- unités
title: Préférences d'affichage et règle d'arrondi pour les allures
type: decision
---

Décision claire sur la présentation des allures pour l'entraînement : afficher systématiquement les allures en min/km arrondies à la plus proche tranche de 5 secondes (ex. 3:40, 3:50, 4:00) pour faciliter la lecture pendant les séances quotidiennes, et afficher aussi la vitesse correspondante en km/h. En parallèle, conserver et fournir les valeurs exactes en secondes (précision au dixième ou centième si nécessaire) pour tous les calculs de splits et pour les fractionnés courts où la précision importe : 200 m, 400 m et la distance (en mètres avec décimales) couverte en 30 s. Application concrète déjà retenue : arrondir le pace VMA affiché à 3:40/km mais garder le pace exact 3:38,18/km pour calculs, arrondir tous les paces d'entraînement à 5 s mais fournir les temps exacts pour 200/400 m et pour la distance couverte en 30 s. Cette règle s'appliquera à toutes les fiches d'entraînement et aux exports imprimables.