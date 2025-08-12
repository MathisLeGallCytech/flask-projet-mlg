# Guide de Déploiement sur Render

## Configuration des Variables d'Environnement

### Variables Requises

Pour que l'application fonctionne correctement sur Render, vous devez configurer les variables d'environnement suivantes :

#### 1. FINNHUB_API_KEY
- **Description** : Clé API pour accéder aux données Finnhub
- **Obtention** : Inscrivez-vous gratuitement sur [https://finnhub.io/register](https://finnhub.io/register)
- **Utilisation** : Données d'options et de volatilité implicite

#### 2. POLYGON_API_KEY (Optionnel)
- **Description** : Clé API pour accéder aux données Polygon.io
- **Obtention** : Inscrivez-vous sur [https://polygon.io/](https://polygon.io/)
- **Utilisation** : Données d'options alternatives

### Configuration sur Render

1. **Accédez à votre dashboard Render**
2. **Sélectionnez votre service** `flask-natixis-app`
3. **Allez dans l'onglet "Environment"**
4. **Ajoutez les variables suivantes** :

```
FINNHUB_API_KEY=votre_clé_finnhub_ici
POLYGON_API_KEY=votre_clé_polygon_ici
FLASK_ENV=production
FLASK_DEBUG=false
```

### Vérification de la Configuration

Après avoir configuré les variables d'environnement :

1. **Redéployez votre application** sur Render
2. **Vérifiez les logs** pour vous assurer qu'il n'y a pas d'erreurs
3. **Testez l'endpoint** `/api/vol-surface-3d/SPY` pour vérifier que l'API fonctionne

### Résolution des Problèmes

#### Erreur HTTP 502
- **Cause** : Variables d'environnement manquantes ou clés API invalides
- **Solution** : Vérifiez que `FINNHUB_API_KEY` est correctement configurée

#### Timeout des Requêtes
- **Cause** : Limites de rate limiting des APIs
- **Solution** : Attendez quelques secondes et réessayez

#### Erreur "Clé API non configurée"
- **Cause** : Variable `FINNHUB_API_KEY` manquante
- **Solution** : Configurez la variable dans l'interface Render

### Limites des APIs Gratuites

#### Finnhub (Gratuit)
- 60 appels par minute
- Données en temps réel limitées
- Historique limité

#### Polygon.io (Gratuit)
- 5 appels par minute
- Données en temps réel limitées
- Historique limité

### Recommandations

1. **Utilisez Finnhub** comme provider principal (plus généreux en gratuit)
2. **Configurez les timeouts** appropriés dans le code
3. **Implémentez un cache** pour éviter les appels répétés
4. **Surveillez les logs** pour détecter les problèmes de rate limiting
