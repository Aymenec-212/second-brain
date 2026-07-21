---
created_at: '2026-06-02T20:30:00Z'
entities:
- douleur 0–10
- humeur +1/0/-1
- FC repos
id: 01KT50ERA067DB1QKJKEFQDC70
language: fr
source:
  end_turn: 6
  session_id: seed-61fa48bcb5c6945f
  start_turn: 2
tags:
- logging
- metrics
- safety
- knee
title: Logging minimal et protocole sécurité (indicateurs à enregistrer et règle secours)
type: decision
---

Champ de logging minimal à remplir après chaque séance (course et renfo) : 1) durée effective de la séance (min), 2) distance si mesurable (km), 3) douleur au genou sur une échelle 0–10, 4) humeur binaire/ternaire +1 / 0 / −1, 5) fréquence cardiaque de repos si disponible. Application stricte des règles de sécurité : douleur au genou >3/10 = arrêt immédiat de toute course concernée, interdire la course pendant 48 heures après un épisode >3/10, et contacter le kiné si la douleur persiste au-delà de ces 48 heures. Si douleur >5/10, indiquer la situation comme urgente lors du contact (demander un créneau prioritaire). Ces champs servent à détecter une tendance défavorable avant l'évaluation finale du 30/06/2026. Conserver les logs centralisés pour revue au checkpoint kiné et à l'évaluation.