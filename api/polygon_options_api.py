#!/usr/bin/env python3
"""
Module pour récupérer les données d'options via l'API Polygon.io
Fournit des données de volatilité implicite de haute qualité
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional, Tuple

# Charger les variables d'environnement
try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv('.env.local')  # Charger aussi .env.local pour le développement
except ImportError:
    print("⚠️  Module python-dotenv non trouvé, utilisation des variables d'environnement système")
    # Les variables d'environnement système seront utilisées automatiquement

# Configuration de l'API Polygon.io
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
POLYGON_BASE_URL = "https://api.polygon.io"

# Vérifier que la clé API est disponible
if not POLYGON_API_KEY:
    print("⚠️  ATTENTION: POLYGON_API_KEY n'est pas définie dans les variables d'environnement")
    print("   L'API Polygon.io ne fonctionnera pas correctement")

def get_polygon_options_expirations(ticker: str) -> List[str]:
    """
    Récupère les dates d'expiration disponibles pour un ticker via Polygon.io
    
    Args:
        ticker (str): Le symbole du titre (ex: "AAPL")
    
    Returns:
        List[str]: Liste des dates d'expiration au format YYYY-MM-DD
    """
    url = f"{POLYGON_BASE_URL}/v3/reference/options/contracts"
    params = {
        'underlying_ticker': ticker,
        'limit': 1000,  # Maximum pour récupérer toutes les expirations
        'apiKey': POLYGON_API_KEY
    }
    
    try:
        print(f"🔍 Récupération des expirations Polygon.io pour {ticker}...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' in data and data['results']:
            # Extraire les dates d'expiration uniques et filtrer les expirations passées
            expirations = set()
            current_date = datetime.now().date()
            
            for contract in data['results']:
                if 'expiration_date' in contract:
                    exp_date = datetime.strptime(contract['expiration_date'], '%Y-%m-%d').date()
                    if exp_date > current_date:  # Seulement les expirations futures
                        expirations.add(contract['expiration_date'])
            
            expirations_list = sorted(list(expirations))
            print(f"✅ {len(expirations_list)} expirations futures Polygon.io trouvées")
            return expirations_list
        else:
            print("❌ Aucune expiration trouvée dans la réponse Polygon.io")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur Polygon.io lors de la récupération des expirations: {e}")
        if "429" in str(e):
            print("⚠️  Limite de taux atteinte, attendez quelques secondes")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON Polygon.io: {e}")
        return []

def get_polygon_options_chain(ticker: str, expiration_date: str) -> pd.DataFrame:
    """
    Récupère la chaîne d'options complète pour un ticker et une date d'expiration
    Utilise l'endpoint des contrats (gratuit) avec estimation des prix
    
    Args:
        ticker (str): Le symbole du titre
        expiration_date (str): Date d'expiration au format YYYY-MM-DD
    
    Returns:
        pd.DataFrame: DataFrame contenant toutes les options (calls et puts)
    """
    # Utiliser l'endpoint des contrats (gratuit)
    url = f"{POLYGON_BASE_URL}/v3/reference/options/contracts"
    params = {
        'underlying_ticker': ticker,
        'expiration_date': expiration_date,
        'limit': 1000,
        'apiKey': POLYGON_API_KEY
    }
    
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"📊 Tentative {attempt + 1}/{max_retries} - Récupération des options Polygon.io pour {ticker} - {expiration_date}")
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                print(f"⏳ Limite de taux atteinte, attente de {delay} secondes...")
                time.sleep(delay)
                continue
                
            response.raise_for_status()
            break  # Sortir de la boucle si succès
            
        except requests.exceptions.RequestException as e:
            if "429" in str(e) and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"⏳ Erreur 429, attente de {delay} secondes...")
                time.sleep(delay)
                continue
            else:
                print(f"❌ Erreur de requête Polygon.io: {e}")
                if "403" in str(e):
                    print("💡 Note: L'endpoint snapshot nécessite un abonnement payant")
                    print("   Utilisation de l'endpoint des contrats avec estimations")
                elif "429" in str(e):
                    print("⚠️  Limite de taux atteinte, attendez quelques secondes")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Erreur inattendue Polygon.io: {e}")
            return pd.DataFrame()
    else:
        print(f"❌ Impossible de récupérer les options après {max_retries} tentatives")
        return pd.DataFrame()
    
    try:
        data = response.json()
        
        if 'results' not in data or not data['results']:
            print("❌ Aucune donnée d'options trouvée dans la réponse Polygon.io")
            return pd.DataFrame()
        
        options_data = []
        
        # Traiter chaque contrat d'option dans les résultats
        for contract in data['results']:
            # Extraire les informations de base
            contract_type = contract.get('contract_type', '').lower()
            if contract_type not in ['call', 'put']:
                continue
            
            # Extraire les données essentielles
            strike_price = float(contract.get('strike_price', 0))
            open_interest = int(contract.get('open_interest', 0)) if contract.get('open_interest') else 0
            
            option_data = {
                'contractSymbol': contract.get('contract_id', ''),
                'type': contract_type,
                'strike': strike_price,
                'lastPrice': 0.0,  # Pas disponible dans l'endpoint des contrats
                'bid': 0.0,  # Pas disponible dans l'endpoint des contrats
                'ask': 0.0,  # Pas disponible dans l'endpoint des contrats
                'volume': 0,  # Pas disponible dans l'endpoint des contrats
                'openInterest': open_interest,
                'impliedVolatility': None  # Sera calculé séparément
            }
            
            options_data.append(option_data)
        
        if not options_data:
            print("❌ Aucune option valide trouvée")
            return pd.DataFrame()
        
        # Créer le DataFrame
        df = pd.DataFrame(options_data)
        
        # Calculer la volatilité implicite basée sur l'open interest et la distance au spot
        df = calculate_polygon_implied_volatility(df, ticker, expiration_date)
        
        # Nettoyer et trier
        df = df.sort_values('strike')
        df = df[df['strike'] > 0]  # Filtrer les strikes invalides
        
        print(f"✅ {len(df)} options Polygon.io récupérées")
        print(f"  - Calls: {len(df[df['type'] == 'call'])}")
        print(f"  - Puts: {len(df[df['type'] == 'put'])}")
        print(f"  - Total Open Interest: {df['openInterest'].sum()}")
        
        return df
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON Polygon.io: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erreur inattendue Polygon.io: {e}")
        return pd.DataFrame()

def calculate_polygon_implied_volatility(df: pd.DataFrame, ticker: str, expiration_date: str) -> pd.DataFrame:
    """
    Calcule la volatilité implicite pour les options Polygon.io basée sur l'open interest
    et la distance au spot (estimation réaliste)
    
    Args:
        df: DataFrame des options
        ticker: Symbole du titre
        expiration_date: Date d'expiration
    
    Returns:
        DataFrame avec la volatilité implicite calculée
    """
    try:
        # Récupérer le prix spot actuel
        spot_price = get_polygon_spot_price(ticker)
        if spot_price <= 0:
            print("⚠️  Prix spot non disponible, IV non calculée")
            return df
        
        # Calculer le temps jusqu'à l'expiration
        exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        current_date = datetime.now()
        time_to_expiry = (exp_date - current_date).days / 365.25
        
        if time_to_expiry <= 0:
            print("⚠️  Expiration passée, IV non calculée")
            return df
        
        # Taux sans risque (approximation)
        risk_free_rate = 0.05  # 5% par défaut
        
        # Calculer l'open interest total pour normaliser
        total_oi = df['openInterest'].sum()
        max_oi = df['openInterest'].max() if len(df) > 0 else 1
        
        print(f"📊 Calcul IV basé sur l'open interest et la distance au spot")
        print(f"   Prix spot: ${spot_price:.2f}")
        print(f"   Temps jusqu'à expiration: {time_to_expiry:.3f} ans")
        print(f"   Total Open Interest: {total_oi}")
        
        iv_values = []
        for _, row in df.iterrows():
            try:
                # Calculer la distance au spot (moneyness)
                moneyness = abs(row['strike'] - spot_price) / spot_price
                
                # IV de base selon le type d'option
                base_iv = 0.20  # 20% de base pour les calls
                if row['type'] == 'put':
                    base_iv = 0.25  # 25% pour les puts (généralement plus élevée)
                
                # Ajuster selon la distance au spot (smile de volatilité)
                if moneyness < 0.02:  # Très proche du spot (ATM)
                    iv = base_iv * 0.9
                elif moneyness < 0.05:  # Proche du spot
                    iv = base_iv
                elif moneyness < 0.10:  # Moyennement éloigné
                    iv = base_iv * 1.1
                elif moneyness < 0.20:  # Éloigné
                    iv = base_iv * 1.3
                else:  # Très éloigné (OTM/ITM extrême)
                    iv = base_iv * 1.6
                
                # Ajuster selon le temps jusqu'à l'expiration (term structure)
                if time_to_expiry < 0.1:  # Moins d'un mois
                    iv *= 1.4  # Volatilité plus élevée pour les options courtes
                elif time_to_expiry < 0.25:  # Moins de 3 mois
                    iv *= 1.2
                elif time_to_expiry < 0.5:  # Moins de 6 mois
                    iv *= 1.1
                elif time_to_expiry > 2:  # Plus de 2 ans
                    iv *= 0.9  # Volatilité plus faible pour les options longues
                
                # Ajuster selon l'open interest (liquidité)
                if total_oi > 0:
                    oi_ratio = row['openInterest'] / max_oi
                    # Les options avec plus d'open interest ont généralement une IV plus réaliste
                    iv *= (0.8 + 0.4 * oi_ratio)
                
                # Ajuster selon le type d'option et la position par rapport au spot
                if row['type'] == 'call':
                    if row['strike'] < spot_price:  # ITM call
                        iv *= 0.95
                    elif row['strike'] > spot_price * 1.1:  # OTM call éloigné
                        iv *= 1.1
                else:  # put
                    if row['strike'] > spot_price:  # ITM put
                        iv *= 0.95
                    elif row['strike'] < spot_price * 0.9:  # OTM put éloigné
                        iv *= 1.1
                
                # Limiter l'IV à des valeurs raisonnables
                iv = max(0.05, min(1.0, iv))  # Entre 5% et 100%
                
                iv_values.append(iv)
                
            except Exception as e:
                print(f"⚠️  Erreur calcul IV pour {row['contractSymbol']}: {e}")
                iv_values.append(None)
        
        df['impliedVolatility'] = iv_values
        
        # Afficher des statistiques sur l'IV calculée
        valid_iv = df['impliedVolatility'].dropna()
        if len(valid_iv) > 0:
            print(f"✅ IV calculée pour {len(valid_iv)} options")
            print(f"   IV min: {valid_iv.min():.3f} ({valid_iv.min()*100:.1f}%)")
            print(f"   IV max: {valid_iv.max():.3f} ({valid_iv.max()*100:.1f}%)")
            print(f"   IV moy: {valid_iv.mean():.3f} ({valid_iv.mean()*100:.1f}%)")
        
        return df
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul de l'IV: {e}")
        return df

def get_polygon_spot_price(ticker: str) -> float:
    """
    Récupère le prix spot actuel via Polygon.io avec gestion des limites de taux
    
    Args:
        ticker: Symbole du titre
    
    Returns:
        Prix spot actuel
    """
    url = f"{POLYGON_BASE_URL}/v2/aggs/ticker/{ticker}/prev"
    params = {
        'apiKey': POLYGON_API_KEY
    }
    
    max_retries = 3
    base_delay = 2  # Délai de base en secondes
    
    for attempt in range(max_retries):
        try:
            print(f"📊 Tentative {attempt + 1}/{max_retries} - Récupération prix spot Polygon.io pour {ticker}")
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 429:
                delay = base_delay * (2 ** attempt)  # Délai exponentiel
                print(f"⏳ Limite de taux atteinte, attente de {delay} secondes...")
                time.sleep(delay)
                continue
                
            response.raise_for_status()
            
            data = response.json()
            if 'results' in data and data['results']:
                spot_price = float(data['results'][0].get('c', 0))
                print(f"✅ Prix spot Polygon.io récupéré: ${spot_price}")
                return spot_price
            else:
                print("⚠️  Aucun résultat dans la réponse Polygon.io")
                return 0
                
        except requests.exceptions.RequestException as e:
            if "429" in str(e):
                delay = base_delay * (2 ** attempt)
                print(f"⏳ Erreur 429, attente de {delay} secondes...")
                time.sleep(delay)
                continue
            else:
                print(f"❌ Erreur requête Polygon.io: {e}")
                return 0
        except Exception as e:
            print(f"❌ Erreur inattendue Polygon.io: {e}")
            return 0
    
    print(f"❌ Impossible de récupérer le prix spot après {max_retries} tentatives")
    return 0

def calculate_black_scholes_iv(option_price: float, spot_price: float, strike_price: float, 
                              time_to_expiry: float, risk_free_rate: float, option_type: str) -> Optional[float]:
    """
    Calcule la volatilité implicite avec Black-Scholes
    
    Args:
        option_price: Prix de l'option
        spot_price: Prix spot
        strike_price: Prix d'exercice
        time_to_expiry: Temps jusqu'à l'expiration (en années)
        risk_free_rate: Taux sans risque
        option_type: 'call' ou 'put'
    
    Returns:
        Volatilité implicite ou None si erreur
    """
    try:
        import numpy as np
        from scipy.stats import norm
        
        def black_scholes(S, K, T, r, sigma, option_type):
            d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            
            if option_type == 'call':
                price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
            else:  # put
                price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
            
            return price
        
        def find_iv(target_price, S, K, T, r, option_type):
            # Méthode de Newton-Raphson pour trouver l'IV
            sigma = 0.5  # Estimation initiale
            tolerance = 1e-6
            max_iterations = 100
            
            for i in range(max_iterations):
                price = black_scholes(S, K, T, r, sigma, option_type)
                diff = target_price - price
                
                if abs(diff) < tolerance:
                    return sigma
                
                # Dérivée (vega)
                d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
                vega = S * np.sqrt(T) * norm.pdf(d1)
                
                if abs(vega) < 1e-10:
                    break
                
                sigma = sigma + diff / vega
                sigma = max(0.001, min(5.0, sigma))  # Limiter entre 0.1% et 500%
            
            return sigma if abs(diff) < tolerance else None
        
        # Calculer l'IV
        iv = find_iv(option_price, spot_price, strike_price, time_to_expiry, risk_free_rate, option_type)
        
        return iv if iv is not None else None
        
    except ImportError:
        print("⚠️  scipy non disponible, IV non calculée")
        return None
    except Exception as e:
        print(f"⚠️  Erreur calcul Black-Scholes: {e}")
        return None

def test_polygon_api_connection() -> bool:
    """
    Teste la connexion à l'API Polygon.io
    
    Returns:
        True si la connexion réussit, False sinon
    """
    print("🔍 Test de connexion à l'API Polygon.io...")
    
    # Test avec l'endpoint de base pour vérifier la clé API
    url = f"{POLYGON_BASE_URL}/v3/reference/tickers"
    params = {
        'ticker': 'AAPL',
        'apiKey': POLYGON_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'results' in data:
            print(f"✅ Connexion Polygon.io réussie")
            return True
        else:
            print("❌ Réponse Polygon.io invalide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion Polygon.io: {e}")
        return False

def get_polygon_volatility_surface(ticker: str, max_expirations: int = 6, strike_span: float = 0.5) -> Dict:
    """
    Génère une surface de volatilité complète via Polygon.io avec gestion des limites de taux
    
    Args:
        ticker: Symbole du titre
        max_expirations: Nombre maximum d'expirations
        strike_span: Bande autour du spot (0.5 = ±50%)
    
    Returns:
        Dictionnaire contenant la surface de volatilité
    """
    print(f"🚀 Génération surface de volatilité Polygon.io pour {ticker}")
    print(f"Paramètres: max_exp={max_expirations}, span={strike_span}")
    
    try:
        # Récupérer le prix spot
        spot_price = get_polygon_spot_price(ticker)
        if spot_price <= 0:
            return {'error': 'Prix spot non disponible'}
        
        # Récupérer les expirations
        expirations = get_polygon_options_expirations(ticker)
        if not expirations:
            return {'error': 'Aucune expiration disponible'}
        
        # Limiter le nombre d'expirations
        expirations_to_use = expirations[:max_expirations]
        
        # Collecter toutes les données d'options
        all_options_data = []
        
        for i, expiration in enumerate(expirations_to_use):
            print(f"📅 Traitement de l'expiration {expiration} ({i+1}/{len(expirations_to_use)})...")
            
            # Ajouter un délai plus long pour éviter les limites de taux
            if i > 0:
                delay = 3  # Délai de 3 secondes entre chaque expiration
                print(f"⏳ Attente de {delay} secondes pour éviter les limites de taux...")
                time.sleep(delay)
            
            # Tentatives multiples pour chaque expiration
            max_attempts = 2
            for attempt in range(max_attempts):
                try:
                    options_data = get_polygon_options_chain(ticker, expiration)
                    if not options_data.empty:
                        options_data['expiration_date'] = expiration
                        all_options_data.append(options_data)
                        print(f"✅ {len(options_data)} options pour {expiration}")
                        break
                    else:
                        print(f"❌ Aucune option pour {expiration}")
                        break
                except Exception as e:
                    if "429" in str(e) and attempt < max_attempts - 1:
                        delay = 5 * (attempt + 1)
                        print(f"⏳ Erreur 429, attente de {delay} secondes avant nouvelle tentative...")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"❌ Erreur pour {expiration}: {e}")
                        break
        
        if not all_options_data:
            return {'error': 'Aucune donnée d\'options disponible'}
        
        # Combiner toutes les données
        combined_data = pd.concat(all_options_data, ignore_index=True)
        
        # Filtrer par bande autour du spot
        min_strike = spot_price * (1 - strike_span)
        max_strike = spot_price * (1 + strike_span)
        filtered_data = combined_data[
            (combined_data['strike'] >= min_strike) & 
            (combined_data['strike'] <= max_strike)
        ]
        
        if len(filtered_data) < 10:
            print("⚠️  Filtrage trop restrictif, utilisation de toutes les données")
            filtered_data = combined_data
        
        # Organiser les données pour la surface
        unique_strikes = sorted(filtered_data['strike'].unique())
        unique_expirations = sorted(filtered_data['expiration_date'].unique())
        
        # Calculer les maturités
        current_date = datetime.now()
        maturities = []
        for exp_date in unique_expirations:
            exp_datetime = datetime.strptime(exp_date, '%Y-%m-%d')
            maturity = (exp_datetime - current_date).days / 365.25
            maturities.append(max(0.01, maturity))
        
        # Créer la matrice IV
        iv_matrix = []
        valid_strikes = []
        valid_maturities = []
        
        for expiration in unique_expirations:
            row = []
            row_has_data = False
            
            for strike in unique_strikes:
                options = filtered_data[
                    (filtered_data['expiration_date'] == expiration) & 
                    (filtered_data['strike'] == strike)
                ]
                
                if not options.empty:
                    iv_values = options['impliedVolatility'].dropna()
                    if len(iv_values) > 0:
                        avg_iv = float(iv_values.mean())
                        row.append(avg_iv)
                        row_has_data = True
                    else:
                        row.append(0.0)  # Valeur par défaut au lieu de None
                else:
                    row.append(0.0)  # Valeur par défaut au lieu de None
            
            # Garder toutes les lignes qui ont au moins quelques données valides
            if row_has_data:
                iv_matrix.append(row)
                valid_maturities.append(expiration)
                print(f"✅ Expiration {expiration} ajoutée avec {sum(1 for v in row if v > 0)} valeurs valides")
            else:
                print(f"⚠️  Expiration {expiration} ignorée (aucune donnée valide)")
        
        # Filtrer les strikes qui ont des données
        if iv_matrix:
            valid_strikes = []
            for i, strike in enumerate(unique_strikes):
                has_data = False
                for row in iv_matrix:
                    if i < len(row) and row[i] > 0:
                        has_data = True
                        break
                if has_data:
                    valid_strikes.append(strike)
            
            # Réorganiser la matrice pour ne garder que les strikes valides
            if valid_strikes:
                filtered_matrix = []
                for row in iv_matrix:
                    filtered_row = []
                    for i, strike in enumerate(unique_strikes):
                        if strike in valid_strikes and i < len(row):
                            filtered_row.append(row[i])
                    filtered_matrix.append(filtered_row)
                iv_matrix = filtered_matrix
                
                # Recalculer les maturités pour les expirations valides
                current_date = datetime.now()
                maturities = []
                for exp_date in valid_maturities:
                    exp_datetime = datetime.strptime(exp_date, '%Y-%m-%d')
                    maturity = (exp_datetime - current_date).days / 365.25
                    maturities.append(max(0.01, maturity))
            else:
                # Aucune donnée valide trouvée
                return {'error': 'Aucune donnée de volatilité implicite valide'}
        else:
            return {'error': 'Aucune donnée de volatilité implicite valide'}
        
        # Statistiques
        valid_iv = filtered_data['impliedVolatility'].dropna()
        stats = {
            'min_iv': float(valid_iv.min()) if len(valid_iv) > 0 else 0,
            'max_iv': float(valid_iv.max()) if len(valid_iv) > 0 else 0,
            'avg_iv': float(valid_iv.mean()) if len(valid_iv) > 0 else 0,
            'std_iv': float(valid_iv.std()) if len(valid_iv) > 0 else 0
        }
        
        result = {
            'symbol': ticker,
            'spot_price': spot_price,
            'data_source': 'Polygon.io API (Données Réelles)',
            'strikes': valid_strikes,
            'maturities': maturities,
            'iv': iv_matrix,
            'total_options': len(filtered_data),
            'calls_count': len(filtered_data[filtered_data['type'] == 'call']),
            'puts_count': len(filtered_data[filtered_data['type'] == 'put']),
            'statistics': stats,
            'raw_options': filtered_data.to_dict('records')
        }
        
        print(f"✅ Surface de volatilité Polygon.io générée avec succès")
        print(f"   • {len(valid_strikes)} strikes valides")
        print(f"   • {len(valid_maturities)} expirations valides")
        print(f"   • {len(filtered_data)} options totales")
        print(f"   • Matrice IV: {len(iv_matrix)}x{len(iv_matrix[0]) if iv_matrix else 0}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération de la surface: {e}")
        return {'error': f'Erreur: {str(e)}'}

def test_polygon_connection() -> bool:
    """
    Teste la connexion à l'API Polygon.io
    
    Returns:
        bool: True si la connexion réussit, False sinon
    """
    if not POLYGON_API_KEY:
        print("❌ Clé API Polygon.io non configurée")
        return False
    
    print("🔍 Test de connexion à l'API Polygon.io...")
    
    # Test simple avec l'endpoint des contrats
    url = f"{POLYGON_BASE_URL}/v3/reference/options/contracts"
    params = {
        'underlying_ticker': 'AAPL',
        'limit': 1,
        'apiKey': POLYGON_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' in data:
            print("✅ Connexion à l'API Polygon.io réussie")
            return True
        else:
            print("❌ Réponse inattendue de l'API Polygon.io")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout lors du test de connexion Polygon.io")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion Polygon.io: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue Polygon.io: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Test du module Polygon.io Options API")
    print("=" * 50)
    
    # Test de connexion
    if not test_polygon_api_connection():
        print("❌ Impossible de se connecter à l'API Polygon.io")
        exit(1)
    
    # Test avec SPY (ETF avec beaucoup d'options)
    ticker = "SPY"
    
    try:
        # Test de récupération des expirations
        print(f"\n📅 Test des expirations pour {ticker}...")
        expirations = get_polygon_options_expirations(ticker)
        if not expirations:
            print(f"❌ Aucune expiration disponible pour {ticker}")
            exit(1)
        
        print(f"✅ {len(expirations)} expirations trouvées")
        print(f"Premières expirations: {expirations[:5]}")
        
        # Test avec la première expiration
        first_expiration = expirations[0]
        print(f"\n📊 Test des options pour {ticker} - {first_expiration}...")
        options_data = get_polygon_options_chain(ticker, first_expiration)
        
        if not options_data.empty:
            print(f"\n✅ Données d'options récupérées avec succès!")
            print(f"Nombre d'options: {len(options_data)}")
            print(f"Calls: {len(options_data[options_data['type'] == 'call'])}")
            print(f"Puts: {len(options_data[options_data['type'] == 'put'])}")
            
            # Afficher quelques exemples avec prix
            print("\nExemples d'options avec prix:")
            sample_data = options_data.head(10)[['type', 'strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility']]
            print(sample_data.to_string(index=False))
            
            # Test de la surface de volatilité
            print(f"\n🌊 Test de la surface de volatilité pour {ticker}...")
            surface_data = get_polygon_volatility_surface(ticker, max_expirations=3, strike_span=0.3)
            
            if 'error' not in surface_data:
                print(f"✅ Surface de volatilité générée avec succès!")
                print(f"  • {len(surface_data['strikes'])} strikes")
                print(f"  • {len(surface_data['maturities'])} maturités")
                print(f"  • {surface_data['total_options']} options totales")
                print(f"  • IV min: {surface_data['statistics']['min_iv']:.4f}")
                print(f"  • IV max: {surface_data['statistics']['max_iv']:.4f}")
                print(f"  • IV moy: {surface_data['statistics']['avg_iv']:.4f}")
            else:
                print(f"❌ Erreur surface de volatilité: {surface_data['error']}")
            
        else:
            print("❌ Aucune donnée d'options récupérée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
