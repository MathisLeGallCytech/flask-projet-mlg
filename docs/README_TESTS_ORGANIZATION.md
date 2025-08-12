# 🧪 Organisation des Tests - Dashboard Dérivés Actions

## 📋 Vue d'ensemble

Ce document décrit l'organisation et la structure des tests dans le projet **Dashboard Dérivés Actions**. Tous les tests sont organisés dans le dossier `tests/` pour une meilleure organisation et maintenance.

## 📁 Structure du Dossier Tests

```
tests/
├── __init__.py              # Package Python
├── README.md                # Documentation principale des tests
├── README_TESTS.md          # Documentation détaillée des tests
├── RESUME_TESTS.md          # Résumé et métriques des tests
├── test_app.py              # Fichier principal de tests (40 tests)
├── run_tests.py             # Script d'exécution automatique
├── pytest.ini              # Configuration pytest
└── .pytest_cache/          # Cache pytest (généré automatiquement)
```

## 🎯 Organisation des Tests

### 1. **test_app.py** - Fichier Principal de Tests
Contient 40 tests organisés en 3 classes :

#### `FlaskAppTestCase` (35 tests)
- **Tests de Pages Web** (8 tests)
  - Page d'accueil, CV, indices, call/put, volatilité, debug, analyse
- **Tests d'APIs** (15 tests)
  - Market data, chart data, calculate option, risk metrics, etc.
- **Tests de Calculs Financiers** (8 tests)
  - Options call/put, grecques, Monte Carlo, Black-Scholes
- **Tests de Validation** (4 tests)
  - Paramètres invalides, erreurs 404, routes legacy

#### `PerformanceTestCase` (2 tests)
- **Temps de calcul** < 10 secondes
- **Requêtes concurrentes** (5 simultanées)

#### `ErrorHandlingTestCase` (3 tests)
- **JSON invalide**
- **Content-Type manquant**
- **Valeurs extrêmes**

### 2. **run_tests.py** - Script d'Exécution
Interface en ligne de commande avec options :
- `--fast` : Tests rapides seulement
- `--performance` : Tests de performance
- `--unit` : Tests unitaires
- `--integration` : Tests d'intégration
- `--coverage` : Tests avec couverture de code

### 3. **pytest.ini** - Configuration
Configuration automatique pour pytest :
- Mode verbeux par défaut
- Gestion des marqueurs
- Filtrage des avertissements
- Couleurs activées

## 🚀 Exécution des Tests

### Depuis le Dossier Racine
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

### Depuis le Dossier Tests
```bash
cd tests

# Tous les tests
python run_tests.py

# Tests spécifiques
python run_tests.py --unit
python run_tests.py --integration
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

## 📊 Métriques de Test

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

### Performance
- **Temps de calcul d'options** : <10 secondes ✅
- **Requêtes concurrentes** : 5 simultanées ✅
- **Temps de réponse API** : <1 seconde ✅

## 🔧 Configuration Technique

### Import des Modules
Les tests utilisent un chemin relatif pour importer l'application :
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
```

### Mocking des APIs
Les tests utilisent `unittest.mock` pour simuler :
- ✅ **Yahoo Finance API** : Données de marché
- ✅ **Finnhub API** : Données d'options
- ✅ **Polygon.io API** : Données avancées

Cela permet de tester l'application sans dépendre des APIs externes.

### Configuration Pytest
```ini
[tool:pytest]
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    performance: marks tests as performance tests
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## 🎯 Types de Tests

### 1. Tests Unitaires
- **Objectif** : Tester des fonctionnalités individuelles
- **Exemples** : Calculs d'options, grecques, APIs
- **Isolation** : Chaque test est indépendant
- **Mocking** : APIs externes mockées

### 2. Tests d'Intégration
- **Objectif** : Tester les interactions entre composants
- **Exemples** : Flux complet d'une requête API
- **Dépendances** : Peut utiliser plusieurs modules
- **Validation** : Vérifier le comportement global

### 3. Tests de Performance
- **Objectif** : Vérifier les temps de réponse
- **Exemples** : Calculs lourds, requêtes concurrentes
- **Métriques** : Temps d'exécution, charge
- **Seuils** : Définir des limites acceptables

### 4. Tests de Gestion d'Erreurs
- **Objectif** : Vérifier la robustesse
- **Exemples** : Données invalides, erreurs API
- **Validation** : Messages d'erreur appropriés
- **Récupération** : Gestion gracieuse des erreurs

## 📝 Ajout de Nouveaux Tests

### 1. Test de Page Web
```python
def test_nouvelle_page(self):
    """Test de la nouvelle page"""
    response = self.app.get('/nouvelle-page')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'<!DOCTYPE html>', response.data)
```

### 2. Test d'API
```python
@patch('api.external_api.get_data')
def test_nouvelle_api(self, mock_get_data):
    """Test de la nouvelle API"""
    mock_get_data.return_value = {'test': 'data'}
    
    response = self.app.get('/api/nouvelle-api')
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertIn('test', data)
```

### 3. Test de Calcul
```python
def test_nouveau_calcul(self):
    """Test du nouveau calcul"""
    test_data = {
        'param1': 100,
        'param2': 0.2
    }
    
    response = self.app.post('/api/calcul',
                           data=json.dumps(test_data),
                           content_type='application/json')
    
    self.assertEqual(response.status_code, 200)
    result = json.loads(response.data)
    self.assertIn('resultat', result)
```

### 4. Test de Performance
```python
def test_performance_nouveau_calcul(self):
    """Test de performance du nouveau calcul"""
    start_time = time.time()
    
    response = self.app.post('/api/calcul-lourd', ...)
    
    end_time = time.time()
    self.assertLess(end_time - start_time, 5.0)  # < 5 secondes
    self.assertEqual(response.status_code, 200)
```

## 🎯 Bonnes Pratiques

### 1. Nommage des Tests
- `test_<fonctionnalité>_<scénario>` : `test_api_calculate_option_valid_data`
- `test_<fonctionnalité>_<erreur>` : `test_api_calculate_option_invalid_data`
- `test_<fonctionnalité>_<performance>` : `test_api_calculate_option_performance`

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

### 5. Documentation
- Documenter chaque test avec une docstring claire
- Expliquer le but et les conditions du test
- Inclure des exemples si nécessaire

## 🔄 Intégration Continue

### GitHub Actions
```yaml
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
      - name: Upload coverage
        uses: codecov/codecov-action@v1
        with:
          file: ./tests/htmlcov/coverage.xml
```

### Pré-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: run-tests
        name: Run Tests
        entry: python tests/run_tests.py --fast
        language: system
        pass_filenames: false
```

## 📊 Monitoring et Rapports

### Rapports de Couverture
```bash
python tests/run_tests.py --coverage
```
Génère :
- Rapport console avec pourcentage de couverture
- Rapport HTML dans `tests/htmlcov/index.html`

### Métriques de Performance
- Temps d'exécution des tests
- Temps de réponse des APIs
- Utilisation mémoire
- Charge CPU

### Alertes
- Tests qui échouent
- Couverture qui baisse
- Performance qui se dégrade
- Nouvelles fonctionnalités sans tests

## 🐛 Dépannage

### Erreurs Courantes

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

### Debug des Tests
```bash
cd tests

# Mode debug avec pytest
python -m pytest test_app.py -v -s --pdb

# Test spécifique avec debug
python -m pytest test_app.py::FlaskAppTestCase::test_api_calculate_option_valid_data -v -s --pdb
```

## 📚 Documentation Complète

- **[tests/README.md](../tests/README.md)** - Documentation principale des tests
- **[tests/README_TESTS.md](../tests/README_TESTS.md)** - Documentation détaillée
- **[tests/RESUME_TESTS.md](../tests/RESUME_TESTS.md)** - Résumé et métriques

## 📞 Support

En cas de problème avec les tests :
1. Vérifier que toutes les dépendances sont installées
2. Vérifier que vous êtes dans le bon répertoire
3. Exécuter avec `-v` pour plus de détails
4. Consulter les logs d'erreur spécifiques
5. Vérifier la configuration pytest

---

**Auteur** : Mathis Le Gall  
**Date** : 2024  
**Version** : 1.0  
**Statut** : ✅ Terminé et Validé

