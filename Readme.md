# Long-Term Investment Tracker Script

## Description

Ce script Pine Script pour TradingView est conçu pour aider les investisseurs à long terme en fournissant des indicateurs clés basés sur le prix moyen d'achat et les volumes de stablecoins accumulés. Il se concentre sur les aspects suivants :

1. **Prix Moyen d'Achat sur 31 Périodes** :
   - Calcule la moyenne mobile simple (SMA) du prix de clôture sur les 31 dernières périodes pour fournir un point de référence pour le prix moyen d'achat.

2. **Volume de Stablecoins Accumulés** :
   - Suivi du volume total de stablecoins accumulés sur la période, en tenant compte des volumes entrants (achats) et sortants (ventes).

3. **Volume des Stablecoins Entrants et Sortants** :
   - Le volume des stablecoins entrants est calculé lorsque le prix de clôture est supérieur au prix d'ouverture (indiquant des achats).
   - Le volume des stablecoins sortants est calculé lorsque le prix de clôture est inférieur au prix d'ouverture (indiquant des ventes).

## Visualisation sur le Graphique

- **Ligne bleue** : Représente le prix moyen d'achat sur les 31 dernières périodes.
- **Ligne verte** : Indique le volume total de stablecoins accumulés (inflows - outflows).
- **Ligne verte supplémentaire** : Représente le volume entrant de stablecoins.
- **Ligne rouge** : Représente le volume sortant de stablecoins.

Des labels sont également ajoutés sur le graphique pour visualiser les volumes accumulés, entrants et sortants.

## Utilisation

Ce script est utile pour les investisseurs qui souhaitent suivre le prix moyen de leurs investissements sur une période donnée, tout en surveillant les flux de stablecoins. Il aide à identifier les périodes d'accumulation et de distribution pour prendre des décisions informées sur l'investissement à long terme.
