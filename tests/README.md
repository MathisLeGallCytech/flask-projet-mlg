# 🧪 Tests - Dashboard Dérivés Actions

## 📋 Vue d'ensemble

Ce dossier contient tous les tests pour l'application Flask **Dashboard Dérivés Actions**. Le système de tests est complet et couvre toutes les fonctionnalités de l'application.

## 🌐 Accès à l'Application

**Application déployée :** [https://flask-projet-natixis-mlg.onrender.com](https://flask-projet-natixis-mlg.onrender.com)

**Développement local :** `http://localhost:5000`

## 📁 Structure du Dossier

```
tests/
├── __init__.py              # Package Python
├── README.md                # Ce fichier (documentation principale)
├── README_TESTS.md          # Documentation détaillée des tests
├── RESUME_TESTS.md          # Résumé et métriques des tests
├── test_app.py              # Fichier principal de tests (40 tests)
├── run_tests.py             # Script d'exécution automatique
├── pytest.ini              # Configuration pytest
└── .pytest_cache/          # Cache pytest (généré automatiquement)
```

## 🚀 Exécution Rapide

### Depuis le dossier racine du projet
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

### Depuis le dossier tests
```bash
cd tests

# Tous les tests
python run_tests.py

# Tests spécifiques
python run_tests.py --unit
python run_tests.py --integration
```

## 📊 Tests Disponibles

### ✅ Tests de Pages Web (8 tests)
- Page d'accueil (`/`)
- Page CV (`/cv-mathis-le-gall`)
- Page indices et actions (`/indices-actions`)
- Page Call & Put (`/call-put`)
- Page surface de volatilité (`/volatility-surface`)
- Pages de debug (`/debug-finnhub`, `/debug-polygon`)
- Pages d'analyse (`/analyse-actions-indices`, `/description-app`)

### ✅ Tests d'APIs (15 tests)
- **Market Data** (`/api/market-data`)
- **Chart Data** (`/api/chart-data-v2/<symbol>`)
- **Calculate Option** (`/api/calculate-option`)
- **Risk Metrics** (`/api/risk-metrics/<symbol>`)
- **Volatility Surface** (`/api/vol-surface/<symbol>`)
- **Available Symbols** (`/api/available-symbols`)
- **Indices/Stocks** (`/api/indices`, `/api/stocks`)

### ✅ Tests de Calculs Financiers (8 tests)
- Options Call & Put avec différents paramètres
- Grecques (Delta, Gamma, Theta, Vega, Rho)
- Monte Carlo vs Black-Scholes
- Intervalles de confiance
- Chemins Monte Carlo
- Haute volatilité et maturités courtes

### ✅ Tests de Performance (2 tests)
- Temps de calcul < 10 secondes
- Requêtes concurrentes (5 simultanées)

### ✅ Tests de Gestion d'Erreurs (3 tests)
- JSON invalide
- Content-Type manquant
- Valeurs extrêmes

### ✅ Tests de Validation (4 tests)
- Paramètres invalides pour les APIs
- Gestion des erreurs 404
- Routes legacy

## 🎯 Classes de Test

### 1. `FlaskAppTestCase`
Tests des fonctionnalités principales de l'application :
- Pages web
- APIs REST
- Calculs financiers

### 2. `PerformanceTestCase`
Tests de performance et de charge :
- Temps de calcul
- Requêtes concurrentes
- Mesure des performances

### 3. `ErrorHandlingTestCase`
Tests de robustesse et gestion d'erreurs :
- Gestion des erreurs
- Validation des données
- Cas limites

## 🔧 Configuration

### Fichier `pytest.ini`
Configuration automatique pour pytest :
- Mode verbeux par défaut
- Gestion des marqueurs (slow, integration, unit, performance)
- Filtrage des avertissements
- Couleurs activées

### Mocking des APIs
Les tests utilisent `unittest.mock` pour simuler :
- ✅ Yahoo Finance API
- ✅ Finnhub API
- ✅ Polygon.io API

Cela permet de tester l'application sans dépendre des APIs externes.

## 📈 Métriques de Test

### Taux de Réussite : 100%
- **40 tests** exécutés avec succès
- **0 échec**
- **0 erreur**
- **Temps d'exécution** : ~8-10 secondes

### Couverture de Code
```bash
python tests/run_tests.py --coverage
```
- **Tests unitaires** : 35 tests
- **Tests d'intégration** : 3 tests
- **Tests de performance** : 2 tests
- **Couverture estimée** : >90%

## 🛠️ Commandes Utiles

### Exécution de Base
```bash
# Tous les tests
python tests/run_tests.py

# Tests rapides (exclure les tests lents)
python tests/run_tests.py --fast

# Tests unitaires seulement
python tests/run_tests.py --unit

# Tests de performance seulement
python tests/run_tests.py --performance

# Tests d'intégration seulement
python tests/run_tests.py --integration
```

### Avec Couverture
```bash
# Tests avec couverture de code
python tests/run_tests.py --coverage

# Rapport HTML généré dans tests/htmlcov/index.html
```

### Commandes Directes
```bash
cd tests

# Avec unittest
python test_app.py

# Avec pytest
python -m pytest test_app.py -v

# Tests spécifiques
python -m pytest test_app.py::FlaskAppTestCase -v
python -m pytest test_app.py::PerformanceTestCase -v
```

## 🐛 Dépannage

### Erreurs courantes

#### 1. ModuleNotFoundError
```bash
# Installer les dépendances
pip install flask pandas numpy scipy requests pytest coverage
```

#### 2. ImportError pour les modules locaux
```bash
# Vérifier que vous êtes dans le bon répertoire
ls app.py tests/test_app.py
```

#### 3. Tests qui échouent
```bash
# Vérifier les logs détaillés
cd tests
python -m pytest test_app.py -v -s
```

### Debug des tests
```bash
cd tests

# Mode debug avec pytest
python -m pytest test_app.py -v -s --pdb

# Test spécifique avec debug
python -m pytest test_app.py::FlaskAppTestCase::test_api_calculate_option_valid_data -v -s --pdb
```

## 📝 Ajout de Nouveaux Tests

### 1. Test unitaire simple
```python
def test_nouvelle_fonctionnalite(self):
    """Test de la nouvelle fonctionnalité"""
    # Arrange
    test_data = {...}
    
    # Act
    response = self.app.post('/api/nouvelle-api', 
                           data=json.dumps(test_data),
                           content_type='application/json')
    
    # Assert
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertIn('expected_field', data)
```

### 2. Test avec mock
```python
@patch('api.external_api.get_data')
def test_api_avec_mock(self, mock_get_data):
    """Test avec mock d'API externe"""
    mock_get_data.return_value = {'test': 'data'}
    
    response = self.app.get('/api/test')
    self.assertEqual(response.status_code, 200)
```

### 3. Test de performance
```python
def test_performance_nouvelle_fonction(self):
    """Test de performance"""
    start_time = time.time()
    
    # Exécuter la fonction
    result = self.app.post('/api/calcul-lourd', ...)
    
    end_time = time.time()
    self.assertLess(end_time - start_time, 5.0)  # < 5 secondes
```

## 🎯 Bonnes Pratiques

### 1. Nommage des tests
- `test_<fonctionnalité>_<scénario>` : `test_api_calculate_option_valid_data`
- `test_<fonctionnalité>_<erreur>` : `test_api_calculate_option_invalid_data`

### 2. Structure AAA
- **Arrange** : Préparer les données de test
- **Act** : Exécuter l'action à tester
- **Assert** : Vérifier les résultats

### 3. Isolation
- Chaque test doit être indépendant
- Utiliser `setUp()` et `tearDown()` pour la configuration
- Nettoyer les données après chaque test

### 4. Mocking
- Mocker les APIs externes
- Mocker les appels de base de données
- Mocker les fonctions coûteuses

## 🔄 Intégration Continue

Pour intégrer dans un pipeline CI/CD :

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python tests/run_tests.py
```

## 📚 Documentation Complète

- **[README_TESTS.md](README_TESTS.md)** - Documentation détaillée des tests
- **[RESUME_TESTS.md](RESUME_TESTS.md)** - Résumé et métriques des tests

## 📞 Support

En cas de problème avec les tests :
1. Vérifier que toutes les dépendances sont installées
2. Vérifier que vous êtes dans le bon répertoire
3. Exécuter avec `-v` pour plus de détails
4. Consulter les logs d'erreur spécifiques

---

**Auteur** : Mathis Le Gall  
**Date** : 2024  
**Version** : 1.0  
**Statut** : ✅ Terminé et Validé

