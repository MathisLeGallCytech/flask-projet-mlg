# Extraction de Volatilité Implicite via l'API Finnhub

## Vue d'ensemble

Ce script Python permet de récupérer les **vraies données de volatilité implicite** des options via l'API Finnhub, sans aucune simulation ou génération de données. Il constitue la base des données utilisées pour les surfaces de volatilité 2D et 3D.

## 🎯 Fonctionnalités

### Données Réelles
- **Volatilité implicite authentique** : Les valeurs proviennent directement des marchés financiers
- **Données 100% réelles** : Le script utilise uniquement les données fournies par l'API Finnhub
- **Aucune simulation** : Pas de calculs locaux ni de données simulées
- **Intégration complète** : Utilisé par les surfaces de volatilité 2D et 3D

### APIs Supportées
- **Finnhub** : Source principale des données d'options
- **Polygon.io** : Source alternative pour les données avancées
- **Yahoo Finance** : Données de base et prix spot

## Important

- **Données 100% réelles** : Le script utilise uniquement les données fournies par l'API Finnhub
- **Aucune simulation** : Pas de calculs locaux ni de données simulées
- **Volatilité implicite authentique** : Les valeurs proviennent directement des marchés financiers

## Prérequis

1. **Clé API Finnhub** (gratuite)
   - Inscrivez-vous sur [https://finnhub.io/register](https://finnhub.io/register)
   - Copiez votre clé API

2. **Dépendances Python**
   ```bash
   pip install requests pandas
   ```

## Configuration

1. **Modifiez le fichier `finnhub_config.py`** :
   ```python
   FINNHUB_API_KEY = "votre_clé_api_ici"
   ```

2. **Ou modifiez directement `finnhub_implied_volatility.py`** :
   ```python
   API_KEY = "votre_clé_api_ici"
   ```

## Utilisation

### Exécution simple
```bash
python finnhub_implied_volatility.py
```

### Utilisation programmatique
```python
from finnhub_implied_volatility import get_implied_volatility, get_options_expirations

# Récupérer les dates d'expiration
expirations = get_options_expirations("AAPL")

# Récupérer la volatilité implicite
volatility_data = get_implied_volatility("AAPL", expirations[0])
```

## Structure des données

Le script retourne un DataFrame pandas avec les colonnes suivantes :

| Colonne | Type | Description |
|---------|------|-------------|
| `contractSymbol` | str | Symbole du contrat d'option |
| `type` | str | Type d'option ('call' ou 'put') |
| `strike` | float | Prix d'exercice |
| `lastPrice` | float | Dernier prix de l'option |
| `impliedVolatility` | float | Volatilité implicite (format décimal) |

## Fonctionnalités

### 1. Récupération des dates d'expiration
```python
expirations = get_options_expirations("AAPL")
# Retourne une liste de timestamps UNIX
```

### 2. Extraction de la volatilité implicite
```python
volatility_data = get_implied_volatility("AAPL", expiration_timestamp)
# Retourne un DataFrame avec toutes les options
```

### 3. Gestion des erreurs
- Clé API invalide
- Ticker inexistant
- Pas d'options disponibles
- Erreurs de réseau

## Exemple de sortie

```
Extraction de volatilité implicite via l'API Finnhub
============================================================
Connexion API réussie - Prix AAPL: $150.25
Récupération des dates d'expiration pour AAPL...
12 dates d'expiration trouvées

Ticker: AAPL
Date d'expiration utilisée: 2024-01-19
--------------------------------------------------
Récupération des options pour AAPL - expiration: 1704067200
Date d'expiration: 2024-01-19
156 options récupérées avec succès
  - Calls: 78
  - Puts: 78
```

## Fonctions Principales

### `get_options_expirations(symbol)`
Récupère toutes les dates d'expiration disponibles pour un symbole donné.

**Paramètres :**
- `symbol` (str) : Symbole de l'action (ex: "AAPL")

**Retourne :**
- Liste de timestamps UNIX des dates d'expiration

### `get_implied_volatility(symbol, expiration)`
Récupère toutes les options et leur volatilité implicite pour une date d'expiration.

**Paramètres :**
- `symbol` (str) : Symbole de l'action
- `expiration` (int) : Timestamp UNIX de la date d'expiration

**Retourne :**
- DataFrame pandas avec les données d'options

## Gestion des Erreurs

### Erreurs API
- **Clé API invalide** : Vérifiez votre clé dans `finnhub_config.py`
- **Limite de requêtes** : Attendez avant de refaire une requête
- **Symbole inexistant** : Vérifiez l'orthographe du symbole

### Erreurs de Données
- **Pas d'options** : Certains symboles n'ont pas d'options disponibles
- **Données manquantes** : Certaines options peuvent avoir des IV manquantes
- **Format incorrect** : Vérifiez le format des données reçues

## Intégration avec Flask

### Endpoint API
```python
@app.route('/api/options/<symbol>')
def get_options_data(symbol):
    try:
        expirations = get_options_expirations(symbol)
        if not expirations:
            return jsonify({"error": "Aucune expiration trouvée"}), 404
        
        # Utiliser la première expiration disponible
        options_data = get_implied_volatility(symbol, expirations[0])
        
        return jsonify({
            "symbol": symbol,
            "expiration": expirations[0],
            "options": options_data.to_dict('records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Template HTML
```html
<script>
async function loadOptionsData(symbol) {
    try {
        const response = await fetch(`/api/options/${symbol}`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Erreur:', data.error);
            return;
        }
        
        // Traitement des données d'options
        displayOptionsData(data.options);
    } catch (error) {
        console.error('Erreur de connexion:', error);
    }
}
</script>
```

## Performance et Optimisation

### Limites API
- **Requêtes par minute** : Limité par Finnhub
- **Temps de réponse** : 1-3 secondes par requête
- **Cache recommandé** : Mise en cache des données fréquemment utilisées

### Optimisations
- **Requêtes en lot** : Éviter les requêtes multiples
- **Cache local** : Stocker les données récentes
- **Gestion des timeouts** : Éviter les blocages

## Tests

### Test de Connexion
```python
python -c "
from finnhub_implied_volatility import get_options_expirations
expirations = get_options_expirations('AAPL')
print(f'Connexion réussie: {len(expirations)} expirations trouvées')
"
```

### Test de Données
```python
python -c "
from finnhub_implied_volatility import get_implied_volatility, get_options_expirations
expirations = get_options_expirations('AAPL')
if expirations:
    data = get_implied_volatility('AAPL', expirations[0])
    print(f'Données récupérées: {len(data)} options')
"
```

## Développement

### Ajout de Nouvelles Fonctionnalités
1. **Filtrage par strike** : Limiter les options par prix d'exercice
2. **Tri par IV** : Trier les options par volatilité implicite
3. **Export CSV** : Exporter les données en format CSV
4. **Graphiques** : Visualisation des données d'options

### Améliorations Possibles
- **Support multi-expiration** : Traitement de plusieurs dates
- **Calculs avancés** : P&L, etc.
- **Interface web** : Interface utilisateur pour la visualisation
- **Alertes** : Notifications sur les changements d'IV

## Support

### Documentation API Finnhub
- [Documentation officielle](https://finnhub.io/docs/api)
- [Endpoint Options](https://finnhub.io/docs/api/stock-options)
- [Limites de taux](https://finnhub.io/docs/api/rate-limits)

### Problèmes Courants
1. **Clé API expirée** : Régénérez votre clé API
2. **Limite de requêtes** : Attendez avant de refaire une requête
3. **Données manquantes** : Vérifiez la disponibilité des options

---

**Développé par Mathis Le Gall**  
**Date**: 10 août 2025  
**Version**: 1.0.0 - Extraction de volatilité implicite Finnhub
