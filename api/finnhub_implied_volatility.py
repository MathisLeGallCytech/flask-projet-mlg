#!/usr/bin/env python3
"""
Script pour extraire la volatilité implicite des options via l'API Finnhub
Utilise uniquement des données réelles fournies par l'API
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time


# Configuration de l'API Finnhub
try:
    from .finnhub_config import FINNHUB_API_KEY, FINNHUB_BASE_URL
    API_KEY = FINNHUB_API_KEY
    BASE_URL = FINNHUB_BASE_URL
except ImportError:
    try:
        from finnhub_config import FINNHUB_API_KEY, FINNHUB_BASE_URL
        API_KEY = FINNHUB_API_KEY
        BASE_URL = FINNHUB_BASE_URL
    except ImportError:
        # Configuration par défaut si le fichier de config n'existe pas
        API_KEY = None
        BASE_URL = "https://finnhub.io/api/v1"

# Vérifier que la clé API est disponible
if not API_KEY:
    print("⚠️  ATTENTION: FINNHUB_API_KEY n'est pas configurée")
    print("   L'API Finnhub ne fonctionnera pas correctement")


def get_options_expirations(ticker: str):
    """
    Récupère les dates d'expiration disponibles pour un ticker donné
    
    Args:
        ticker (str): Le symbole du titre (ex: "AAPL")
    
    Returns:
        list: Liste des dates d'expiration (timestamps UNIX)
    """
    if not API_KEY:
        print("❌ Clé API Finnhub non configurée")
        return []
    
    url = f"{BASE_URL}/stock/option-chain"
    params = {
        'symbol': ticker,
        'token': API_KEY
    }
    
    try:
        print(f"Récupération des dates d'expiration pour {ticker}...")
        response = requests.get(url, params=params, timeout=15)  # Timeout de 15 secondes
        response.raise_for_status()
        
        data = response.json()
        
        # L'API Finnhub retourne directement un tableau d'options
        if isinstance(data, list) and len(data) > 0:
            # Extraire les dates d'expiration uniques
            expirations = set()
            for option in data:
                if 'expirationDate' in option:
                    # Convertir en timestamp UNIX
                    try:
                        exp_date = datetime.strptime(option['expirationDate'], '%Y-%m-%d')
                        exp_timestamp = int(exp_date.timestamp())
                        expirations.add(exp_timestamp)
                    except ValueError:
                        # Si c'est déjà un timestamp
                        if isinstance(option['expirationDate'], int):
                            expirations.add(option['expirationDate'])
                        else:
                            print(f"Format de date invalide: {option['expirationDate']}")
            
            expirations_list = sorted(list(expirations))
            print(f"✅ {len(expirations_list)} dates d'expiration trouvées")
            return expirations_list
        elif 'data' in data and data['data']:
            # Structure alternative avec 'data'
            expirations = set()
            for option in data['data']:
                if 'expirationDate' in option:
                    try:
                        exp_date = datetime.strptime(option['expirationDate'], '%Y-%m-%d')
                        exp_timestamp = int(exp_date.timestamp())
                        expirations.add(exp_timestamp)
                    except ValueError:
                        if isinstance(option['expirationDate'], int):
                            expirations.add(option['expirationDate'])
            
            expirations_list = sorted(list(expirations))
            print(f"✅ {len(expirations_list)} dates d'expiration trouvées (structure data)")
            return expirations_list
        else:
            print("❌ Aucune donnée d'options trouvée")
            return []
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout lors de la récupération des expirations pour {ticker}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des expirations: {e}")
        return []
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return []


def get_implied_volatility(ticker: str, expiration: int):
    """
    Récupère la volatilité implicite des options pour un ticker et une date d'expiration donnés.
    
    Args:
        ticker (str): Le symbole du titre (ex: "AAPL")
        expiration (int): Timestamp UNIX de la date d'expiration
    
    Returns:
        pd.DataFrame: DataFrame contenant les données de volatilité implicite
    """
    if not API_KEY:
        print("❌ Clé API Finnhub non configurée")
        return pd.DataFrame()

    url = f"{BASE_URL}/stock/option-chain"
    params = {
        'symbol': ticker,
        'expiration': expiration,
        'token': API_KEY
    }
    
    try:
        print(f"Récupération des options pour {ticker} - expiration: {expiration}")
        print(f"Date d'expiration: {datetime.fromtimestamp(expiration).strftime('%Y-%m-%d')}")
        
        response = requests.get(url, params=params, timeout=15) # Timeout de 15 secondes
        response.raise_for_status()
        
        data = response.json()
        
        # L'API Finnhub retourne directement un tableau d'options
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ {len(data)} options trouvées")
            options_data = []
            
            for option in data:
                # Vérifier que c'est l'expiration demandée
                if 'expirationDate' in option:
                    option_exp_date = datetime.strptime(option['expirationDate'], '%Y-%m-%d')
                    target_exp_date = datetime.fromtimestamp(expiration)
                    
                    # Comparer les dates (ignorer l'heure)
                    if option_exp_date.date() == target_exp_date.date():
                        option_data = {
                            'contractSymbol': option.get('contractName', ''),
                            'type': option.get('type', '').lower(),
                            'strike': float(option.get('strike', 0)),
                            'lastPrice': float(option.get('lastPrice', 0)) if option.get('lastPrice') is not None else 0.0,
                            'impliedVolatility': float(option.get('impliedVolatility', 0)) / 100.0 if option.get('impliedVolatility') is not None else 0.0
                        }
                        options_data.append(option_data)
            
            if not options_data:
                print("❌ Aucune option trouvée pour cette expiration")
                return pd.DataFrame()
                
        elif 'data' in data and data['data']:
            # Structure alternative avec 'data'
            print(f"✅ Structure data trouvée")
            options_data = []
            
            for expiration_data in data['data']:
                if 'options' in expiration_data:
                    # Traiter les calls
                    if 'CALL' in expiration_data['options']:
                        for call in expiration_data['options']['CALL']:
                            option_data = {
                                'contractSymbol': call['contractName'],
                                'type': 'call',
                                'strike': float(call['strike']),
                                'lastPrice': float(call['lastPrice']) if call['lastPrice'] is not None else 0.0,
                                'impliedVolatility': float(call['impliedVolatility']) / 100.0 if call['impliedVolatility'] is not None else 0.0
                            }
                            options_data.append(option_data)
                    
                    # Traiter les puts
                    if 'PUT' in expiration_data['options']:
                        for put in expiration_data['options']['PUT']:
                            option_data = {
                                'contractSymbol': put['contractName'],
                                'type': 'put',
                                'strike': float(put['strike']),
                                'lastPrice': float(put['lastPrice']) if put['lastPrice'] is not None else 0.0,
                                'impliedVolatility': float(put['impliedVolatility']) / 100.0 if put['impliedVolatility'] is not None else 0.0
                            }
                            options_data.append(option_data)
        else:
            print("❌ Aucune donnée d'options trouvée pour cette expiration")
            return pd.DataFrame()
        
        if not options_data:
            print("❌ Aucune option avec les données requises trouvée")
            return pd.DataFrame()
        
        # Créer le DataFrame
        df = pd.DataFrame(options_data)
        
        # Remplacer les valeurs NaN par 0 dans impliedVolatility
        df['impliedVolatility'] = df['impliedVolatility'].fillna(0)
        
        # Trier par strike croissant
        df = df.sort_values('strike')
        
        print(f"✅ {len(df)} options récupérées avec succès")
        print(f"  - Calls: {len(df[df['type'] == 'call'])}")
        print(f"  - Puts: {len(df[df['type'] == 'put'])}")
        
        return df
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout lors de la récupération des options pour {ticker} - expiration: {expiration}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête HTTP: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Code d'erreur: {e.response.status_code}")
            print(f"Réponse: {e.response.text}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return pd.DataFrame()


def test_api_connection():
    """
    Teste la connexion à l'API Finnhub
    """
    if not API_KEY:
        print("❌ Clé API Finnhub non configurée, impossible de tester la connexion.")
        return False

    print("🔍 Test de connexion à l'API Finnhub...")
    
    # Test simple avec un appel à l'API
    url = f"{BASE_URL}/quote"
    params = {
        'symbol': 'AAPL',
        'token': API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10) # Timeout de 10 secondes
        response.raise_for_status()
        
        data = response.json()
        if 'c' in data:
            print(f"✅ Connexion API réussie - Prix AAPL: ${data['c']}")
            return True
        else:
            print("❌ Réponse API invalide")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout lors du test de connexion API.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion API: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Extraction de volatilité implicite via l'API Finnhub")
    print("=" * 60)
    
    # Vérifier la clé API
    if API_KEY == "YOUR_FINNHUB_API_KEY":
        print("❌ ERREUR: Veuillez configurer votre clé API Finnhub dans la variable API_KEY")
        print("   Obtenez votre clé gratuite sur: https://finnhub.io/register")
        exit(1)
    
    # Test de connexion
    if not test_api_connection():
        print("❌ Impossible de se connecter à l'API Finnhub")
        exit(1)
    
    # Exemple d'utilisation
    ticker = "AAPL"
    
    try:
        # Récupérer les dates d'expiration disponibles
        expirations = get_options_expirations(ticker)
        
        if not expirations:
            print(f"❌ Aucune date d'expiration disponible pour {ticker}")
            exit(1)
        
        # Essayer plusieurs dates d'expiration jusqu'à trouver des options
        for expiration_str in expirations[:5]:  # Tester les 5 premières dates
            expiration_date = expiration_str  # Format déjà YYYY-MM-DD
            
            # Convertir en timestamp UNIX pour l'API
            try:
                expiration_timestamp = int(datetime.strptime(expiration_str, '%Y-%m-%d').timestamp())
            except:
                # Si c'est déjà un timestamp
                expiration_timestamp = int(expiration_str)
            
            print(f"\nTest avec la date d'expiration: {expiration_date}")
            
            # Récupérer la volatilité implicite
            volatility_data = get_implied_volatility(ticker, expiration_timestamp)
            
            if not volatility_data.empty:
                print(f"✅ Options trouvées pour {expiration_date}")
                break
            else:
                print(f"❌ Aucune option pour {expiration_date}, essai suivant...")
        else:
            print("❌ Aucune option trouvée pour les 5 premières dates d'expiration")
            exit(1)
        
        print(f"\nTicker: {ticker}")
        print(f"Date d'expiration utilisée: {expiration_date}")
        print("-" * 50)
        
        if not volatility_data.empty:
            print(f"\n✅ Données de volatilité implicite récupérées avec succès!")
            
            # Afficher les données
            print("\nDonnées de volatilité implicite (premières 10 lignes):")
            print(volatility_data.head(10))
            
            print(f"\nStatistiques:")
            print(f"Nombre total d'options: {len(volatility_data)}")
            print(f"Nombre de calls: {len(volatility_data[volatility_data['type'] == 'call'])}")
            print(f"Nombre de puts: {len(volatility_data[volatility_data['type'] == 'put'])}")
            
            # Statistiques de volatilité implicite
            print(f"\nStatistiques de volatilité implicite:")
            print(f"Min: {volatility_data['impliedVolatility'].min():.4f}")
            print(f"Max: {volatility_data['impliedVolatility'].max():.4f}")
            print(f"Moyenne: {volatility_data['impliedVolatility'].mean():.4f}")
            print(f"Écart-type: {volatility_data['impliedVolatility'].std():.4f}")
            
            # Afficher quelques exemples par type
            calls_data = volatility_data[volatility_data['type'] == 'call']
            puts_data = volatility_data[volatility_data['type'] == 'put']
            
            if len(calls_data) > 0:
                print(f"\nExemples de calls:")
                print(calls_data.head(5)[['strike', 'lastPrice', 'impliedVolatility']])
            
            if len(puts_data) > 0:
                print(f"\nExemples de puts:")
                print(puts_data.head(5)[['strike', 'lastPrice', 'impliedVolatility']])
            
        else:
            print("❌ Aucune donnée de volatilité implicite trouvée.")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()
