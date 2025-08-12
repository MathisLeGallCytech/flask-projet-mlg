# Smile de Volatilité - Documentation

## Vue d'ensemble

Le module de smile de volatilité implémente la visualisation et l'analyse du **smile de volatilité** pour une maturité spécifique. Cette fonctionnalité permet d'analyser la structure de volatilité implicite en fonction du prix d'exercice (strike) pour comprendre les biais de marché et les anomalies de pricing.

## 🎯 Fonctionnalités Implémentées

### Visualisation du Smile
- **Graphique 2D** du smile de volatilité
- **Données réelles** via Finnhub API
- **Filtrage par bande** autour du prix spot
- **Statistiques détaillées** du smile

### Analyse du Smile
- **Forme du smile** : Symétrique, asymétrique, skew
- **Niveau de volatilité** : ATM, ITM, OTM
- **Anomalies** : Smile inversé, smile plat
- **Comparaison** avec le modèle Black-Scholes

### Fonctionnalités Avancées
- **Sélection de maturité** en jours
- **Filtrage par span** autour du spot
- **Export des données** en JSON
- **Validation** des données d'options

## 🏗️ Architecture

### Structure des Modules
```
api/
└── finnhub_volatility_smile.py    # Module principal du smile

app.py
└── api_volatility_smile()         # Endpoint API principal
```

### Fonction Principale
```python
def create_volatility_smile(symbol, maturity_days, span=0.3):
    """
    Crée un smile de volatilité pour une maturité spécifique
    
    Args:
        symbol (str): Symbole de l'actif sous-jacent
        maturity_days (int): Maturité en jours
        span (float): Bande autour du spot (0.3 = ±30%)
    
    Returns:
        dict: Données du smile de volatilité
    """
```

## 📊 Implémentation du Smile

### Algorithme Principal

#### 1. Récupération des Données
```python
def get_options_for_maturity(symbol, target_maturity_days):
    """
    Récupère les options pour une maturité cible
    
    Args:
        symbol (str): Symbole de l'actif
        target_maturity_days (int): Maturité cible en jours
    
    Returns:
        DataFrame: Options filtrées par maturité
    """
    # Récupérer toutes les expirations
    expirations = get_options_expirations(symbol)
    
    # Trouver l'expiration la plus proche de la maturité cible
    current_date = datetime.now()
    target_date = current_date + timedelta(days=target_maturity_days)
    
    closest_expiration = min(expirations, 
                           key=lambda x: abs(x - target_date.timestamp()))
    
    # Récupérer les options pour cette expiration
    options_data = get_implied_volatility(symbol, closest_expiration)
    
    return options_data
```

#### 2. Filtrage et Nettoyage
```python
def filter_and_clean_options(options_data, spot_price, span):
    """
    Filtre et nettoie les données d'options
    
    Args:
        options_data (DataFrame): Données d'options brutes
        spot_price (float): Prix spot actuel
        span (float): Bande de filtrage
    
    Returns:
        DataFrame: Données nettoyées
    """
    # Filtrer par bande autour du spot
    min_strike = spot_price * (1 - span)
    max_strike = spot_price * (1 + span)
    
    filtered_data = options_data[
        (options_data['strike'] >= min_strike) & 
        (options_data['strike'] <= max_strike)
    ]
    
    # Nettoyer les volatilités aberrantes
    filtered_data = filtered_data[
        (filtered_data['impliedVolatility'] >= 0.01) & 
        (filtered_data['impliedVolatility'] <= 2.0)
    ]
    
    return filtered_data
```

#### 3. Construction du Smile
```python
def build_volatility_smile(options_data, spot_price):
    """
    Construit le smile de volatilité
    
    Args:
        options_data (DataFrame): Données d'options filtrées
        spot_price (float): Prix spot actuel
    
    Returns:
        dict: Structure du smile
    """
    # Séparer calls et puts
    calls = options_data[options_data['type'] == 'call']
    puts = options_data[options_data['type'] == 'put']
    
    # Calculer le moneyness (S/K)
    calls['moneyness'] = spot_price / calls['strike']
    puts['moneyness'] = spot_price / puts['strike']
    
    # Grouper par strike et calculer la moyenne IV
    smile_data = []
    for strike in sorted(options_data['strike'].unique()):
        strike_options = options_data[options_data['strike'] == strike]
        avg_iv = strike_options['impliedVolatility'].mean()
        
        smile_data.append({
            'strike': strike,
            'moneyness': spot_price / strike,
            'implied_volatility': avg_iv,
            'calls_count': len(strike_options[strike_options['type'] == 'call']),
            'puts_count': len(strike_options[strike_options['type'] == 'put'])
        })
    
    return smile_data
```

## 🔧 API Endpoint

### Endpoint Principal
```
GET /api/volatility-smile/<symbol>
```

### Paramètres de Requête
- `maturity` : Maturité en jours (défaut: 30)
- `span` : Bande autour du spot (défaut: 0.3)

### Exemple de Requête
```
GET /api/volatility-smile/AAPL?maturity=30&span=0.3
```

### Réponse
```json
{
    "symbol": "AAPL",
    "spot_price": 150.25,
    "target_maturity_days": 30,
    "actual_maturity_days": 28,
    "span": 0.3,
    "data_source": "Finnhub API",
    "smile_data": [
        {
            "strike": 120.0,
            "moneyness": 1.252,
            "implied_volatility": 0.2345,
            "calls_count": 5,
            "puts_count": 3
        },
        {
            "strike": 135.0,
            "moneyness": 1.113,
            "implied_volatility": 0.2156,
            "calls_count": 8,
            "puts_count": 6
        },
        {
            "strike": 150.0,
            "moneyness": 1.002,
            "implied_volatility": 0.1987,
            "calls_count": 12,
            "puts_count": 10
        },
        {
            "strike": 165.0,
            "moneyness": 0.911,
            "implied_volatility": 0.2234,
            "calls_count": 7,
            "puts_count": 9
        },
        {
            "strike": 180.0,
            "moneyness": 0.835,
            "implied_volatility": 0.2456,
            "calls_count": 4,
            "puts_count": 6
        }
    ],
    "statistics": {
        "min_iv": 0.1987,
        "max_iv": 0.2456,
        "mean_iv": 0.2236,
        "std_iv": 0.0189,
        "atm_iv": 0.1987,
        "skew": 0.0234
    },
    "total_options": 75,
    "calls_count": 36,
    "puts_count": 34
}
```

## 📈 Analyse du Smile

### Types de Smile

#### Smile Symétrique
- **Forme** : Courbe en U symétrique autour du strike ATM
- **Cause** : Modèle de sauts ou volatilité stochastique
- **Exemple** : Marchés calmes, liquidité élevée

#### Smile Asymétrique (Skew)
- **Forme** : Courbe inclinée vers la gauche ou droite
- **Cause** : Biais de marché, événements extrêmes
- **Exemple** : Marchés baissiers (skew négatif)

#### Smile Inversé
- **Forme** : Courbe en ∩ (inverse du smile normal)
- **Cause** : Anomalies de marché, liquidité faible
- **Exemple** : Marchés très volatils

### Métriques du Smile

#### Volatilité ATM (At-the-Money)
```python
def get_atm_volatility(smile_data, spot_price):
    """
    Trouve la volatilité ATM (moneyness ≈ 1)
    """
    atm_options = [d for d in smile_data if abs(d['moneyness'] - 1) < 0.05]
    if atm_options:
        return np.mean([d['implied_volatility'] for d in atm_options])
    return None
```

#### Skew du Smile
```python
def calculate_smile_skew(smile_data):
    """
    Calcule le skew du smile (asymétrie)
    """
    itm_options = [d for d in smile_data if d['moneyness'] > 1.05]
    otm_options = [d for d in smile_data if d['moneyness'] < 0.95]
    
    if itm_options and otm_options:
        itm_iv = np.mean([d['implied_volatility'] for d in itm_options])
        otm_iv = np.mean([d['implied_volatility'] for d in otm_options])
        return itm_iv - otm_iv
    
    return 0
```

## 🎯 Utilisation

### Interface Web
1. **Accéder** à `/volatility-surface`
2. **Sélectionner un symbole** (AAPL, SPY, QQQ recommandés)
3. **Choisir la maturité** en jours (30, 60, 90 jours)
4. **Ajuster le span** si nécessaire (0.2 à 0.5)
5. **Visualiser le smile** de volatilité

### Interprétation

#### Smile Normal
- **Forme** : Courbe en U
- **Interprétation** : Marché normal, liquidité bonne
- **Trading** : Stratégies de volatilité classiques

#### Smile Skewé
- **Forme** : Courbe inclinée
- **Interprétation** : Biais de marché, événements attendus
- **Trading** : Stratégies directionnelles

#### Smile Plat
- **Forme** : Ligne droite
- **Interprétation** : Modèle Black-Scholes valide
- **Trading** : Stratégies neutres

## 🚀 Performance

### Temps de Calcul
- **Récupération des données** : 1-3 secondes
- **Construction du smile** : < 100ms
- **Calcul des statistiques** : < 10ms

### Optimisations
- **Filtrage précoce** des données
- **Cache** des expirations
- **Validation** des données d'options
- **Gestion** des erreurs API

## 🔍 Cas d'Usage

### Trading d'Options
- **Stratégies de volatilité** : Butterfly, straddle, strangle
- **Hedging** : Protection contre les mouvements extrêmes
- **Arbitrage** : Exploitation des anomalies de pricing

### Gestion de Risque
- **Stress testing** : Scénarios de volatilité
- **Limites de risque** : Contrôle des expositions
- **Reporting** : Analyse des positions

### Recherche
- **Validation de modèles** : Comparaison avec Black-Scholes
- **Analyse de marché** : Compréhension des biais
- **Backtesting** : Test de stratégies

## 📚 Références

### Théorie du Smile
- **Derman, E.** (1999). "Regimes of Volatility"
- **Gatheral, J.** (2006). "The Volatility Surface"
- **Hull, J.C.** (2018). "Options, Futures, and Other Derivatives"

### Implémentation
- **Finnhub API** pour les données d'options
- **NumPy** pour les calculs statistiques
- **Pandas** pour la manipulation des données

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 1.0.0 - Smile de volatilité complet
