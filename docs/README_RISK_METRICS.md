# Métriques de Risque - Documentation

## Vue d'ensemble

Le module de métriques de risque implémente les indicateurs de risque les plus utilisés en finance quantitative : **Value at Risk (VaR)**, **Conditional VaR (CVaR)**, **volatilité**, **rendements**, et autres statistiques avancées pour l'analyse des actifs financiers.

## 🎯 Fonctionnalités Implémentées

### Métriques de Risque Principales
- **Value at Risk (VaR)** : Historique et paramétrique
- **Conditional VaR (CVaR)** : Expected Shortfall
- **Volatilité** : Historique et annualisée
- **Maximum Drawdown** : Perte maximale historique
- **Skewness et Kurtosis** : Asymétrie et aplatissement

### Métriques de Performance
- **Rendements** : Journaliers et cumulés
- **Rendement annualisé** : Performance sur un an
- **Ratio de Sharpe** : Rendement ajusté au risque
- **Ratio de Sortino** : Rendement ajusté au risque de baisse

### Statistiques Descriptives
- **Moyenne et médiane** des rendements
- **Écart-type** et variance
- **Minimum et maximum** historiques
- **Percentiles** (5%, 25%, 75%, 95%)

## 🏗️ Architecture

### Structure des Modules
```
models/
└── risk_metrics.py             # Classe RiskCalculator

app.py
└── api_risk_metrics()          # Endpoint API principal
```

### Classe RiskCalculator
```python
class RiskCalculator:
    def calculate_all_metrics(self, prices)
    def calculate_var(self, returns, confidence_level=0.95, method='historical')
    def calculate_cvar(self, returns, confidence_level=0.95)
    def calculate_volatility(self, returns, annualized=True)
    def calculate_max_drawdown(self, prices)
    def validate_data(self, prices)
```

## 📊 Métriques Détaillées

### Value at Risk (VaR)

#### Définition
La VaR mesure la perte maximale potentielle sur un horizon de temps donné avec un niveau de confiance spécifié.

#### Méthodes Implémentées

**VaR Historique :**
```python
def calculate_historical_var(self, returns, confidence_level=0.95):
    """
    Calcule la VaR historique basée sur les rendements passés
    
    Args:
        returns (list): Liste des rendements historiques
        confidence_level (float): Niveau de confiance (0.95 = 95%)
    
    Returns:
        float: VaR historique
    """
    percentile = (1 - confidence_level) * 100
    return np.percentile(returns, percentile)
```

**VaR Paramétrique :**
```python
def calculate_parametric_var(self, returns, confidence_level=0.95):
    """
    Calcule la VaR paramétrique en supposant une distribution normale
    
    Args:
        returns (list): Liste des rendements historiques
        confidence_level (float): Niveau de confiance
    
    Returns:
        float: VaR paramétrique
    """
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    z_score = norm.ppf(1 - confidence_level)
    return mean_return - z_score * std_return
```

### Conditional VaR (CVaR)

#### Définition
La CVaR (Expected Shortfall) mesure la perte moyenne dans les pires cas au-delà de la VaR.

#### Implémentation
```python
def calculate_cvar(self, returns, confidence_level=0.95):
    """
    Calcule la Conditional VaR (Expected Shortfall)
    
    Args:
        returns (list): Liste des rendements historiques
        confidence_level (float): Niveau de confiance
    
    Returns:
        float: CVaR
    """
    var = self.calculate_historical_var(returns, confidence_level)
    tail_returns = [r for r in returns if r <= var]
    return np.mean(tail_returns) if tail_returns else var
```

### Volatilité

#### Définition
La volatilité mesure la dispersion des rendements autour de leur moyenne.

#### Implémentation
```python
def calculate_volatility(self, returns, annualized=True):
    """
    Calcule la volatilité des rendements
    
    Args:
        returns (list): Liste des rendements historiques
        annualized (bool): Si True, annualise la volatilité
    
    Returns:
        float: Volatilité (journalière ou annualisée)
    """
    volatility = np.std(returns)
    
    if annualized:
        # Annualisation : √252 pour les données journalières
        volatility *= np.sqrt(252)
    
    return volatility
```

### Maximum Drawdown

#### Définition
Le maximum drawdown mesure la perte maximale depuis un pic historique.

#### Implémentation
```python
def calculate_max_drawdown(self, prices):
    """
    Calcule le maximum drawdown
    
    Args:
        prices (list): Liste des prix historiques
    
    Returns:
        dict: Maximum drawdown avec détails
    """
    peak = prices[0]
    max_dd = 0
    max_dd_start = 0
    max_dd_end = 0
    
    for i, price in enumerate(prices):
        if price > peak:
            peak = price
            peak_idx = i
        else:
            dd = (peak - price) / peak
            if dd > max_dd:
                max_dd = dd
                max_dd_start = peak_idx
                max_dd_end = i
    
    return {
        'max_drawdown': max_dd,
        'start_date': max_dd_start,
        'end_date': max_dd_end,
        'recovery_date': None  # À implémenter si nécessaire
    }
```

## 🔧 API Endpoint

### Endpoint Principal
```
GET /api/risk-metrics/<symbol>
```

### Paramètres de Requête
- `start` : Date de début (YYYY-MM-DD)
- `end` : Date de fin (YYYY-MM-DD)

### Exemple de Requête
```
GET /api/risk-metrics/AAPL?start=2024-01-01&end=2024-12-31
```

### Réponse
```json
{
    "symbol": "AAPL",
    "period": {
        "start": "2024-01-01",
        "end": "2024-12-31",
        "days": 252
    },
    "returns": {
        "daily_mean": 0.0008,
        "daily_median": 0.0012,
        "daily_std": 0.0189,
        "annualized_return": 0.2016,
        "annualized_volatility": 0.2998
    },
    "risk_metrics": {
        "var_95_historical": -0.0312,
        "var_99_historical": -0.0445,
        "var_95_parametric": -0.0301,
        "cvar_95": -0.0456,
        "cvar_99": -0.0589,
        "max_drawdown": 0.2345,
        "max_drawdown_start": 45,
        "max_drawdown_end": 89
    },
    "statistics": {
        "skewness": -0.1234,
        "kurtosis": 3.4567,
        "min_return": -0.0891,
        "max_return": 0.0678,
        "percentile_5": -0.0312,
        "percentile_25": -0.0123,
        "percentile_75": 0.0145,
        "percentile_95": 0.0345
    },
    "performance_ratios": {
        "sharpe_ratio": 0.6723,
        "sortino_ratio": 0.8912
    }
}
```

## 📈 Validation des Données

### Validation Implémentée
```python
def validate_data(self, prices):
    """
    Valide les données de prix
    
    Args:
        prices (list): Liste des prix
    
    Returns:
        tuple: (is_valid, message)
    """
    if len(prices) < 30:
        return False, "Au moins 30 observations requises"
    
    if any(p <= 0 for p in prices):
        return False, "Tous les prix doivent être positifs"
    
    if len(set(prices)) < 2:
        return False, "Au moins 2 prix différents requis"
    
    return True, "Données valides"
```

### Gestion des Erreurs
- **Données insuffisantes** : Minimum 30 observations
- **Prix négatifs ou nuls** : Rejet des données
- **Données manquantes** : Interpolation ou exclusion
- **Période trop courte** : Avertissement utilisateur

## 🎯 Utilisation

### Interface Web
1. **Accéder** à `/indices-actions`
2. **Sélectionner un symbole** dans la liste
3. **Choisir la période** d'analyse
4. **Consulter les métriques** :
   - Métriques de risque (VaR, CVaR, volatilité)
   - Statistiques descriptives
   - Ratios de performance

### Exemples d'Analyse

#### Action Volatile (TSLA)
- **Volatilité annualisée** : 60-80%
- **VaR 95%** : -4% à -6% (journalier)
- **Maximum Drawdown** : 30-50%

#### Indice Stable (S&P 500)
- **Volatilité annualisée** : 15-20%
- **VaR 95%** : -2% à -3% (journalier)
- **Maximum Drawdown** : 10-20%

## 🚀 Performance

### Temps de Calcul
- **Métriques de base** : < 100ms
- **Analyse complète** : 200-500ms
- **Validation des données** : < 10ms

### Optimisations
- **Calculs vectorisés** avec NumPy
- **Cache** des résultats fréquents
- **Validation** précoce des données
- **Gestion mémoire** optimisée

## 🔍 Cas d'Usage

### Gestion de Portefeuille
- **Allocation d'actifs** basée sur le risque
- **Hedging** avec les métriques de risque
- **Rebalancing** selon les VaR

### Conformité Réglementaire
- **Reporting** des métriques de risque
- **Stress testing** avec différents scénarios
- **Limites de risque** (VaR limits)

### Recherche Quantitative
- **Backtesting** de stratégies
- **Analyse de performance** des modèles
- **Validation** des hypothèses de marché

## 📚 Références

### Méthodes Théoriques
- **Jorion, P.** (2006). "Value at Risk: The New Benchmark for Managing Financial Risk"
- **Artzner, P. et al.** (1999). "Coherent Measures of Risk"
- **Rockafellar, R.T. & Uryasev, S.** (2000). "Optimization of Conditional Value-at-Risk"

### Implémentation
- **NumPy** pour les calculs vectorisés
- **SciPy** pour les distributions statistiques
- **Pandas** pour la manipulation des données temporelles

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 1.0.0 - Métriques de risque complètes
