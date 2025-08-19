# 🧪 Tests de l'Application Flask - Mathis Le Gall

Ce document décrit le système de tests complet pour l'application Flask de trading et d'analyse financière.

## 📋 Vue d'ensemble

Le système de tests couvre :
- ✅ **Tests unitaires** : Fonctionnalités individuelles
- ✅ **Tests d'intégration** : Interactions entre composants
- ✅ **Tests de performance** : Temps de réponse et charge
- ✅ **Tests d'API** : Endpoints REST
- ✅ **Tests de gestion d'erreurs** : Robustesse de l'application

## 🌐 Accès à l'Application

**Application déployée :** [https://flask-projet-mlg.onrender.com](https://flask-projet-mlg.onrender.com)

**Développement local :** `http://localhost:5000`

## 🚀 Exécution des Tests

### Méthode 1 : Script automatique (Recommandé)

```bash
# Tous les tests
python run_tests.py

# Tests rapides seulement
python run_tests.py --fast

# Tests de performance seulement
python run_tests.py --performance

# Tests unitaires seulement
python run_tests.py --unit

# Tests d'intégration seulement
python run_tests.py --integration

# Tests avec couverture de code
python run_tests.py --coverage
```

### Méthode 2 : Commandes directes

```bash
# Avec unittest (méthode native)
python test_app.py

# Avec pytest (plus de fonctionnalités)
python -m pytest test_app.py -v

# Tests spécifiques
python -m pytest test_app.py::FlaskAppTestCase -v
python -m pytest test_app.py::PerformanceTestCase -v
python -m pytest test_app.py::ErrorHandlingTestCase -v
```

### Méthode 3 : Avec couverture de code

```bash
# Installer coverage
pip install coverage

# Exécuter les tests avec couverture
coverage run -m pytest test_app.py

# Générer le rapport
coverage report
coverage html  # Génère htmlcov/index.html
```

## 📊 Structure des Tests

### 1. FlaskAppTestCase
Tests des fonctionnalités principales de l'application :

#### Pages Web
- ✅ Page d'accueil (`/`)
- ✅ Page CV (`/cv-mathis-le-gall`)
- ✅ Page indices et actions (`/indices-actions`)
- ✅ Page Call & Put (`/call-put`)
- ✅ Page surface de volatilité (`/volatility-surface`)
- ✅ Pages de debug (`/debug-finnhub`, `/debug-polygon`)
- ✅ Pages d'analyse (`/analyse-actions-indices`)

#### APIs
- ✅ **Market Data** (`/api/market-data`)
  - Test avec données valides
  - Test avec erreur d'API
- ✅ **Chart Data** (`/api/chart-data-v2/<symbol>`)
  - Test avec données valides
  - Test avec erreur d'API
- ✅ **Calculate Option** (`/api/calculate-option`)
  - Test avec données valides (call/put)
  - Test avec données invalides
  - Test avec champs manquants
  - Test avec haute volatilité
  - Test avec maturité courte
  - Test avec nombre élevé de simulations
- ✅ **Risk Metrics** (`/api/risk-metrics/<symbol>`)
  - Test avec données valides
  - Test sans données
- ✅ **Volatility Surface** (`/api/vol-surface/<symbol>`)
  - Test avec paramètres invalides
- ✅ **Available Symbols** (`/api/available-symbols`)
- ✅ **Indices/Stocks** (`/api/indices`, `/api/stocks`)

#### Calculs Avancés
- ✅ **Grecques** (Delta, Gamma, Theta, Vega, Rho)
- ✅ **Intervalles de confiance**
- ✅ **Chemins Monte Carlo**
- ✅ **Comparaison Black-Scholes vs Monte Carlo**

### 2. PerformanceTestCase
Tests de performance et de charge :

- ✅ **Temps de calcul** : Vérification que les calculs d'options prennent moins de 10 secondes
- ✅ **Requêtes concurrentes** : Test avec 5 requêtes simultanées
- ✅ **Mesure des temps** : Rapport des temps de calcul Monte Carlo vs Black-Scholes

### 3. ErrorHandlingTestCase
Tests de robustesse et gestion d'erreurs :

- ✅ **JSON invalide** : Gestion des requêtes malformées
- ✅ **Content-Type manquant** : Validation des en-têtes
- ✅ **Valeurs extrêmes** : Gestion des paramètres hors limites

## 🔧 Configuration

### Fichier pytest.ini
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

### Couverture de Code
```bash
python run_tests.py --coverage
```

Cela génère :
- Rapport console avec pourcentage de couverture
- Rapport HTML dans `htmlcov/index.html`

### Performance
- ⏱️ Temps de calcul d'options < 10 secondes
- 🔄 Support de requêtes concurrentes
- 📊 Mesure des temps de réponse

## 🐛 Dépannage

### Erreurs courantes

#### 1. ModuleNotFoundError
```bash
# Installer les dépendances
pip install flask pandas numpy scipy requests
```

#### 2. ImportError pour les modules locaux
```bash
# Vérifier que vous êtes dans le bon répertoire
ls app.py test_app.py
```

#### 3. Tests qui échouent
```bash
# Vérifier les logs détaillés
python -m pytest test_app.py -v -s
```

### Debug des tests

```bash
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

## 📊 Rapports et Métriques

### Exécution complète
```bash
python run_tests.py
```

Résultat attendu :
```
🚀 Démarrage des tests de l'application Flask...
============================================================
test_home_page (__main__.FlaskAppTestCase) ... ok
test_cv_page (__main__.FlaskAppTestCase) ... ok
...
📊 Résumé des tests:
   Tests exécutés: 45
   Échecs: 0
   Erreurs: 0
   Succès: 45

✅ Tous les tests ont réussi!
```

### Couverture de code
```bash
python run_tests.py --coverage
```

Résultat attendu :
```
Name                    Stmts   Miss  Cover
-------------------------------------------
app.py                    450     45    90%
test_app.py              280      0   100%
```

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
        run: python run_tests.py
```

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
