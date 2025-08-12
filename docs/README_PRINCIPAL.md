# Dashboard Dérivés Actions - Flask

Un dashboard moderne pour l'analyse des dérivés d'actions, développé avec Flask et données financières en temps réel.

## 🚀 Fonctionnalités Principales

- **Interface moderne** avec Tailwind CSS et Lucide Icons
- **Navigation intuitive** avec sidebar responsive
- **Données financières en temps réel** via Yahoo Finance API
- **Actualisation automatique** toutes les 5 minutes
- **Graphiques interactifs** avec Chart.js et Plotly.js
- **Surface de volatilité 3D** interactive avec contrôles avancés
- **Calculs d'options Call & Put** avec Monte Carlo et Black-Scholes
- **Métriques de risque** avancées (VaR, CVaR, volatilité, etc.)
- **Smile de volatilité** pour une maturité spécifique
- **Monitoring API en temps réel** avec indicateurs de statut
- **Export de données** en JSON, CSV et Excel
- **Pages spécialisées** :
  - Indices & Actions (avec données live)
  - Call & Put (calculs d'options)
  - Surface de Volatilité (2D et 3D)
  - Analyse Actions Indices (comparaison de performances)
  - Analyse des Grecques (analyse avancée des options)
  - CV Mathis Le Gall (page personnelle)
  - Description de l'application
  - Pages de debug et test

## 🎯 Fonctionnalités Avancées

### Surface de Volatilité 3D Interactive
- **Visualisation 3D** avec Plotly.js
- **Contrôles interactifs** : Surface, Wireframe, Contour
- **Échelles de couleurs** personnalisables
- **Indicateur de prix spot** en temps réel
- **Statistiques avancées** : Min, Max, Moyenne, Écart-type
- **Performance optimisée** avec limitation intelligente des maturités
- **Export de données** en multiples formats

### Calculs d'Options Call & Put
- **Modèle Black-Scholes** avec tous les grecques
- **Simulation Monte Carlo** avec intervalles de confiance
- **Grecques calculées** : Delta, Gamma, Theta, Vega, Rho
- **Trajectoires simulées** pour visualisation
- **Comparaison des modèles** en temps réel

### Métriques de Risque
- **Value at Risk (VaR)** historique et paramétrique
- **Conditional VaR (CVaR)**
- **Volatilité** historique et annualisée
- **Rendements** journaliers et cumulés
- **Skewness et Kurtosis**
- **Maximum Drawdown**

### Smile de Volatilité
- **Visualisation du smile** pour une maturité spécifique
- **Données réelles** via Finnhub API
- **Filtrage par bande** autour du prix spot
- **Statistiques détaillées** du smile

## 📦 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/MathisLeGallCytech/option-vision-hub.git
cd option-vision-hub
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configuration des APIs (optionnel)**
```bash
# Pour Finnhub (données d'options)
# Créer api/finnhub_config.py avec votre clé API

# Pour Polygon.io (données d'options avancées)
# Ajouter votre clé API dans le code

# Pour Alpha Vantage (données alternatives)
# Ajouter votre clé API dans le code
```

6. **Lancer l'application**
```bash
python app.py
```

7. **Ouvrir dans le navigateur**
```
http://localhost:5000
```

## 🏗️ Structure du Projet

```
flaskProjectNatixisMathisLeGall/
├── app.py                 # Application Flask principale
├── api/                   # Modules API
│   ├── __init__.py
│   ├── alpha_vantage_api.py      # API Alpha Vantage
│   ├── finnhub_config.py         # Configuration Finnhub
│   ├── finnhub_implied_volatility.py  # Volatilité implicite Finnhub
│   ├── finnhub_volatility_smile.py    # Smile de volatilité Finnhub
│   ├── polygon_options_api.py         # API Polygon.io
│   └── yahoo_finance_api.py           # API Yahoo Finance
├── models/                # Modèles de calcul
│   ├── __init__.py
│   ├── implied_volatility_extractor.py  # Extracteur de volatilité
│   ├── implied_volatility_final.py      # Volatilité finale
│   ├── options_pricing.py               # Calculs d'options
│   ├── risk_metrics.py                  # Métriques de risque
│   └── volatility_surface_3d.py         # Surface de volatilité 3D
├── tests/                 # Tests de l'application
│   ├── __init__.py
│   ├── README.md              # Documentation des tests
│   ├── README_TESTS.md        # Documentation détaillée
│   ├── RESUME_TESTS.md        # Résumé des tests
│   ├── test_app.py            # Tests principaux (40 tests)
│   ├── run_tests.py           # Script d'exécution
│   └── pytest.ini            # Configuration pytest
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation principale
├── docs/                 # Documentation complète
│   ├── INDEX.md
│   ├── README_PRINCIPAL.md
│   ├── README_API_STATUS.md
│   ├── README_VOLATILITY_SURFACE.md
│   ├── README_POLYGON_INTEGRATION.md
│   ├── README_FINNHUB_IMPLIED_VOLATILITY.md
│   ├── README_PROGRESS_BARS.md
│   ├── README_STRIKE_PERCENTAGE_IMPROVEMENT.md
│   ├── README_AUDIT_VOLATILITY_SURFACE.md
│   ├── README_VOLATILITY_SURFACE_CLEANUP.md
│   ├── README_FINAL_3D_CORRECTIONS.md
│   ├── README_FINAL_GRAPH_FIX.md
│   ├── README_BLACK_SQUARE_REMOVAL.md
│   ├── README_CALL_PUT_CALCULATIONS.md
│   ├── README_RISK_METRICS.md
│   ├── README_VOLATILITY_SMILE.md
│   ├── README_DATA_EXPORT.md
│   └── README_PAGES_AND_ROUTES.md
├── static/               # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── logo_natixis.png
├── templates/            # Templates HTML Jinja2
│   ├── base.html         # Template de base
│   ├── base_flask.html   # Template Flask
│   ├── index.html        # Page d'accueil
│   ├── indices_actions.html
│   ├── call_put.html
│   ├── volatility_surface.html
│   ├── volatility_surface_old.html
│   ├── analyse_actions_indices.html
│   ├── analyse_greeks.html
│   ├── cv_mathis_le_gall.html
│   ├── description_app.html
│   └── force_refresh.html
└── venv/                 # Environnement virtuel Python
```

## 🎨 Interface

L'interface utilise :
- **Tailwind CSS** pour le styling
- **Lucide Icons** pour les icônes
- **Chart.js** pour les graphiques 2D
- **Plotly.js** pour les graphiques 3D
- **Design system** cohérent avec thème sombre
- **Layout responsive** adapté à tous les écrans
- **Indicateurs de statut API** en temps réel

## 📊 Données Financières

### APIs utilisées :
- **Yahoo Finance** (gratuit, pas de clé requise) - Données de base
- **Finnhub** (clé API requise) - Données d'options et volatilité implicite
- **Polygon.io** (clé API requise) - Données d'options avancées
- **Alpha Vantage** (optionnel, 500 requêtes/jour gratuites) - Données alternatives

### Indices suivis :
- CAC 40 (^FCHI)
- S&P 500 (^GSPC)
- NASDAQ (^IXIC)
- DAX (^GDAXI)
- FTSE 100 (^FTSE)
- NIKKEI (^N225)
- Dow Jones (^DJI)
- STOXX 50 (^STOXX50E)

### Actions suivies :
- **Tech US** : AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, ADBE, CRM, INTC, ORCL, CSCO, PYPL, AVGO
- **Europe** : LVMH.PA, ASML.AS, SAP.DE, NESN.SW, AIR.PA, BAYN.DE
- **Asie** : 005930.KS, 0700.HK
- **Aéronautique** : BA

### Symboles recommandés pour les options :
- **SPY** - SPDR S&P 500 ETF (37 maturités)
- **QQQ** - Invesco QQQ Trust (38 maturités)
- **AAPL** - Apple Inc (30 maturités)
- **TSLA** - Tesla Inc (26 maturités)

## 🎯 Utilisation des Fonctionnalités

### Pages Principales
- **Accueil** : `http://localhost:5000/`
- **CV Mathis Le Gall** : `http://localhost:5000/cv-mathis-le-gall`
- **Indices & Actions** : `http://localhost:5000/indices-actions`
- **Call & Put** : `http://localhost:5000/call-put`
- **Surface de Volatilité** : `http://localhost:5000/volatility-surface`
- **Analyse Actions Indices** : `http://localhost:5000/analyse-actions-indices`
- **Analyse des Grecques** : `http://localhost:5000/analyse-greeks`
- **Description App** : `http://localhost:5000/description-app`

### Pages de Debug et Test
- **Force Refresh** : `http://localhost:5000/force-refresh`
- **Test Vol Surface** : `http://localhost:5000/test-vol-surface`
- **Debug Finnhub** : `http://localhost:5000/debug-finnhub`
- **Debug Polygon** : `http://localhost:5000/debug-polygon`
- **Test Indices Actions** : `http://localhost:5000/test-indices-actions`

### Surface de Volatilité 3D
```
http://localhost:5000/volatility-surface
```
1. **Sélectionner un symbole** : SPY, QQQ, AAPL, TSLA recommandés
2. **Choisir le fournisseur** : Finnhub (par défaut) ou Polygon.io
3. **Cliquer sur "Charger la Surface"**
4. **Utiliser les contrôles 3D** : Surface, Wireframe, Contour
5. **Exporter les données** : JSON, CSV, Excel

### Calculs d'Options Call & Put
```
http://localhost:5000/call-put
```
1. **Saisir les paramètres** : Prix spot, strike, échéance, etc.
2. **Choisir le modèle** : Black-Scholes et/ou Monte Carlo
3. **Visualiser les résultats** : Prix, grecques, intervalles de confiance
4. **Analyser les trajectoires** simulées

### Métriques de Risque
```
http://localhost:5000/indices-actions
```
1. **Sélectionner un symbole**
2. **Choisir la période** d'analyse
3. **Consulter les métriques** : VaR, CVaR, volatilité, etc.

### Smile de Volatilité
```
http://localhost:5000/volatility-surface
```
1. **Sélectionner un symbole**
2. **Choisir la maturité** en jours
3. **Visualiser le smile** de volatilité

## 🔧 APIs Disponibles

### Données de Marché
- `GET /api/market-data` - Données générales (indices + actions)
- `GET /api/indices` - Données des indices uniquement
- `GET /api/stocks` - Données des actions uniquement
- `GET /api/chart-data/<symbol>` - Données de graphique
- `GET /api/chart-data-v2/<symbol>` - Données de graphique avec timeframe

### Options et Volatilité
- `GET /api/vol-surface/<symbol>` - Surface de volatilité 2D
- `GET /api/vol-surface-3d/<symbol>` - Surface de volatilité 3D
- `GET /api/vol-surface-3d-export/<symbol>` - Export des données 3D
- `GET /api/volatility-smile/<symbol>` - Smile de volatilité
- `GET /api/available-symbols` - Symboles disponibles

### Calculs Financiers
- `POST /api/calculate-option` - Calculs d'options Call & Put
- `GET /api/risk-metrics/<symbol>` - Métriques de risque

## 🚀 Performance

- **Temps de réponse** : < 3 secondes pour les données de base
- **Surface 3D** : 10-15 secondes de chargement initial
- **Calculs d'options** : < 2 secondes pour Black-Scholes, 5-10 secondes pour Monte Carlo
- **Optimisations** : Limitation intelligente des maturités, cache des données
- **Monitoring** : Indicateurs de statut API en temps réel

## 🔧 Développement

Pour ajouter de nouvelles fonctionnalités :

1. **Ajouter une route** dans `app.py`
2. **Créer un template** dans `templates/`
3. **Mettre à jour la navigation** dans les templates
4. **Ajouter des données** dans les modules API appropriés
5. **Ajouter des tests** dans le dossier `tests/`
6. **Documenter** dans le dossier `docs/`

## 🧪 Tests

Le projet inclut un système de tests complet dans le dossier `tests/` :

### Exécution des Tests
```bash
# Tous les tests
python tests/run_tests.py

# Tests rapides seulement
python tests/run_tests.py --fast

# Tests de performance seulement
python tests/run_tests.py --performance

# Tests avec couverture de code
python tests/run_tests.py --coverage
```

### Couverture des Tests
- **40 tests** couvrant toutes les fonctionnalités
- **Tests unitaires** : Pages web, APIs, calculs financiers
- **Tests de performance** : Temps de réponse et charge
- **Tests de gestion d'erreurs** : Robustesse de l'application
- **Mocking des APIs** : Tests sans dépendance externe

Pour plus de détails, consultez [tests/README.md](tests/README.md).

## 📚 Documentation

Toute la documentation détaillée se trouve dans le dossier `docs/` :

### Documentation Principale
- **README_PRINCIPAL.md** - Ce fichier (vue d'ensemble complète)

### Fonctionnalités Avancées
- **README_CALL_PUT_CALCULATIONS.md** - Calculs d'options Call & Put (Black-Scholes, Monte Carlo)
- **README_RISK_METRICS.md** - Métriques de risque (VaR, CVaR, volatilité)
- **README_VOLATILITY_SMILE.md** - Smile de volatilité pour une maturité spécifique
- **README_DATA_EXPORT.md** - Export de données (JSON, CSV, Excel)

### APIs et Données
- **README_API_STATUS.md** - Statut des APIs et monitoring en temps réel
- **README_VOLATILITY_SURFACE.md** - Surface de volatilité 2D
- **README_POLYGON_INTEGRATION.md** - Intégration Polygon.io
- **README_FINNHUB_IMPLIED_VOLATILITY.md** - Volatilité implicite Finnhub

### Développement et Optimisations
- **README_PAGES_AND_ROUTES.md** - Documentation complète des pages et routes
- **README_PROGRESS_BARS.md** - Barres de progression
- **README_STRIKE_PERCENTAGE_IMPROVEMENT.md** - Améliorations des strikes
- **README_AUDIT_VOLATILITY_SURFACE.md** - Audit de la surface de volatilité
- **README_VOLATILITY_SURFACE_CLEANUP.md** - Nettoyage de la surface de volatilité
- **README_FINAL_3D_CORRECTIONS.md** - Corrections finales 3D
- **README_FINAL_GRAPH_FIX.md** - Corrections finales des graphiques
- **README_BLACK_SQUARE_REMOVAL.md** - Suppression du carré noir

## 🎯 Notes Techniques

- **Interface Flask** complète sans dépendance React
- **Structure modulaire** et extensible
- **Données financières** en temps réel via APIs multiples
- **Cache intelligent** pour optimiser les performances
- **Surface de volatilité 3D** avec Plotly.js
- **Calculs financiers** avancés (Black-Scholes, Monte Carlo)
- **Métriques de risque** complètes
- **Monitoring API** en temps réel
- **Export de données** en multiples formats
- **Pages de debug** pour le développement

## 👨‍💻 Auteur

**Mathis Le Gall** - Projet Flask Derivatives

---

*Projet original créé avec Lovable.dev*
