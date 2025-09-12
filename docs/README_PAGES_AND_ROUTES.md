# Pages et Routes - Dashboard Dérivés Actions

## 📋 Vue d'ensemble

Ce document détaille toutes les pages et routes disponibles dans l'application Flask **Dashboard Dérivés Actions**. Il sert de référence complète pour comprendre la structure de navigation et les fonctionnalités accessibles.

## 🏠 Pages Principales

### Page d'Accueil
- **Route** : `/`
- **Template** : `templates/index.html`
- **Description** : Dashboard principal avec vue d'ensemble des fonctionnalités
- **Fonctionnalités** :
  - Navigation vers toutes les sections
  - Aperçu des données de marché
  - Accès rapide aux fonctionnalités principales

### CV Mathis Le Gall
- **Route** : `/cv-mathis-le-gall`
- **Template** : `templates/cv_mathis_le_gall.html`
- **Description** : Page personnelle avec CV et informations de contact
- **Fonctionnalités** :
  - Présentation professionnelle
  - Compétences techniques
  - Expériences et projets

### Indices et Actions
- **Route** : `/indices-actions`
- **Template** : `templates/indices_actions.html`
- **Description** : Données de marché en temps réel
- **Fonctionnalités** :
  - Données des indices boursiers
  - Données des actions
  - Graphiques interactifs
  - Métriques de risque
  - Actualisation automatique

### Calculs Call & Put
- **Route** : `/call-put`
- **Template** : `templates/call_put.html`
- **Description** : Calculs d'options Call et Put
- **Fonctionnalités** :
  - Modèle Black-Scholes
  - Simulation Monte Carlo
  - Calcul des grecques
  - Intervalles de confiance
  - Visualisation des trajectoires

### Surface de Volatilité
- **Route** : `/volatility-surface`
- **Template** : `templates/volatility_surface.html`
- **Description** : Visualisation 3D des surfaces de volatilité
- **Fonctionnalités** :
  - Surface de volatilité 3D interactive
  - Contrôles de visualisation (Surface, Wireframe, Contour)
  - Smile de volatilité
  - Export de données
  - Statistiques avancées

### Analyse Actions Indices
- **Route** : `/analyse-actions-indices`
- **Template** : `templates/analyse_actions_indices.html`
- **Description** : Comparaison de performances (Base 100)
- **Fonctionnalités** :
  - Comparaison relative des performances
  - Analyse de corrélation
  - Graphiques de comparaison
  - Métriques de performance

### Analyse des Grecques
- **Route** : `/analyse-greeks`
- **Template** : `templates/analyse_greeks.html`
- **Description** : Analyse avancée des grecques d'options
- **Fonctionnalités** :
  - Calcul des grecques (Delta, Gamma, Theta, Vega, Rho)
  - Sensibilité aux paramètres
  - Visualisation des grecques
  - Analyse de risque

### Tweet Analysis
- **Route** : `/analyse-volatility`
- **Template** : `templates/analyse_volatility.html`
- **Description** : Analyse des tweets et des sentiments du marché (en développement)
- **Fonctionnalités** :
  - Analyse de sentiment des tweets financiers
  - Mots-clés tendances
  - Influence des utilisateurs
  - Corrélation prix-tweets
  - Prédiction de volatilité
  - Alertes en temps réel

### Description de l'Application
- **Route** : `/description-app`
- **Template** : `templates/description_app.html`
- **Description** : Documentation de l'application
- **Fonctionnalités** :
  - Présentation des fonctionnalités
  - Guide d'utilisation
  - Architecture technique
  - Technologies utilisées

## 🐛 Pages de Debug et Test

### Force Refresh
- **Route** : `/force-refresh`
- **Template** : `templates/force_refresh.html`
- **Description** : Page pour forcer le rafraîchissement des données
- **Fonctionnalités** :
  - Rafraîchissement manuel des données
  - Réinitialisation du cache
  - Diagnostic des problèmes de données

### Test Vol Surface
- **Route** : `/test-vol-surface`
- **Template** : `test_vol_surface_debug.html`
- **Description** : Page de test pour debug de la surface de volatilité
- **Fonctionnalités** :
  - Test des données de volatilité
  - Validation des calculs
  - Diagnostic des erreurs

### Debug Finnhub
- **Route** : `/debug-finnhub`
- **Template** : `templates/debug_finnhub.html`
- **Description** : Page de débogage pour l'API Finnhub
- **Fonctionnalités** :
  - Test de connectivité API
  - Validation des données
  - Diagnostic des erreurs
  - Monitoring des limites

### Debug Polygon
- **Route** : `/debug-polygon`
- **Template** : `templates/debug_polygon.html`
- **Description** : Page de débogage pour l'API Polygon.io
- **Fonctionnalités** :
  - Test de connectivité API
  - Validation des données
  - Diagnostic des erreurs
  - Monitoring des limites

### Test Indices Actions
- **Route** : `/test-indices-actions`
- **Template** : `test_indices_actions.html`
- **Description** : Page de test pour les indices et actions
- **Fonctionnalités** :
  - Test des données de marché
  - Validation des calculs
  - Diagnostic des erreurs

## 🔌 APIs Disponibles

### Données de Marché

#### GET /api/market-data
- **Description** : Données générales (indices + actions)
- **Paramètres** : Aucun
- **Retour** : JSON avec données des indices et actions
- **Utilisation** : Données de base pour le dashboard

#### GET /api/indices
- **Description** : Données des indices uniquement
- **Paramètres** : Aucun
- **Retour** : JSON avec données des indices
- **Utilisation** : Données spécifiques aux indices

#### GET /api/stocks
- **Description** : Données des actions uniquement
- **Paramètres** : Aucun
- **Retour** : JSON avec données des actions
- **Utilisation** : Données spécifiques aux actions

### Graphiques

#### GET /api/chart-data/<symbol>
- **Description** : Données de graphique pour un symbole
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec données de graphique
- **Utilisation** : Graphiques de prix

#### GET /api/chart-data-v2/<symbol>
- **Description** : Données de graphique avec timeframe
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec données de graphique et timeframe
- **Utilisation** : Graphiques avancés avec périodes

### Options et Volatilité

#### GET /api/vol-surface/<symbol>
- **Description** : Surface de volatilité 2D
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec surface de volatilité 2D
- **Utilisation** : Visualisation 2D des volatilités

#### GET /api/vol-surface-3d/<symbol>
- **Description** : Surface de volatilité 3D
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec surface de volatilité 3D
- **Utilisation** : Visualisation 3D interactive

#### GET /api/vol-surface-3d-export/<symbol>
- **Description** : Export des données 3D
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : Fichier JSON/CSV/Excel
- **Utilisation** : Export des données pour analyse externe

#### GET /api/volatility-smile/<symbol>
- **Description** : Smile de volatilité
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec smile de volatilité
- **Utilisation** : Analyse du smile de volatilité

### Calculs Financiers

#### POST /api/calculate-option
- **Description** : Calculs d'options Call & Put
- **Paramètres** : JSON avec paramètres d'option
- **Retour** : JSON avec résultats des calculs
- **Utilisation** : Calculs Black-Scholes et Monte Carlo

#### GET /api/risk-metrics/<symbol>
- **Description** : Métriques de risque
- **Paramètres** : `symbol` (symbole boursier)
- **Retour** : JSON avec métriques de risque
- **Utilisation** : Analyse de risque (VaR, CVaR, etc.)

### Utilitaires

#### GET /api/available-symbols
- **Description** : Symboles disponibles
- **Paramètres** : Aucun
- **Retour** : JSON avec liste des symboles
- **Utilisation** : Sélection de symboles dans l'interface

## 🎯 Navigation et Structure

### Structure de Navigation
```
Dashboard Principal (/)
├── CV Mathis Le Gall (/cv-mathis-le-gall)
├── Indices & Actions (/indices-actions)
├── Call & Put (/call-put)
├── Surface de Volatilité (/volatility-surface)
├── Analyse Actions Indices (/analyse-actions-indices)
├── Analyse des Grecques (/analyse-greeks)
├── Description App (/description-app)
└── Pages de Debug
    ├── Force Refresh (/force-refresh)
    ├── Test Vol Surface (/test-vol-surface)
    ├── Debug Finnhub (/debug-finnhub)
    ├── Debug Polygon (/debug-polygon)
    └── Test Indices Actions (/test-indices-actions)
```

### Flux d'Utilisation Recommandé

#### Pour les Nouveaux Utilisateurs
1. **Accueil** → Vue d'ensemble
2. **Description App** → Comprendre les fonctionnalités
3. **Indices & Actions** → Données de base
4. **Surface de Volatilité** → Fonctionnalité principale

#### Pour les Utilisateurs Avancés
1. **Call & Put** → Calculs d'options
2. **Analyse des Grecques** → Analyse avancée
3. **Analyse Actions Indices** → Comparaisons
4. **Pages de Debug** → Diagnostic si nécessaire

#### Pour les Développeurs
1. **Pages de Debug** → Diagnostic des APIs
2. **Test Vol Surface** → Validation des calculs
3. **Force Refresh** → Réinitialisation des données

## 🔧 Configuration et Développement

### Ajout de Nouvelles Pages
1. **Créer la route** dans `app.py`
2. **Créer le template** dans `templates/`
3. **Mettre à jour la navigation** dans les templates de base
4. **Documenter** dans ce README

### Ajout de Nouvelles APIs
1. **Créer la route API** dans `app.py`
2. **Implémenter la logique** dans les modules appropriés
3. **Ajouter la documentation** dans ce README
4. **Tester** avec les pages de debug

### Gestion des Erreurs
- **Pages principales** : Gestion d'erreur utilisateur-friendly
- **Pages de debug** : Affichage détaillé des erreurs
- **APIs** : Retour d'erreurs JSON standardisées

## 📊 Métriques et Monitoring

### Pages les Plus Utilisées
- **Surface de Volatilité** : Fonctionnalité principale
- **Indices & Actions** : Données de base
- **Call & Put** : Calculs d'options

### APIs les Plus Appelées
- **/api/market-data** : Données de base
- **/api/vol-surface-3d** : Surface de volatilité
- **/api/calculate-option** : Calculs d'options

### Performance
- **Pages principales** : < 2 secondes de chargement
- **APIs de données** : < 3 secondes de réponse
- **Calculs complexes** : 5-15 secondes selon la complexité

## 🎯 Notes Techniques

- **Toutes les pages** utilisent les templates de base Flask
- **Navigation cohérente** entre toutes les pages
- **Gestion d'état** pour les données de session
- **Cache intelligent** pour optimiser les performances
- **Pages de debug** pour le développement et maintenance
- **Documentation complète** de toutes les routes et APIs

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 1.0.0 - Documentation complète des pages et routes

