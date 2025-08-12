#!/usr/bin/env python3
"""
Configuration pour l'API Finnhub
"""

# Remplacez par votre clé API Finnhub
# Obtenez votre clé gratuite sur: https://finnhub.io/register
FINNHUB_API_KEY = "d2cdsh9r01qihtcraq80d2cdsh9r01qihtcraq8g"

# URL de base de l'API
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# Limites de l'API (pour la version gratuite)
API_RATE_LIMIT = 60  # appels par minute
API_DELAY = 1.0  # délai entre les appels en secondes
