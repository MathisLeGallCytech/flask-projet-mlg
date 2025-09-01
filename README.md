# Flask Project - Mathis Le Gall

## 📚 Documentation

Toute la documentation du projet se trouve dans le dossier [`docs/`](docs/).

### 🚀 Accès Rapide

- **[Documentation Principale](docs/README_PRINCIPAL.md)** - Vue d'ensemble complète du projet
- **[Index de la Documentation](docs/INDEX.md)** - Guide de navigation dans la documentation
- **[Surface de Volatilité 3D](docs/README_3D_VOLATILITY_SURFACE.md)** - Fonctionnalité principale 3D
- **[Corrections Finales](docs/README_FINAL_GRAPH_FIX.md)** - Améliorations récentes des graphiques
- **[Nettoyage du Code](docs/README_VOLATILITY_SURFACE_CLEANUP.md)** - Optimisations et refactoring

### 🎯 Fonctionnalités Principales

- **Surface de volatilité 3D interactive** avec Plotly.js et contrôles avancés
- **APIs multi-sources** (Finnhub, Polygon.io, Yahoo Finance, Alpha Vantage)
- **Graphiques interactifs** avec Chart.js et Plotly.js optimisés
- **Monitoring des APIs** en temps réel avec indicateurs de statut
- **Interface Flask** moderne et responsive avec Tailwind CSS
- **Calculs d'options Call & Put** avec Black-Scholes et Monte Carlo
- **Métriques de risque avancées** (VaR, CVaR, volatilité, Maximum Drawdown)
- **Smile de volatilité** pour analyse des options avec données réelles
- **Export de données** en JSON, CSV et Excel avec métadonnées
- **Pages spécialisées** : CV, analyse des grecques, comparaison de performances
- **Système de cache** pour optimiser les performances
- **Gestion mémoire** avancée avec monitoring et nettoyage automatique

### 🆕 Améliorations Récentes

#### Corrections des Graphiques (Décembre 2024)
- **Graphiques responsifs** : Adaptation optimale à toutes les tailles d'écran
- **Légendes améliorées** : Informations détaillées sur les axes et données
- **Palette de couleurs cohérente** : Thème sombre uniforme
- **Contrôles interactifs** : Zoom, rotation et navigation fluides
- **Export intégré** : Capture PNG haute résolution
- **Performance optimisée** : Chargement rapide des graphiques 3D

#### Nettoyage et Optimisation du Code
- **Refactoring complet** : Séparation des responsabilités
- **Cache intelligent** : Système de cache TTL pour les données
- **Gestion d'erreurs robuste** : Try-catch et fallbacks
- **Documentation améliorée** : Docstrings et commentaires
- **Standards PEP 8** : Code formaté et lisible
- **Monitoring mémoire** : Surveillance et nettoyage automatique

### 🛠️ Installation Rapide

```bash
# Cloner le projet
git clone [URL_DU_REPO]
cd flaskProjectMathisLeGall

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configuration des APIs (optionnel)
# Créer un fichier .env avec vos clés API :
# FINNHUB_API_KEY=votre_clé_finnhub
# POLYGON_API_KEY=votre_clé_polygon

# Lancer l'application
python app.py
```

### 🧪 Tests

```bash
# Exécuter tous les tests
python tests/run_tests.py

# Tests rapides seulement
python tests/run_tests.py --fast

# Tests avec couverture de code
python tests/run_tests.py --coverage

# Tests de performance
python tests/run_tests.py --performance
```

### 🌐 Accès à l'Application

**Application déployée :** [https://flask-projet-mlg.onrender.com](https://flask-projet-mlg.onrender.com)

**Développement local :** Ouvrez votre navigateur et allez sur : `http://localhost:5000`

**Monitoring :** `http://localhost:5000/health` - État de l'application et utilisation mémoire

### 📊 Fonctionnalités Avancées

#### Surface de Volatilité 3D
- **Visualisation interactive** avec contrôles Surface/Wireframe/Contour
- **Échelles de couleurs** personnalisables (Viridis, Plasma, Inferno)
- **Indicateur de prix spot** en temps réel
- **Statistiques avancées** : Min, Max, Moyenne, Écart-type
- **Performance optimisée** avec limitation intelligente des maturités
- **Export de données** en multiples formats

#### Calculs d'Options
- **Modèle Black-Scholes** avec tous les grecques (Delta, Gamma, Theta, Vega, Rho)
- **Simulation Monte Carlo** avec intervalles de confiance
- **Trajectoires simulées** pour visualisation
- **Comparaison des modèles** en temps réel
- **Validation croisée** des résultats

#### Métriques de Risque
- **Value at Risk (VaR)** historique et paramétrique
- **Conditional VaR (CVaR)** pour les queues de distribution
- **Volatilité** historique et annualisée
- **Rendements** journaliers et cumulés
- **Skewness et Kurtosis** pour l'analyse de distribution
- **Maximum Drawdown** pour l'évaluation des pertes

### 🔧 Configuration Avancée

#### Variables d'Environnement
```bash
# APIs requises
FINNHUB_API_KEY=votre_clé_finnhub

# APIs optionnelles
POLYGON_API_KEY=votre_clé_polygon
ALPHA_VANTAGE_API_KEY=votre_clé_alpha_vantage

# Configuration de l'application
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Configuration Gunicorn (Production)
```bash
# Lancer avec Gunicorn
gunicorn -c gunicorn.conf.py app:app

# Configuration dans gunicorn.conf.py
workers = 4
bind = "0.0.0.0:5000"
timeout = 120
max_requests = 1000
max_requests_jitter = 100
```

### 📖 Documentation Complète

Consultez le dossier [`docs/`](docs/) pour une documentation détaillée de toutes les fonctionnalités, APIs, et aspects techniques du projet.

#### Documentation par Thème
- **[APIs et Données](docs/README_API_STATUS.md)** - Monitoring et gestion des APIs
- **[Calculs Financiers](docs/README_CALL_PUT_CALCULATIONS.md)** - Modèles de pricing
- **[Métriques de Risque](docs/README_RISK_METRICS.md)** - Analyses de risque
- **[Visualisations](docs/README_VOLATILITY_SURFACE.md)** - Graphiques et surfaces
- **[Tests et Qualité](docs/README_TESTS_ORGANIZATION.md)** - Organisation des tests
- **[Performance](docs/README_PROGRESS_BAR.md)** - Optimisations et monitoring

---

**Développé par Mathis Le Gall**  
**Dernière mise à jour : Décembre 2024**
