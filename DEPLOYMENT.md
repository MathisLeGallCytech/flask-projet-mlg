# 🚀 Guide de Déploiement sur Render

## 📋 Prérequis

1. **Compte Render** : Créez un compte sur [render.com](https://render.com)
2. **Clés API** : Obtenez vos clés gratuites :
   - [Finnhub API](https://finnhub.io/register) - Clé gratuite
   - [Polygon.io](https://polygon.io/) - Clé gratuite

## 🔧 Configuration sur Render

### 1. Connecter votre repository GitHub

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre repository GitHub
4. Sélectionnez le repository `flaskProjectNatixisMathisLeGall`

### 2. Configuration du service

- **Name** : `flask-natixis-app` (ou nom de votre choix)
- **Environment** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`
- **Plan** : `Free`

### 3. Variables d'environnement

Dans la section "Environment Variables", ajoutez :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `FINNHUB_API_KEY` | `votre_clé_finnhub` | Clé API Finnhub |
| `POLYGON_API_KEY` | `votre_clé_polygon` | Clé API Polygon.io |
| `FLASK_ENV` | `production` | Environnement Flask |
| `FLASK_DEBUG` | `False` | Mode debug désactivé |

### 4. Déploiement automatique

- ✅ **Auto-Deploy** : Activé par défaut
- ✅ **Branch** : `main` ou `master`

## 🔍 Vérification du déploiement

1. **Logs de build** : Vérifiez que le build se termine sans erreur
2. **URL de l'application** : Render génère automatiquement une URL
3. **Test des fonctionnalités** : Testez les pages principales

## 🛠️ Dépannage

### Erreurs courantes

1. **Module not found** : Vérifiez `requirements.txt`
2. **API keys manquantes** : Vérifiez les variables d'environnement
3. **Timeout** : Les APIs peuvent être lentes, c'est normal

### Logs utiles

```bash
# Voir les logs en temps réel
# Dans le dashboard Render → Logs
```

## 📊 Monitoring

- **Uptime** : Surveillé automatiquement par Render
- **Logs** : Accessibles dans le dashboard
- **Métriques** : Disponibles dans la version payante

## 🔄 Mise à jour

Les mises à jour sont automatiques quand vous poussez sur votre branche principale.

## 💰 Coûts

- **Version gratuite** : 0€/mois
- **Limitations** :
  - 512 MB RAM
  - 0.1 CPU
  - 750 heures/mois
  - Pas de domaine personnalisé

## 🆘 Support

- [Documentation Render](https://render.com/docs)
- [Support Render](https://render.com/support)
