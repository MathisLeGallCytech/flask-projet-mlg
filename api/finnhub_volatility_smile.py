#!/usr/bin/env python3
"""
Module pour extraire le smile de volatilité via l'API Finnhub
Utilise une seule maturité pour créer une courbe de volatilité implicite
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time
from typing import Dict, List, Optional, Tuple

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
        API_KEY = "d2cdsh9r01qihtcraq80d2cdsh9r01qihtcraq8g"  # Clé API réelle
        BASE_URL = "https://finnhub.io/api/v1"


def get_single_maturity_options(ticker: str, target_maturity_days: int = 30) -> pd.DataFrame:
    """
    Récupère les options pour une maturité spécifique (en jours)
    
    Args:
        ticker (str): Le symbole du titre (ex: "SPY")
        target_maturity_days (int): Maturité cible en jours (défaut: 30 jours)
    
    Returns:
        pd.DataFrame: DataFrame contenant les options pour cette maturité
    """
    print(f"🔍 Récupération des options pour {ticker} avec maturité ~{target_maturity_days} jours")
    
    try:
        # Récupérer toutes les expirations disponibles
        url = f"{BASE_URL}/stock/option-chain"
        params = {
            'symbol': ticker,
            'token': API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or (isinstance(data, list) and len(data) == 0):
            print("❌ Aucune donnée d'options trouvée")
            return pd.DataFrame()
        
        # Traiter les données selon la structure
        options_data = []
        current_date = datetime.now()
        
        if isinstance(data, list):
            # Structure directe
            for option in data:
                if 'expirationDate' in option:
                    try:
                        exp_date = datetime.strptime(option['expirationDate'], '%Y-%m-%d')
                        days_to_expiry = (exp_date - current_date).days
                        
                        # Vérifier si cette expiration correspond à notre maturité cible
                        if abs(days_to_expiry - target_maturity_days) <= 7:  # Tolérance de ±7 jours
                            option_data = {
                                'contractSymbol': option.get('contractName', ''),
                                'type': option.get('type', '').lower(),
                                'strike': float(option.get('strike', 0)),
                                'lastPrice': float(option.get('lastPrice', 0)) if option.get('lastPrice') is not None else 0.0,
                                'bid': float(option.get('bid', 0)) if option.get('bid') is not None else 0.0,
                                'ask': float(option.get('ask', 0)) if option.get('ask') is not None else 0.0,
                                'volume': int(option.get('volume', 0)) if option.get('volume') is not None else 0,
                                'openInterest': int(option.get('openInterest', 0)) if option.get('openInterest') is not None else 0,
                                'impliedVolatility': float(option.get('impliedVolatility', 0)) / 100.0 if option.get('impliedVolatility') is not None else 0.0,
                                'expirationDate': option['expirationDate'],
                                'daysToExpiry': days_to_expiry
                            }
                            options_data.append(option_data)
                    except (ValueError, TypeError) as e:
                        print(f"⚠️  Erreur traitement option: {e}")
                        continue
        
        elif isinstance(data, dict) and 'data' in data:
            # Structure avec 'data'
            for expiration_data in data['data']:
                if 'options' in expiration_data and 'expirationDate' in expiration_data:
                    try:
                        exp_date = datetime.strptime(expiration_data['expirationDate'], '%Y-%m-%d')
                        days_to_expiry = (exp_date - current_date).days
                        
                        # Vérifier si cette expiration correspond à notre maturité cible
                        if abs(days_to_expiry - target_maturity_days) <= 7:  # Tolérance de ±7 jours
                            # Traiter les calls
                            if 'CALL' in expiration_data['options']:
                                for call in expiration_data['options']['CALL']:
                                    option_data = {
                                        'contractSymbol': call.get('contractName', ''),
                                        'type': 'call',
                                        'strike': float(call.get('strike', 0)),
                                        'lastPrice': float(call.get('lastPrice', 0)) if call.get('lastPrice') is not None else 0.0,
                                        'bid': float(call.get('bid', 0)) if call.get('bid') is not None else 0.0,
                                        'ask': float(call.get('ask', 0)) if call.get('ask') is not None else 0.0,
                                        'volume': int(call.get('volume', 0)) if call.get('volume') is not None else 0,
                                        'openInterest': int(call.get('openInterest', 0)) if call.get('openInterest') is not None else 0,
                                        'impliedVolatility': float(call.get('impliedVolatility', 0)) / 100.0 if call.get('impliedVolatility') is not None else 0.0,
                                        'expirationDate': expiration_data['expirationDate'],
                                        'daysToExpiry': days_to_expiry
                                    }
                                    options_data.append(option_data)
                            
                            # Traiter les puts
                            if 'PUT' in expiration_data['options']:
                                for put in expiration_data['options']['PUT']:
                                    option_data = {
                                        'contractSymbol': put.get('contractName', ''),
                                        'type': 'put',
                                        'strike': float(put.get('strike', 0)),
                                        'lastPrice': float(put.get('lastPrice', 0)) if put.get('lastPrice') is not None else 0.0,
                                        'bid': float(put.get('bid', 0)) if put.get('bid') is not None else 0.0,
                                        'ask': float(put.get('ask', 0)) if put.get('ask') is not None else 0.0,
                                        'volume': int(put.get('volume', 0)) if put.get('volume') is not None else 0,
                                        'openInterest': int(put.get('openInterest', 0)) if put.get('openInterest') is not None else 0,
                                        'impliedVolatility': float(put.get('impliedVolatility', 0)) / 100.0 if put.get('impliedVolatility') is not None else 0.0,
                                        'expirationDate': expiration_data['expirationDate'],
                                        'daysToExpiry': days_to_expiry
                                    }
                                    options_data.append(option_data)
                    except (ValueError, TypeError) as e:
                        print(f"⚠️  Erreur traitement expiration: {e}")
                        continue
        
        if not options_data:
            print(f"❌ Aucune option trouvée pour la maturité ~{target_maturity_days} jours")
            return pd.DataFrame()
        
        # Créer le DataFrame
        df = pd.DataFrame(options_data)
        
        # Nettoyer les données
        df = df[df['strike'] > 0]  # Filtrer les strikes invalides
        df = df[df['impliedVolatility'] > 0]  # Filtrer les IV invalides
        df = df.sort_values('strike')
        
        print(f"✅ {len(df)} options trouvées pour la maturité ~{target_maturity_days} jours")
        print(f"  - Calls: {len(df[df['type'] == 'call'])}")
        print(f"  - Puts: {len(df[df['type'] == 'put'])}")
        print(f"  - Maturité réelle: {df['daysToExpiry'].iloc[0] if len(df) > 0 else 'N/A'} jours")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête HTTP: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return pd.DataFrame()


def get_spot_price(ticker: str) -> float:
    """
    Récupère le prix spot actuel via l'API Finnhub
    
    Args:
        ticker (str): Le symbole du titre
    
    Returns:
        float: Prix spot actuel
    """
    try:
        url = f"{BASE_URL}/quote"
        params = {
            'symbol': ticker,
            'token': API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        spot_price = float(data.get('c', 0))
        
        if spot_price > 0:
            print(f"✅ Prix spot récupéré: ${spot_price:.2f}")
            return spot_price
        else:
            print("❌ Prix spot non disponible")
            return 0
            
    except Exception as e:
        print(f"❌ Erreur récupération prix spot: {e}")
        return 0


def create_volatility_smile(ticker: str, maturity_days: int = 30, span: float = 0.3) -> Dict:
    """
    Crée un smile de volatilité avec sélection automatique de la meilleure maturité
    
    Args:
        ticker (str): Le symbole du titre
        maturity_days (int): Maturité suggérée en jours (défaut: 30) - sera ajustée automatiquement
        span (float): Bande autour du spot (défaut: 0.3 = ±30%)
    
    Returns:
        Dict: Dictionnaire contenant les données du smile
    """
    print(f"🚀 Création du smile de volatilité pour {ticker}")
    print(f"Paramètres: maturité suggérée={maturity_days} jours, span={span}")
    
    try:
        # Récupérer le prix spot
        spot_price = get_spot_price(ticker)
        if spot_price <= 0:
            return {'error': 'Prix spot non disponible'}
        
        # Essayer d'abord la maturité suggérée
        options_df = get_single_maturity_options(ticker, maturity_days)
        
        # Si pas de données, essayer d'autres maturités
        if options_df.empty:
            print(f"⚠️  Aucune option pour {maturity_days} jours, recherche de la meilleure maturité...")
            
            # Essayer différentes maturités
            test_maturities = [7, 14, 21, 30, 45, 60, 90, 180]
            best_options = pd.DataFrame()
            best_maturity = maturity_days
            
            for test_maturity in test_maturities:
                if test_maturity != maturity_days:  # Éviter de refaire le test initial
                    test_df = get_single_maturity_options(ticker, test_maturity)
                    if len(test_df) > len(best_options):
                        best_options = test_df
                        best_maturity = test_maturity
                        print(f"✅ Maturité {test_maturity} jours: {len(test_df)} options trouvées")
            
            if not best_options.empty:
                options_df = best_options
                maturity_days = best_maturity
                print(f"🎯 Utilisation de la maturité {maturity_days} jours avec {len(options_df)} options")
            else:
                return {'error': f'Aucune option disponible pour {ticker} dans les maturités testées'}
        
        if options_df.empty:
            return {'error': f'Aucune option disponible pour {ticker}'}
        
        # Filtrer par bande autour du spot
        min_strike = spot_price * (1 - span)
        max_strike = spot_price * (1 + span)
        filtered_df = options_df[
            (options_df['strike'] >= min_strike) & 
            (options_df['strike'] <= max_strike)
        ]
        
        if len(filtered_df) < 5:
            print("⚠️  Filtrage trop restrictif, utilisation de toutes les données")
            filtered_df = options_df
        
        # Séparer les calls et puts
        calls_df = filtered_df[filtered_df['type'] == 'call'].copy()
        puts_df = filtered_df[filtered_df['type'] == 'put'].copy()
        
        # Calculer les statistiques
        stats = {
            'total_options': len(filtered_df),
            'calls_count': len(calls_df),
            'puts_count': len(puts_df),
            'min_strike': float(filtered_df['strike'].min()),
            'max_strike': float(filtered_df['strike'].max()),
            'min_iv': float(filtered_df['impliedVolatility'].min()),
            'max_iv': float(filtered_df['impliedVolatility'].max()),
            'avg_iv': float(filtered_df['impliedVolatility'].mean()),
            'std_iv': float(filtered_df['impliedVolatility'].std()),
            'maturity_days': int(filtered_df['daysToExpiry'].iloc[0]) if len(filtered_df) > 0 else maturity_days
        }
        
        # Préparer les données pour le graphique
        result = {
            'symbol': ticker,
            'spot_price': spot_price,
            'data_source': 'Finnhub API (Données Réelles)',
            'maturity_days': stats['maturity_days'],
            'maturity_years': stats['maturity_days'] / 365.25,
            'strikes': filtered_df['strike'].tolist(),
            'calls_iv': calls_df['impliedVolatility'].tolist() if len(calls_df) > 0 else [],
            'puts_iv': puts_df['impliedVolatility'].tolist() if len(puts_df) > 0 else [],
            'calls_strikes': calls_df['strike'].tolist() if len(calls_df) > 0 else [],
            'puts_strikes': puts_df['strike'].tolist() if len(puts_df) > 0 else [],
            'statistics': stats,
            'raw_options': filtered_df.to_dict('records')
        }
        
        print(f"✅ Smile de volatilité créé avec succès")
        print(f"   • {len(filtered_df)} options totales")
        print(f"   • {len(calls_df)} calls, {len(puts_df)} puts")
        print(f"   • IV min: {stats['min_iv']:.3f} ({stats['min_iv']*100:.1f}%)")
        print(f"   • IV max: {stats['max_iv']:.3f} ({stats['max_iv']*100:.1f}%)")
        print(f"   • IV moy: {stats['avg_iv']:.3f} ({stats['avg_iv']*100:.1f}%)")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du smile: {e}")
        return {'error': f'Erreur: {str(e)}'}


def test_api_connection() -> bool:
    """
    Teste la connexion à l'API Finnhub
    
    Returns:
        bool: True si la connexion réussit, False sinon
    """
    print("🔍 Test de connexion à l'API Finnhub...")
    
    try:
        url = f"{BASE_URL}/quote"
        params = {
            'symbol': 'SPY',
            'token': API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'c' in data and data['c'] > 0:
            print(f"✅ Connexion API réussie - Prix SPY: ${data['c']}")
            return True
        else:
            print("❌ Réponse API invalide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion API: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Test du module Smile de Volatilité Finnhub")
    print("=" * 60)
    
    # Test de connexion
    if not test_api_connection():
        print("❌ Impossible de se connecter à l'API Finnhub")
        exit(1)
    
    # Test avec SPY
    ticker = "SPY"
    
    try:
        # Test avec différentes maturités
        maturities = [30, 60, 90]  # 1 mois, 2 mois, 3 mois
        
        for maturity in maturities:
            print(f"\n📊 Test du smile pour {ticker} - {maturity} jours")
            print("-" * 50)
            
            smile_data = create_volatility_smile(ticker, maturity, 0.3)
            
            if 'error' not in smile_data:
                print(f"✅ Smile créé avec succès!")
                print(f"  • Prix spot: ${smile_data['spot_price']:.2f}")
                print(f"  • Maturité: {smile_data['maturity_days']} jours ({smile_data['maturity_years']:.2f} ans)")
                print(f"  • Options totales: {smile_data['statistics']['total_options']}")
                print(f"  • Calls: {smile_data['statistics']['calls_count']}")
                print(f"  • Puts: {smile_data['statistics']['puts_count']}")
                print(f"  • IV min: {smile_data['statistics']['min_iv']:.3f}")
                print(f"  • IV max: {smile_data['statistics']['max_iv']:.3f}")
                print(f"  • IV moy: {smile_data['statistics']['avg_iv']:.3f}")
                
                # Afficher quelques exemples
                if smile_data['calls_iv']:
                    print(f"\nExemples de calls:")
                    for i in range(min(3, len(smile_data['calls_strikes']))):
                        print(f"  Strike: ${smile_data['calls_strikes'][i]:.2f}, IV: {smile_data['calls_iv'][i]*100:.1f}%")
                
                if smile_data['puts_iv']:
                    print(f"\nExemples de puts:")
                    for i in range(min(3, len(smile_data['puts_strikes']))):
                        print(f"  Strike: ${smile_data['puts_strikes'][i]:.2f}, IV: {smile_data['puts_iv'][i]*100:.1f}%")
                
                break  # Arrêter après le premier succès
            else:
                print(f"❌ Erreur: {smile_data['error']}")
        
        else:
            print("❌ Aucun smile créé pour les maturités testées")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
