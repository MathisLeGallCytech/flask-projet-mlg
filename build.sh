#!/usr/bin/env bash
# Script de build pour Render

echo "🚀 Démarrage du build sur Render..."

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Vérifier que les variables d'environnement sont définies
echo "🔧 Vérification des variables d'environnement..."
if [ -z "$FINNHUB_API_KEY" ]; then
    echo "⚠️  FINNHUB_API_KEY n'est pas définie"
else
    echo "✅ FINNHUB_API_KEY est configurée"
fi

if [ -z "$POLYGON_API_KEY" ]; then
    echo "⚠️  POLYGON_API_KEY n'est pas définie"
else
    echo "✅ POLYGON_API_KEY est configurée"
fi

echo "✅ Build terminé avec succès !"
