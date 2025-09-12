# Index de la Documentation - Dashboard Dérivés Actions

## 📋 Vue d'ensemble

Ce document sert d'index complet pour naviguer dans toute la documentation du projet **Dashboard Dérivés Actions**. Chaque section est organisée par thème pour faciliter la recherche d'informations spécifiques.

## 🌐 Accès à l'Application

**Application déployée :** [https://flask-projet-mlg.onrender.com](https://flask-projet-mlg.onrender.com)

**Développement local :** `http://localhost:5000`

## 🚀 Documentation Principale

### [README_PRINCIPAL.md](README_PRINCIPAL.md)
**Vue d'ensemble complète du projet**
- Installation et configuration
- Structure du projet
- Fonctionnalités principales
- Guide d'utilisation
- APIs disponibles
- Performance et optimisation
- Pages principales et de debug

### [README_RECENT_UPDATES.md](README_RECENT_UPDATES.md)
**Mises à jour récentes (Janvier 2025)**
- Nettoyage et optimisation du projet
- Suppression des fichiers de test et exports temporaires
- Renommage "Tweet Analysis"
- Corrections de code
- Documentation mise à jour

## 🎯 Fonctionnalités Avancées

### [README_CALL_PUT_CALCULATIONS.md](README_CALL_PUT_CALCULATIONS.md)
**Calculs d'options Call & Put**
- Modèle Black-Scholes avec tous les grecques
- Simulation Monte Carlo avec intervalles de confiance
- Comparaison des modèles
- Validation et tests
- Exemples de calculs

### [README_RISK_METRICS.md](README_RISK_METRICS.md)
**Métriques de risque avancées**
- Value at Risk (VaR) historique et paramétrique
- Conditional VaR (CVaR)
- Volatilité et rendements
- Maximum Drawdown
- Ratios de performance (Sharpe, Sortino)

### [README_VOLATILITY_SMILE.md](README_VOLATILITY_SMILE.md)
**Smile de volatilité**
- Visualisation du smile pour une maturité spécifique
- Analyse des formes de smile (symétrique, skew, inversé)
- Données réelles via Finnhub API
- Interprétation et cas d'usage

### [README_DATA_EXPORT.md](README_DATA_EXPORT.md)
**Export de données**
- Formats supportés : JSON, CSV, Excel
- Métadonnées incluses
- API endpoints d'export
- Cas d'usage et intégration

## 🔌 APIs et Données

### [README_API_STATUS.md](README_API_STATUS.md)
**Monitoring API en temps réel**
- Indicateurs de statut API
- Gestion des erreurs et limites
- Métriques de performance
- Améliorations futures

### [README_VOLATILITY_SURFACE.md](README_VOLATILITY_SURFACE.md)
**Surface de volatilité 2D**
- Visualisation 2D des surfaces de volatilité
- Données multi-sources (Finnhub, Polygon.io)
- Filtrage et nettoyage des données
- Statistiques avancées

### [README_POLYGON_INTEGRATION.md](README_POLYGON_INTEGRATION.md)
**Intégration Polygon.io**
- Données d'options avancées
- Gestion des limites de taux
- Fallback vers Finnhub
- Optimisations de performance

### [README_FINNHUB_IMPLIED_VOLATILITY.md](README_FINNHUB_IMPLIED_VOLATILITY.md)
**Volatilité implicite Finnhub**
- Extraction des données d'options
- Calcul de la volatilité implicite
- Gestion des expirations
- Validation des données

## 🛠️ Développement et Optimisations

### [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)
**Pages et routes de l'application**
- Documentation complète de toutes les pages
- Routes API disponibles
- Structure de navigation
- Pages de debug et test
- Guide d'utilisation par type d'utilisateur

### [README_TESTS_ORGANIZATION.md](README_TESTS_ORGANIZATION.md)
**Organisation des tests**
- Structure du dossier tests
- Types de tests (unitaires, intégration, performance)
- Configuration technique
- Bonnes pratiques
- Intégration continue

### [README_PROGRESS_BARS.md](README_PROGRESS_BARS.md)
**Barres de progression**
- Interface utilisateur pour le chargement
- Indicateurs de progression
- Gestion des états de chargement
- Amélioration de l'expérience utilisateur

### [README_STRIKE_PERCENTAGE_IMPROVEMENT.md](README_STRIKE_PERCENTAGE_IMPROVEMENT.md)
**Améliorations des strikes**
- Filtrage intelligent des strikes
- Optimisation de la couverture des données
- Amélioration de la précision
- Gestion des données manquantes

### [README_AUDIT_VOLATILITY_SURFACE.md](README_AUDIT_VOLATILITY_SURFACE.md)
**Audit de la surface de volatilité**
- Validation des données
- Détection des anomalies
- Qualité des données
- Recommandations d'amélioration

### [README_VOLATILITY_SURFACE_CLEANUP.md](README_VOLATILITY_SURFACE_CLEANUP.md)
**Nettoyage de la surface de volatilité**
- Filtrage des données aberrantes
- Interpolation des données manquantes
- Lissage des surfaces
- Amélioration de la visualisation

### [README_FINAL_3D_CORRECTIONS.md](README_FINAL_3D_CORRECTIONS.md)
**Corrections finales 3D**
- Optimisations de la visualisation 3D
- Corrections des bugs de rendu
- Amélioration des performances
- Finalisation de l'interface

### [README_FINAL_GRAPH_FIX.md](README_FINAL_GRAPH_FIX.md)
**Corrections finales des graphiques**
- Résolution des problèmes d'affichage
- Optimisation des graphiques 2D
- Amélioration de la réactivité
- Tests et validation

### [README_BLACK_SQUARE_REMOVAL.md](README_BLACK_SQUARE_REMOVAL.md)
**Suppression du carré noir**
- Résolution du bug d'affichage
- Correction du rendu 3D
- Amélioration de la transparence
- Tests de validation

## 🎯 Pages et Routes

### Pages Principales
- **Accueil** (`/`) - Dashboard principal
- **CV Mathis Le Gall** (`/cv-mathis-le-gall`) - Page personnelle
- **Indices & Actions** (`/indices-actions`) - Données de marché
- **Call & Put** (`/call-put`) - Calculs d'options
- **Surface de Volatilité** (`/volatility-surface`) - Visualisation 3D
- **Analyse Actions Indices** (`/analyse-actions-indices`) - Comparaison de performances
- **Analyse des Grecques** (`/analyse-greeks`) - Analyse avancée des options
- **Description App** (`/description-app`) - Documentation de l'application

### Pages de Debug et Test
- **Force Refresh** (`/force-refresh`) - Rafraîchissement forcé
- **Test Vol Surface** (`/test-vol-surface`) - Test de la surface de volatilité
- **Debug Finnhub** (`/debug-finnhub`) - Debug de l'API Finnhub
- **Debug Polygon** (`/debug-polygon`) - Debug de l'API Polygon.io
- **Test Indices Actions** (`/test-indices-actions`) - Test des données de marché

### APIs Disponibles
- **Données de marché** : `/api/market-data`, `/api/indices`, `/api/stocks`
- **Graphiques** : `/api/chart-data/<symbol>`, `/api/chart-data-v2/<symbol>`
- **Options** : `/api/vol-surface/<symbol>`, `/api/vol-surface-3d/<symbol>`
- **Calculs** : `/api/calculate-option`, `/api/risk-metrics/<symbol>`
- **Export** : `/api/vol-surface-3d-export/<symbol>`
- **Utilitaires** : `/api/volatility-smile/<symbol>`, `/api/available-symbols`

## 🔍 Recherche Rapide

### Par Fonctionnalité
- **Calculs d'options** → [README_CALL_PUT_CALCULATIONS.md](README_CALL_PUT_CALCULATIONS.md)
- **Métriques de risque** → [README_RISK_METRICS.md](README_RISK_METRICS.md)
- **Surface de volatilité** → [README_VOLATILITY_SURFACE.md](README_VOLATILITY_SURFACE.md)
- **Smile de volatilité** → [README_VOLATILITY_SMILE.md](README_VOLATILITY_SMILE.md)
- **Export de données** → [README_DATA_EXPORT.md](README_DATA_EXPORT.md)

### Par API
- **Yahoo Finance** → [README_PRINCIPAL.md](README_PRINCIPAL.md) (section Données Financières)
- **Finnhub** → [README_FINNHUB_IMPLIED_VOLATILITY.md](README_FINNHUB_IMPLIED_VOLATILITY.md)
- **Polygon.io** → [README_POLYGON_INTEGRATION.md](README_POLYGON_INTEGRATION.md)
- **Monitoring API** → [README_API_STATUS.md](README_API_STATUS.md)

### Par Problème
- **Performance lente** → [README_FINAL_3D_CORRECTIONS.md](README_FINAL_3D_CORRECTIONS.md)
- **Erreurs d'affichage** → [README_FINAL_GRAPH_FIX.md](README_FINAL_GRAPH_FIX.md)
- **Données manquantes** → [README_STRIKE_PERCENTAGE_IMPROVEMENT.md](README_STRIKE_PERCENTAGE_IMPROVEMENT.md)
- **Problèmes API** → [README_API_STATUS.md](README_API_STATUS.md)

### Par Page
- **Pages principales** → [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)
- **Pages de debug** → [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)
- **APIs** → [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)

### Par Tests
- **Organisation des tests** → [README_TESTS_ORGANIZATION.md](README_TESTS_ORGANIZATION.md)
- **Documentation des tests** → [tests/README.md](../tests/README.md)
- **Exécution des tests** → [tests/run_tests.py](../tests/run_tests.py)

## 📊 Structure du Projet

```
flaskProjectMathisLeGall/
├── app.py                          # Application Flask principale
├── api/                            # Modules API
│   ├── yahoo_finance_api.py        # Données de marché
│   ├── finnhub_implied_volatility.py  # Volatilité implicite
│   ├── finnhub_volatility_smile.py    # Smile de volatilité
├── models/                         # Modèles de calcul
│   ├── options_pricing.py          # Calculs d'options
│   ├── risk_metrics.py             # Métriques de risque
│   └── volatility_surface_3d.py    # Surface de volatilité 3D
├── tests/                          # Tests de l'application
│   ├── README.md                   # Documentation des tests
│   ├── test_app.py                 # Tests principaux (40 tests)
│   ├── run_tests.py                # Script d'exécution
│   └── pytest.ini                 # Configuration pytest
├── templates/                      # Templates HTML
├── static/                         # Fichiers statiques
└── docs/                          # Documentation complète
    ├── INDEX.md                    # Ce fichier
    ├── README_PRINCIPAL.md         # Documentation principale
    └── [autres README...]          # Documentation spécialisée
```

## 🎯 Guide de Démarrage Rapide

### Pour les Nouveaux Utilisateurs
1. **Installation** → [README_PRINCIPAL.md](README_PRINCIPAL.md) (section Installation)
2. **Première utilisation** → [README_PRINCIPAL.md](README_PRINCIPAL.md) (section Utilisation)
3. **Fonctionnalités de base** → [README_PRINCIPAL.md](README_PRINCIPAL.md) (section Fonctionnalités)

### Pour les Développeurs
1. **Architecture** → [README_PRINCIPAL.md](README_PRINCIPAL.md) (section Structure)
2. **APIs** → [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)
3. **Tests** → [tests/README.md](../tests/README.md)
4. **Optimisations** → Section Développement et Optimisations ci-dessus
5. **Pages de debug** → [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)

### Pour les Utilisateurs Avancés
1. **Calculs d'options** → [README_CALL_PUT_CALCULATIONS.md](README_CALL_PUT_CALCULATIONS.md)
2. **Métriques de risque** → [README_RISK_METRICS.md](README_RISK_METRICS.md)
3. **Export de données** → [README_DATA_EXPORT.md](README_DATA_EXPORT.md)
4. **Surface de volatilité 3D** → [README_3D_VOLATILITY_SURFACE.md](README_3D_VOLATILITY_SURFACE.md)

## 📞 Support et Contact

Pour toute question ou problème :
- **Documentation technique** : Consulter les README appropriés
- **Bugs et problèmes** : Vérifier les README de développement
- **Nouvelles fonctionnalités** : Consulter les README de fonctionnalités
- **Pages de debug** : [README_PAGES_AND_ROUTES.md](README_PAGES_AND_ROUTES.md)

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 2.1.0 - Index complet de la documentation avec toutes les pages et APIs
