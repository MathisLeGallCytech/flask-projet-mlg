#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration des APIs
"""

import os
import sys
from dotenv import load_dotenv

def test_environment_variables():
    """Teste la configuration des variables d'environnement"""
    print("🔍 Test des variables d'environnement...")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier FINNHUB_API_KEY
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    if finnhub_key:
        print("✅ FINNHUB_API_KEY configurée")
        print(f"   Clé: {finnhub_key[:10]}...{finnhub_key[-4:]}")
    else:
        print("❌ FINNHUB_API_KEY non configurée")
    
    # Vérifier POLYGON_API_KEY
    polygon_key = os.getenv("POLYGON_API_KEY")
    if polygon_key:
        print("✅ POLYGON_API_KEY configurée")
        print(f"   Clé: {polygon_key[:10]}...{polygon_key[-4:]}")
    else:
        print("⚠️  POLYGON_API_KEY non configurée (optionnel)")
    
    # Vérifier FLASK_ENV
    flask_env = os.getenv("FLASK_ENV", "development")
    print(f"✅ FLASK_ENV: {flask_env}")
    
    # Vérifier FLASK_DEBUG
    flask_debug = os.getenv("FLASK_DEBUG", "True")
    print(f"✅ FLASK_DEBUG: {flask_debug}")
    
    return finnhub_key is not None

def test_finnhub_api():
    """Teste la connexion à l'API Finnhub"""
    print("\n🔍 Test de l'API Finnhub...")
    
    try:
        from api.finnhub_implied_volatility import test_finnhub_connection
        if test_finnhub_connection():
            print("✅ Connexion à l'API Finnhub réussie")
            return True
        else:
            print("❌ Échec de la connexion à l'API Finnhub")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de l'API Finnhub: {e}")
        return False

def test_polygon_api():
    """Teste la connexion à l'API Polygon.io"""
    print("\n🔍 Test de l'API Polygon.io...")
    
    try:
        from api.polygon_options_api import test_polygon_connection
        if test_polygon_connection():
            print("✅ Connexion à l'API Polygon.io réussie")
            return True
        else:
            print("❌ Échec de la connexion à l'API Polygon.io")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de l'API Polygon.io: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de configuration des APIs")
    print("=" * 50)
    
    # Test des variables d'environnement
    env_ok = test_environment_variables()
    
    # Test de l'API Finnhub
    finnhub_ok = test_finnhub_api()
    
    # Test de l'API Polygon.io
    polygon_ok = test_polygon_api()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    if env_ok:
        print("✅ Variables d'environnement: OK")
    else:
        print("❌ Variables d'environnement: PROBLÈME")
    
    if finnhub_ok:
        print("✅ API Finnhub: OK")
    else:
        print("❌ API Finnhub: PROBLÈME")
    
    if polygon_ok:
        print("✅ API Polygon.io: OK")
    else:
        print("⚠️  API Polygon.io: OPTIONNEL")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    
    if not env_ok:
        print("   - Configurez FINNHUB_API_KEY dans vos variables d'environnement")
        print("   - Créez un fichier .env avec vos clés API")
    
    if not finnhub_ok:
        print("   - Vérifiez votre clé API Finnhub")
        print("   - Testez la connexion internet")
    
    if env_ok and finnhub_ok:
        print("   - Configuration prête pour le déploiement !")
    
    return env_ok and finnhub_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
