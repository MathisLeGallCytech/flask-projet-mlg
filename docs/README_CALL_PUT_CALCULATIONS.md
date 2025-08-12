# Calculs d'Options Call & Put - Documentation

## Vue d'ensemble

Le module de calculs d'options Call & Put implémente les modèles financiers les plus utilisés pour l'évaluation des options : **Black-Scholes** et **Monte Carlo**. Il fournit des calculs précis avec tous les grecques et des intervalles de confiance.

## 🎯 Fonctionnalités Implémentées

### Modèles de Calcul
- **Black-Scholes** : Modèle analytique classique
- **Monte Carlo** : Simulation stochastique avec intervalles de confiance
- **Comparaison** : Analyse comparative des deux modèles

### Grecques Calculées
- **Delta** : Sensibilité au prix de l'actif sous-jacent
- **Gamma** : Sensibilité du delta aux variations de prix
- **Theta** : Sensibilité au temps (décroissance temporelle)
- **Vega** : Sensibilité à la volatilité
- **Rho** : Sensibilité au taux d'intérêt

### Fonctionnalités Avancées
- **Intervalles de confiance** pour Monte Carlo
- **Trajectoires simulées** pour visualisation
- **Validation des paramètres** en temps réel
- **Calculs de performance** (temps d'exécution)

## 🏗️ Architecture

### Structure des Modules
```
models/
├── options_pricing.py          # Classe principale OptionPricer
└── risk_metrics.py             # Métriques de risque associées

app.py
├── api_calculate_option()      # Endpoint API principal
└── _inv_norm_cdf()            # Fonction d'inverse CDF normale
```

### Classe OptionPricer
```python
class OptionPricer:
    def black_scholes_price_and_greeks(self, S, K, T, r, sigma, option_type)
    def monte_carlo_price_and_greeks(self, S, K, T, r, sigma, option_type, 
                                    nb_simulations, nb_steps, return_std, return_paths)
```

## 📊 Modèle Black-Scholes

### Formules Implémentées

#### Prix de l'Option
**Call :**
```
C = S * N(d1) - K * e^(-rT) * N(d2)
```

**Put :**
```
P = K * e^(-rT) * N(-d2) - S * N(-d1)
```

Où :
- `d1 = (ln(S/K) + (r + σ²/2)T) / (σ√T)`
- `d2 = d1 - σ√T`
- `N(x)` = Fonction de répartition normale standard

#### Grecques
- **Delta** : `∂C/∂S = N(d1)` (Call), `∂P/∂S = N(d1) - 1` (Put)
- **Gamma** : `∂²C/∂S² = ∂²P/∂S² = N'(d1) / (Sσ√T)`
- **Theta** : `∂C/∂T = -SσN'(d1) / (2√T) - rKe^(-rT)N(d2)`
- **Vega** : `∂C/∂σ = S√T N'(d1)`
- **Rho** : `∂C/∂r = KTe^(-rT)N(d2)` (Call), `∂P/∂r = -KTe^(-rT)N(-d2)` (Put)

### Implémentation
```python
def black_scholes_price_and_greeks(self, S, K, T, r, sigma, option_type):
    """
    Calcule le prix et les grecques selon Black-Scholes
    
    Args:
        S (float): Prix spot de l'actif sous-jacent
        K (float): Prix d'exercice (strike)
        T (float): Temps jusqu'à l'échéance (en années)
        r (float): Taux d'intérêt sans risque
        sigma (float): Volatilité
        option_type (str): 'call' ou 'put'
    
    Returns:
        tuple: (prix, delta, gamma, theta, vega, rho)
    """
```

## 🎲 Modèle Monte Carlo

### Algorithme Implémenté

#### Simulation des Trajectoires
1. **Génération de trajectoires** selon le mouvement brownien géométrique
2. **Calcul des payoffs** à l'échéance
3. **Actualisation** au taux sans risque
4. **Moyenne** pour obtenir le prix estimé

#### Formule de Simulation
```
S(t) = S(0) * exp((r - σ²/2)t + σ√t * Z)
```

Où `Z ~ N(0,1)` est une variable aléatoire normale standard.

### Implémentation
```python
def monte_carlo_price_and_greeks(self, S, K, T, r, sigma, option_type,
                                nb_simulations=10000, nb_steps=252,
                                return_std=True, return_paths=False):
    """
    Calcule le prix et les grecques par simulation Monte Carlo
    
    Args:
        S, K, T, r, sigma, option_type: Paramètres de base
        nb_simulations (int): Nombre de simulations
        nb_steps (int): Nombre de pas temporels
        return_std (bool): Retourner l'erreur standard
        return_paths (bool): Retourner les trajectoires
    
    Returns:
        dict: Résultats avec prix, grecques, intervalles de confiance
    """
```

### Intervalles de Confiance
```python
# Calcul de l'intervalle de confiance
z = _z_from_confidence(confidence_level)  # 1.96 pour 95%
lower_bound = price - z * std_error
upper_bound = price + z * std_error
```

## 🔧 API Endpoint

### Endpoint Principal
```
POST /api/calculate-option
```

### Paramètres d'Entrée
```json
{
    "spotPrice": 100.0,
    "strikePrice": 100.0,
    "timeMaturity": 1.0,
    "riskFreeRate": 0.05,
    "volatility": 0.2,
    "optionType": "call",
    "modelChoice": "both",
    "numSimulations": 10000,
    "numSteps": 252,
    "confidenceLevel": 0.95,
    "numPaths": 50
}
```

### Réponse
```json
{
    "monteCarlo": {
        "optionPrice": 10.4506,
        "delta": 0.5234,
        "gamma": 0.0198,
        "theta": -6.2341,
        "vega": 39.8765,
        "rho": 44.1234,
        "confidenceInterval": {
            "lower": 10.2345,
            "mean": 10.4506,
            "upper": 10.6667,
            "confidenceLevel": 0.95
        },
        "paths": [...],
        "timeGrid": [...],
        "timeMs": 245.67
    },
    "blackScholes": {
        "optionPrice": 10.4506,
        "delta": 0.5234,
        "gamma": 0.0198,
        "theta": -6.2341,
        "vega": 39.8765,
        "rho": 44.1234,
        "timeMs": 0.12
    },
    "parameters": {...},
    "timings": {
        "totalMs": 245.79
    }
}
```

## 📈 Validation et Tests

### Validation des Paramètres
```python
# Validation des valeurs positives
if spot_price <= 0 or strike_price <= 0 or time_maturity <= 0:
    return jsonify({'error': 'Les prix et l\'échéance doivent être positifs'}), 400

# Validation des bornes
if risk_free_rate < 0 or risk_free_rate > 1 or volatility < 0 or volatility > 1:
    return jsonify({'error': 'Le taux sans risque et la volatilité doivent être entre 0 et 1'}), 400
```

### Tests de Cohérence
- **Convergence Monte Carlo** : Vérification que Monte Carlo converge vers Black-Scholes
- **Parité Call-Put** : Validation de la relation `C - P = S - Ke^(-rT)`
- **Grecques** : Vérification des relations entre grecques
- **Bornes** : Validation des bornes théoriques des prix

## 🎯 Utilisation

### Interface Web
1. **Accéder** à `/call-put`
2. **Saisir les paramètres** :
   - Prix spot (S)
   - Prix d'exercice (K)
   - Échéance (T)
   - Taux sans risque (r)
   - Volatilité (σ)
   - Type d'option (Call/Put)
3. **Choisir le modèle** : Black-Scholes, Monte Carlo, ou les deux
4. **Visualiser les résultats** : Prix, grecques, intervalles de confiance

### Exemples de Calculs

#### Option Call At-the-Money
- **S = 100**, **K = 100**, **T = 1 an**, **r = 5%**, **σ = 20%**
- **Résultat** : Prix ≈ 10.45, Delta ≈ 0.52, Gamma ≈ 0.02

#### Option Put Out-of-the-Money
- **S = 100**, **K = 90**, **T = 0.5 an**, **r = 3%**, **σ = 25%**
- **Résultat** : Prix ≈ 2.34, Delta ≈ -0.23, Gamma ≈ 0.03

## 🚀 Performance

### Temps de Calcul Typiques
- **Black-Scholes** : < 1ms
- **Monte Carlo** (10k simulations) : 200-500ms
- **Monte Carlo** (100k simulations) : 2-5 secondes

### Optimisations Implémentées
- **Vectorisation NumPy** pour les calculs
- **Génération efficace** des nombres aléatoires
- **Calculs parallèles** pour les grecques
- **Cache** des résultats fréquents

## 🔍 Cas d'Usage

### Trading
- **Évaluation d'options** en temps réel
- **Hedging** avec les grecques
- **Gestion de portefeuille** d'options

### Recherche
- **Backtesting** de stratégies d'options
- **Analyse de sensibilité** aux paramètres
- **Validation** de modèles plus complexes

### Formation
- **Apprentissage** des modèles d'options
- **Visualisation** des concepts financiers
- **Expérimentation** avec différents paramètres

## 📚 Références

### Modèles Théoriques
- **Black, F. & Scholes, M.** (1973). "The Pricing of Options and Corporate Liabilities"
- **Hull, J.C.** (2018). "Options, Futures, and Other Derivatives"
- **Glasserman, P.** (2004). "Monte Carlo Methods in Financial Engineering"

### Implémentation
- **Approximation d'Acklam** pour l'inverse de la CDF normale
- **Génération de nombres aléatoires** avec NumPy
- **Calculs vectorisés** pour optimiser les performances

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 1.0.0 - Calculs d'options complets
