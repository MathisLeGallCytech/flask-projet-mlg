#!/usr/bin/env python3
"""
Configuration pour l'API Tradier
"""

import os

# Charger les variables d'environnement
try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv('.env.local')  # Charger aussi .env.local pour le développement
except ImportError:
    print("⚠️  Module python-dotenv non trouvé, utilisation des variables d'environnement système")
    # Les variables d'environnement système seront utilisées automatiquement

# Récupérer la clé API depuis les variables d'environnement
# Obtenez votre clé gratuite sur: https://developer.tradier.com/
TRADIER_API_KEY = os.getenv("TRADIER_API_KEY")

# Vérifier que la clé API est définie
if not TRADIER_API_KEY:
    print("❌ ERREUR: TRADIER_API_KEY n'est pas définie dans les variables d'environnement")
    print("   L'API Tradier ne fonctionnera pas correctement")
    print("   Créez un fichier .env avec: TRADIER_API_KEY=votre_clé")
    print("   Obtenez votre clé gratuite sur: https://developer.tradier.com/")
    print("   Exemple de fichier .env:")
    print("   TRADIER_API_KEY=ZmaUW8lsN09pUC7ZnBEecenKvVkc")
else:
    print(f"✅ TRADIER_API_KEY chargée depuis les variables d'environnement: {TRADIER_API_KEY[:10]}...{TRADIER_API_KEY[-4:]}")

# URL de base de l'API
TRADIER_BASE_URL = "https://api.tradier.com/v1"

# Limites de l'API (pour la version gratuite)
API_RATE_LIMIT = 120  # appels par minute
API_DELAY = 0.5  # délai entre les appels en secondes

# Configuration des headers par défaut
DEFAULT_HEADERS = {
    "Authorization": f"Bearer {TRADIER_API_KEY}" if TRADIER_API_KEY else "",
    "Accept": "application/json"
}

# Configuration pour les tests
TEST_SYMBOLS = ["AAPL", "SPY", "QQQ", "TSLA", "MSFT"]

# Configuration pour les expirations
MAX_EXPIRATIONS = 6  # Nombre maximum d'expirations à récupérer
DEFAULT_SPAN = 0.3  # Bande par défaut autour du spot (30%)

# Configuration pour les timeouts
REQUEST_TIMEOUT = 15  # Timeout des requêtes en secondes
CONNECTION_TIMEOUT = 10  # Timeout de connexion en secondes

def get_tradier_config():
    """
    Retourne la configuration Tradier complète
    
    Returns:
        dict: Configuration complète de l'API Tradier
    """
    return {
        'api_key': TRADIER_API_KEY,
        'base_url': TRADIER_BASE_URL,
        'rate_limit': API_RATE_LIMIT,
        'delay': API_DELAY,
        'headers': DEFAULT_HEADERS,
        'test_symbols': TEST_SYMBOLS,
        'max_expirations': MAX_EXPIRATIONS,
        'default_span': DEFAULT_SPAN,
        'request_timeout': REQUEST_TIMEOUT,
        'connection_timeout': CONNECTION_TIMEOUT
    }

def is_tradier_configured():
    """
    Vérifie si l'API Tradier est correctement configurée
    
    Returns:
        bool: True si configurée, False sinon
    """
    return TRADIER_API_KEY is not None and len(TRADIER_API_KEY) > 0

def get_tradier_headers():
    """
    Retourne les headers pour les requêtes Tradier
    
    Returns:
        dict: Headers pour les requêtes API
    """
    if not TRADIER_API_KEY:
        return {"Accept": "application/json"}
    
    return {
        "Authorization": f"Bearer {TRADIER_API_KEY}",
        "Accept": "application/json"
    }

if __name__ == "__main__":
    print("🔧 Configuration Tradier")
    print("=" * 40)
    print(f"API Key configurée: {'✅ Oui' if is_tradier_configured() else '❌ Non'}")
    print(f"Base URL: {TRADIER_BASE_URL}")
    print(f"Rate Limit: {API_RATE_LIMIT} appels/minute")
    print(f"Timeout: {REQUEST_TIMEOUT}s")
    
    if TRADIER_API_KEY:
        print(f"API Key: {TRADIER_API_KEY[:10]}...{TRADIER_API_KEY[-4:]}")
    else:
        print("API Key: Non configurée")
        print("\n📝 Pour configurer:")
        print("1. Créez un compte sur https://developer.tradier.com/")
        print("2. Obtenez votre clé API")
        print("3. Définissez TRADIER_API_KEY dans vos variables d'environnement")
