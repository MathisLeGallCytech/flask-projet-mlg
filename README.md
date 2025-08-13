# Flask Project Natixis - Mathis Le Gall

## 📚 Documentation

Toute la documentation du projet se trouve dans le dossier [`docs/`](docs/).

### 🚀 Accès Rapide

- **[Documentation Principale](docs/README_PRINCIPAL.md)** - Vue d'ensemble complète du projet
- **[Index de la Documentation](docs/INDEX.md)** - Guide de navigation dans la documentation
- **[Surface de Volatilité 3D](docs/README_3D_VOLATILITY_SURFACE.md)** - Fonctionnalité principale 3D

### 🎯 Fonctionnalités Principales

- **Surface de volatilité 3D interactive** avec Plotly.js
- **APIs multi-sources** (Finnhub, Polygon.io, Yahoo Finance, Alpha Vantage)
- **Graphiques interactifs** avec Chart.js et Plotly.js
- **Monitoring des APIs** en temps réel
- **Interface Flask** moderne et responsive
- **Calculs d'options Call & Put** avec Black-Scholes et Monte Carlo
- **Métriques de risque avancées** (VaR, CVaR, volatilité)
- **Smile de volatilité** pour analyse des options
- **Export de données** en JSON, CSV et Excel
- **Pages spécialisées** : CV, analyse des grecques, comparaison de performances

### 🛠️ Installation Rapide

```bash
# Cloner le projet
git clone [URL_DU_REPO]
cd flaskProjectNatixisMathisLeGall

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

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
```

### 🌐 Accès à l'Application

**Application déployée :** [https://flask-projet-natixis-mlg.onrender.com](https://flask-projet-natixis-mlg.onrender.com)

**Développement local :** Ouvrez votre navigateur et allez sur : `http://localhost:5000`

### 📖 Documentation Complète

Consultez le dossier [`docs/`](docs/) pour une documentation détaillée de toutes les fonctionnalités, APIs, et aspects techniques du projet.

---

**Développé par Mathis Le Gall** - Projet Natixis
