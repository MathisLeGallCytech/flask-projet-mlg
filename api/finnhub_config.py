#!/usr/bin/env python3
"""
Configuration pour l'API Finnhub
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
# Obtenez votre clé gratuite sur: https://finnhub.io/register
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Vérifier que la clé API est définie
if not FINNHUB_API_KEY:
    print("⚠️  ATTENTION: FINNHUB_API_KEY n'est pas définie dans les variables d'environnement")
    print("   L'API Finnhub ne fonctionnera pas correctement")
    print("   Définissez FINNHUB_API_KEY dans vos variables d'environnement")

# URL de base de l'API
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# Limites de l'API (pour la version gratuite)
API_RATE_LIMIT = 60  # appels par minute
API_DELAY = 1.0  # délai entre les appels en secondes
