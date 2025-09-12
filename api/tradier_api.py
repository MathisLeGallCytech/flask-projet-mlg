#!/usr/bin/env python3
"""
API Tradier pour la récupération des prix d'options
"""

import requests
import json
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional, Any
import pandas as pd

class TradierAPI:
    """
    Classe pour interagir avec l'API Tradier
    """
    
    def __init__(self, token: str):
        """
        Initialise l'API Tradier avec le token d'authentification
        
        Args:
            token (str): Token d'authentification Tradier
        """
        self.token = token
        self.base_url = "https://api.tradier.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
        """
        Effectue une requête HTTP vers l'API Tradier avec retry automatique
        
        Args:
            endpoint (str): Point de terminaison de l'API
            params (Dict, optional): Paramètres de la requête
            max_retries (int): Nombre maximum de tentatives
            
        Returns:
            Dict: Réponse de l'API ou None en cas d'erreur
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(max_retries + 1):
            try:
                # Timeout plus long pour les connexions lentes
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params=params,
                    timeout=(10, 30)  # (connect_timeout, read_timeout)
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit
                    print(f"⚠️  Rate limit atteint, attente avant retry...")
                    time.sleep(2 ** attempt)  # Backoff exponentiel
                    continue
                else:
                    print(f"❌ Erreur API: {response.status_code} - {response.text}")
                    return None
                    
            except requests.exceptions.ConnectTimeout as e:
                print(f"❌ Timeout de connexion (tentative {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)  # Backoff exponentiel
                    continue
                else:
                    print(f"❌ Impossible de se connecter à Tradier après {max_retries + 1} tentatives")
                    return None
                    
            except requests.exceptions.ConnectionError as e:
                print(f"❌ Erreur de connexion (tentative {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)  # Backoff exponentiel
                    continue
                else:
                    print(f"❌ Impossible de se connecter à Tradier après {max_retries + 1} tentatives")
                    print(f"💡 Vérifiez votre connexion internet et que api.tradier.com est accessible")
                    return None
                    
            except requests.exceptions.Timeout as e:
                print(f"❌ Timeout de lecture (tentative {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur de requête: {e}")
                return None
        
        return None
    
    def get_account_info(self) -> Optional[Dict]:
        """
        Récupère les informations du compte
        
        Returns:
            Dict: Informations du compte ou None en cas d'erreur
        """
        return self._make_request("/user/profile")
    
    def get_market_status(self) -> Optional[Dict]:
        """
        Récupère le statut du marché
        
        Returns:
            Dict: Statut du marché ou None en cas d'erreur
        """
        return self._make_request("/markets/clock")
    
    def get_option_chain(self, symbol: str, expiration: Optional[str] = None) -> Optional[Dict]:
        """
        Récupère la chaîne d'options pour un symbole donné
        
        Args:
            symbol (str): Symbole de l'action (ex: "SPT")
            expiration (str, optional): Date d'expiration au format YYYY-MM-DD
            
        Returns:
            Dict: Chaîne d'options ou None en cas d'erreur
        """
        params = {"symbol": symbol}
        if expiration:
            params["expiration"] = expiration
            
        return self._make_request("/markets/options/chains", params)
    
    def get_option_expirations(self, symbol: str) -> Optional[Dict]:
        """
        Récupère les dates d'expiration disponibles pour un symbole
        
        Args:
            symbol (str): Symbole de l'action (ex: "SPT")
            
        Returns:
            Dict: Dates d'expiration ou None en cas d'erreur
        """
        params = {"symbol": symbol}
        return self._make_request("/markets/options/expirations", params)
    
    def get_option_strikes(self, symbol: str, expiration: str) -> Optional[Dict]:
        """
        Récupère les prix d'exercice disponibles pour un symbole et une expiration
        
        Args:
            symbol (str): Symbole de l'action (ex: "SPT")
            expiration (str): Date d'expiration au format YYYY-MM-DD
            
        Returns:
            Dict: Prix d'exercice ou None en cas d'erreur
        """
        params = {
            "symbol": symbol,
            "expiration": expiration
        }
        return self._make_request("/markets/options/strikes", params)
    
    def search_symbols(self, query: str, indexes: bool = False) -> Optional[Dict]:
        """
        Recherche des symboles basée sur une requête
        
        Args:
            query (str): Terme de recherche (ex: "apple", "AAPL")
            indexes (bool): Inclure les indices dans la recherche
            
        Returns:
            Dict: Résultats de recherche ou None en cas d'erreur
        """
        params = {
            "q": query,
            "indexes": str(indexes).lower()
        }
        return self._make_request("/markets/search", params)
    
    def get_popular_symbols(self) -> List[Dict[str, str]]:
        """
        Retourne une liste des symboles populaires avec options
        
        Returns:
            List[Dict]: Liste des symboles populaires avec nom et symbole
        """
        popular_symbols = [
            {"symbol": "AAPL", "name": "Apple Inc."},
            {"symbol": "MSFT", "name": "Microsoft Corp."},
            {"symbol": "GOOGL", "name": "Alphabet Inc."},
            {"symbol": "AMZN", "name": "Amazon.com Inc."},
            {"symbol": "TSLA", "name": "Tesla Inc."},
            {"symbol": "META", "name": "Meta Platforms Inc."},
            {"symbol": "NVDA", "name": "NVIDIA Corp."},
            {"symbol": "NFLX", "name": "Netflix Inc."},
            {"symbol": "AMD", "name": "Advanced Micro Devices"},
            {"symbol": "INTC", "name": "Intel Corp."},
            {"symbol": "CRM", "name": "Salesforce Inc."},
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF"},
            {"symbol": "QQQ", "name": "Invesco QQQ Trust"},
            {"symbol": "IWM", "name": "iShares Russell 2000 ETF"},
            {"symbol": "VXX", "name": "iPath Series B S&P 500 VIX Short-Term Futures ETN"},
            {"symbol": "VIX", "name": "CBOE Volatility Index"},
            {"symbol": "GLD", "name": "SPDR Gold Trust"},
            {"symbol": "SLV", "name": "iShares Silver Trust"},
            {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond ETF"},
            {"symbol": "HYG", "name": "iShares iBoxx $ High Yield Corporate Bond ETF"}
        ]
        return popular_symbols
    
    def get_option_quotes(self, symbol: str, expiration: str, strike: float, option_type: str = "call") -> Optional[Dict]:
        """
        Récupère les cotations d'options pour des paramètres spécifiques
        
        Args:
            symbol (str): Symbole de l'action (ex: "SPT")
            expiration (str): Date d'expiration au format YYYY-MM-DD
            strike (float): Prix d'exercice
            option_type (str): Type d'option ("call" ou "put")
            
        Returns:
            Dict: Cotations d'options ou None en cas d'erreur
        """
        params = {
            "symbol": symbol,
            "expiration": expiration,
            "strike": strike,
            "greeks": "true"
        }
        
        # Construire le symbole d'option
        option_symbol = f"{symbol}{expiration.replace('-', '')}{option_type.upper()[0]}{int(strike * 1000):08d}"
        params["option_symbol"] = option_symbol
        
        return self._make_request("/markets/quotes", params)
    
    def get_stock_quote(self, symbol: str) -> Optional[Dict]:
        """
        Récupère la cotation d'une action
        
        Args:
            symbol (str): Symbole de l'action (ex: "SPT")
            
        Returns:
            Dict: Cotation de l'action ou None en cas d'erreur
        """
        params = {"symbols": symbol}
        return self._make_request("/markets/quotes", params)
    
    def get_historical_quote(self, symbol: str, date: str) -> Optional[Dict]:
        """
        Récupère les données historiques d'une action pour une date spécifique
        
        Args:
            symbol (str): Symbole de l'action (ex: "AAPL")
            date (str): Date au format YYYY-MM-DD
            
        Returns:
            Dict: Données historiques de l'action ou None en cas d'erreur
        """
        params = {
            "symbol": symbol,
            "start": date,
            "end": date
        }
        return self._make_request("/markets/history", params)
    
    def get_option_quotes_v2(self, symbol: str, expiration: str, strike: float, option_type: str = "call") -> Optional[Dict]:
        """
        Récupère les cotations d'options en utilisant l'endpoint correct de Tradier
        
        Args:
            symbol (str): Symbole de l'action (ex: "AAPL")
            expiration (str): Date d'expiration au format YYYY-MM-DD
            strike (float): Prix d'exercice
            option_type (str): Type d'option ("call" ou "put")
            
        Returns:
            Dict: Cotations d'options ou None en cas d'erreur
        """
        # Utiliser l'endpoint correct pour les options
        endpoint = f"/markets/options/chains"
        params = {
            "symbol": symbol,
            "expiration": expiration,
            "greeks": "true"
        }
        
        return self._make_request(endpoint, params)
    
    def get_historical_options_data(self, symbol: str, expiration: str, date: str = None) -> Optional[pd.DataFrame]:
        """
        Récupère les données historiques d'options pour une maturité donnée
        
        Args:
            symbol (str): Symbole de l'action (ex: "AAPL")
            expiration (str): Date d'expiration au format YYYY-MM-DD
            date (str): Date historique au format YYYY-MM-DD (par défaut: J-1)
            
        Returns:
            pd.DataFrame: DataFrame contenant les données historiques d'options ou None en cas d'erreur
        """
        if date is None:
            # Par défaut, utiliser J-1
            from datetime import datetime, timedelta
            yesterday = datetime.now() - timedelta(days=1)
            date = yesterday.strftime("%Y-%m-%d")
        
        print(f"📅 Récupération des options {symbol} pour l'expiration {expiration} au {date}...")
        
        # Utiliser l'endpoint options/chains avec la date historique
        params = {
            "symbol": symbol,
            "expiration": expiration,
            "date": date,
            "greeks": "true"
        }
        
        chain_data = self._make_request("/markets/options/chains", params)
        if not chain_data or "options" not in chain_data:
            print(f"❌ Impossible de récupérer les données historiques pour {date}")
            return None
        
        options = chain_data["options"]["option"]
        if not options:
            print(f"❌ Aucune option trouvée pour {date}")
            return None
        
        # Convertir en liste si ce n'est pas déjà le cas
        if not isinstance(options, list):
            options = [options]
        
        print(f"✅ {len(options)} options trouvées pour {date}")
        
        # Créer le DataFrame
        all_options_data = []
        for option in options:
            try:
                option_row = {
                    "Symbol": symbol,
                    "Expiration": expiration,
                    "Date_Historique": date,
                    "Strike": float(option.get("strike", 0)),
                    "Type": option.get("option_type", "Unknown").capitalize(),
                    "Bid": option.get("bid", None),
                    "Ask": option.get("ask", None),
                    "Last": option.get("last", None),
                    "Volume": option.get("volume", None),
                    "Open_Interest": option.get("open_interest", None),
                    "Implied_Volatility": option.get("implied_volatility", None),
                    "Delta": option.get("delta", None),
                    "Gamma": option.get("gamma", None),
                    "Theta": option.get("theta", None),
                    "Vega": option.get("vega", None)
                }
                all_options_data.append(option_row)
            except Exception as e:
                print(f"   ⚠️  Erreur lors du traitement d'une option: {e}")
                continue
        
        if not all_options_data:
            print("❌ Aucune donnée d'option valide")
            return None
        
        # Créer le DataFrame
        df = pd.DataFrame(all_options_data)
        
        # Convertir les colonnes numériques
        numeric_columns = ["Bid", "Ask", "Last", "Volume", "Open_Interest", 
                          "Implied_Volatility", "Delta", "Gamma", "Theta", "Vega"]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Trier le DataFrame
        df = df.sort_values(["Strike", "Type"])
        
        print(f"✅ DataFrame historique créé avec {len(df)} lignes d'options")
        return df
    
    def get_multiple_dates_options(self, symbol: str, expiration: str, dates: List[str] = None) -> Optional[pd.DataFrame]:
        """
        Récupère les données d'options pour une maturité sur plusieurs dates historiques
        
        Args:
            symbol (str): Symbole de l'action (ex: "AAPL")
            expiration (str): Date d'expiration au format YYYY-MM-DD
            dates (List[str]): Liste des dates historiques au format YYYY-MM-DD
            
        Returns:
            pd.DataFrame: DataFrame contenant les données d'options sur plusieurs dates ou None en cas d'erreur
        """
        if dates is None:
            # Par défaut, utiliser J-1, J-2, J-3
            from datetime import datetime, timedelta
            today = datetime.now()
            dates = []
            for i in range(1, 4):  # J-1, J-2, J-3
                date = today - timedelta(days=i)
                dates.append(date.strftime("%Y-%m-%d"))
        
        print(f"📅 Récupération des options {symbol} pour l'expiration {expiration} sur {len(dates)} dates...")
        
        all_data = []
        
        for date in dates:
            print(f"   📊 Traitement de la date {date}...")
            
            # Récupérer les données pour cette date
            date_data = self.get_historical_options_data(symbol, expiration, date)
            if date_data is not None:
                all_data.append(date_data)
                print(f"      ✅ {len(date_data)} options récupérées")
            else:
                print(f"      ❌ Échec pour {date}")
            
            # Pause pour éviter de surcharger l'API
            time.sleep(0.5)
        
        if not all_data:
            print("❌ Aucune donnée récupérée")
            return None
        
        # Combiner tous les DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Trier par date historique, puis par strike et type
        combined_df = combined_df.sort_values(["Date_Historique", "Strike", "Type"])
        
        print(f"✅ DataFrame combiné créé avec {len(combined_df)} lignes d'options sur {len(dates)} dates")
        return combined_df
    
    def get_apple_options_dataframe(self, max_expirations: int = 5, max_strikes: int = 10) -> Optional[pd.DataFrame]:
        """
        Récupère les données d'options d'Apple sur plusieurs maturités et strikes
        
        Args:
            max_expirations (int): Nombre maximum de maturités à récupérer
            max_strikes (int): Nombre maximum de strikes par maturité
            
        Returns:
            pd.DataFrame: DataFrame contenant les données d'options ou None en cas d'erreur
        """
        symbol = "AAPL"
        print(f"🍎 Récupération des options {symbol}...")
        
        # Récupérer les expirations disponibles
        expirations = self.get_option_expirations(symbol)
        if not expirations or "expirations" not in expirations:
            print("❌ Impossible de récupérer les expirations")
            return None
            
        exp_list = expirations["expirations"]["date"]
        if not exp_list:
            print("❌ Aucune expiration trouvée")
            return None
        
        # Limiter le nombre d'expirations
        selected_expirations = exp_list[:max_expirations]
        print(f"✅ {len(selected_expirations)} expirations sélectionnées: {selected_expirations}")
        
        all_options_data = []
        
        for expiration in selected_expirations:
            print(f"📅 Traitement de l'expiration {expiration}...")
            
            # Utiliser l'endpoint options/chains qui est plus fiable
            chain_data = self.get_option_chain(symbol, expiration)
            if not chain_data or "options" not in chain_data:
                print(f"   ⚠️  Impossible de récupérer la chaîne d'options pour {expiration}")
                continue
            
            options = chain_data["options"]["option"]
            if not options:
                print(f"   ⚠️  Aucune option trouvée pour {expiration}")
                continue
            
            # Convertir en liste si ce n'est pas déjà le cas
            if not isinstance(options, list):
                options = [options]
            
            # Limiter le nombre d'options
            selected_options = options[:max_strikes * 2]  # *2 car on a Call et Put
            print(f"   💰 {len(selected_options)} options trouvées")
            
            for option in selected_options:
                try:
                    option_row = {
                        "Symbol": symbol,
                        "Expiration": expiration,
                        "Strike": float(option.get("strike", 0)),
                        "Type": option.get("option_type", "Unknown").capitalize(),
                        "Bid": option.get("bid", None),
                        "Ask": option.get("ask", None),
                        "Last": option.get("last", None),
                        "Volume": option.get("volume", None),
                        "Open_Interest": option.get("open_interest", None),
                        "Implied_Volatility": option.get("implied_volatility", None),
                        "Delta": option.get("delta", None),
                        "Gamma": option.get("gamma", None),
                        "Theta": option.get("theta", None),
                        "Vega": option.get("vega", None)
                    }
                    all_options_data.append(option_row)
                except Exception as e:
                    print(f"   ⚠️  Erreur lors du traitement d'une option: {e}")
                    continue
            
            # Petite pause pour éviter de surcharger l'API
            time.sleep(0.2)
        
        if not all_options_data:
            print("❌ Aucune donnée d'option récupérée")
            return None
        
        # Créer le DataFrame
        df = pd.DataFrame(all_options_data)
        
        # Convertir les colonnes numériques
        numeric_columns = ["Bid", "Ask", "Last", "Volume", "Open_Interest", 
                          "Implied_Volatility", "Delta", "Gamma", "Theta", "Vega"]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Trier le DataFrame
        df = df.sort_values(["Expiration", "Strike", "Type"])
        
        print(f"✅ DataFrame créé avec {len(df)} lignes d'options")
        return df


def main():
    """
    Fonction principale pour tester l'API Tradier
    """
    # Token d'authentification depuis les variables d'environnement
    from .tradier_config import TRADIER_API_KEY
    TOKEN = TRADIER_API_KEY
    
    # Initialiser l'API
    api = TradierAPI(TOKEN)
    
    print("🔗 Test de connexion à l'API Tradier...")
    print("=" * 50)
    
    # Test 1: Informations du compte
    print("\n1️⃣ Test des informations du compte:")
    account_info = api.get_account_info()
    if account_info:
        print("✅ Connexion réussie!")
        if "profile" in account_info:
            profile = account_info["profile"]
            print(f"   Compte: {profile.get('name', 'N/A')}")
            print(f"   ID: {profile.get('id', 'N/A')}")
    else:
        print("❌ Échec de la connexion")
    
    # Test 2: Statut du marché
    print("\n2️⃣ Test du statut du marché:")
    market_status = api.get_market_status()
    if market_status:
        print("✅ Statut du marché récupéré!")
        if "clock" in market_status:
            clock = market_status["clock"]
            print(f"   État: {clock.get('state', 'N/A')}")
            print(f"   Heure: {clock.get('next_open', 'N/A')}")
    else:
        print("❌ Impossible de récupérer le statut du marché")
    
    # Test 3: Récupération des options Apple
    print("\n3️⃣ 🍎 Récupération des options Apple:")
    print("   Récupération de 3 maturités avec 5 strikes chacune...")
    
    apple_options_df = api.get_apple_options_dataframe(max_expirations=3, max_strikes=5)
    
    if apple_options_df is not None:
        print("\n📊 DataFrame des options Apple créé avec succès!")
        print(f"   Dimensions: {apple_options_df.shape[0]} lignes x {apple_options_df.shape[1]} colonnes")
        
        # Afficher les premières lignes
        print("\n🔍 Aperçu du DataFrame:")
        print(apple_options_df.head(10))
        
        # Afficher les informations sur le DataFrame
        print("\n📈 Informations sur le DataFrame:")
        print(f"   Colonnes: {list(apple_options_df.columns)}")
        print(f"   Types de données: {apple_options_df.dtypes.to_dict()}")
        
        # Statistiques par expiration
        print("\n📅 Répartition par expiration:")
        expiration_counts = apple_options_df.groupby('Expiration').size()
        print(expiration_counts)
        
        # Statistiques par type d'option
        print("\n📊 Répartition par type d'option:")
        type_counts = apple_options_df.groupby('Type').size()
        print(type_counts)
        
        # Sauvegarder le DataFrame en CSV dans le dossier data_exports
        import os
        os.makedirs("data_exports", exist_ok=True)
        csv_filename = f"data_exports/apple_options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        apple_options_df.to_csv(csv_filename, index=False)
        print(f"\n💾 DataFrame sauvegardé dans: {csv_filename}")
        
    else:
        print("❌ Échec de la récupération des options Apple")
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé!")


def get_apple_options_simple():
    """
    Fonction simple pour récupérer les options Apple et retourner le DataFrame
    """
    TOKEN = TRADIER_API_KEY
    api = TradierAPI(TOKEN)
    
    print("🍎 Récupération des options Apple...")
    df = api.get_apple_options_dataframe(max_expirations=5, max_strikes=8)
    
    if df is not None:
        print(f"✅ {len(df)} options récupérées avec succès!")
        return df
    else:
        print("❌ Échec de la récupération")
        return None

def get_apple_options_j1():
    """
    Fonction simple pour récupérer les options Apple de J-1
    """
    TOKEN = TRADIER_API_KEY
    api = TradierAPI(TOKEN)
    
    print("🍎 Récupération des options Apple de J-1...")
    
    # Récupérer les expirations
    expirations = api.get_option_expirations("AAPL")
    if not expirations or "expirations" not in expirations:
        print("❌ Impossible de récupérer les expirations")
        return None
    
    exp_list = expirations["expirations"]["date"]
    if not exp_list:
        print("❌ Aucune expiration trouvée")
        return None
    
    # Prendre la première expiration
    first_exp = exp_list[0]
    print(f"   Expiration: {first_exp}")
    
    # Récupérer les données J-1
    df = api.get_historical_options_data("AAPL", first_exp)
    
    if df is not None:
        print(f"✅ {len(df)} options J-1 récupérées avec succès!")
        return df
    else:
        print("❌ Échec de la récupération J-1")
        return None

def get_aapl_historical_iv30_parallel(days_back: int = 365, max_workers: int = 5) -> Optional[pd.DataFrame]:
    """
    Récupère les données d'historique IV30 (volatilité implicite 30 jours) pour AAPL en parallèle
    Calcule la volatilité implicite à partir des prix des options car Tradier ne la fournit pas
    
    Args:
        days_back (int): Nombre de jours en arrière à récupérer (par défaut: 365)
        max_workers (int): Nombre maximum de workers parallèles (par défaut: 5)
        
    Returns:
        pd.DataFrame: DataFrame contenant les données IV30 historiques ou None en cas d'erreur
    """
    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    TOKEN = TRADIER_API_KEY
    
    print(f"🍎 Récupération PARALLÈLE des données IV30 historiques AAPL sur {days_back} jours...")
    print(f"   🚀 Utilisation de {max_workers} workers parallèles")
    
    # Récupérer les expirations disponibles (une seule fois)
    api = TradierAPI(TOKEN)
    expirations = api.get_option_expirations("AAPL")
    if not expirations or "expirations" not in expirations:
        print("❌ Impossible de récupérer les expirations")
        return None
    
    exp_list = expirations["expirations"]["date"]
    if not exp_list:
        print("❌ Aucune expiration trouvée")
        return None
    
    # Trouver l'expiration la plus proche de 30 jours
    from datetime import datetime, timedelta
    today = datetime.now()
    target_date = today + timedelta(days=30)
    
    best_expiration = None
    min_diff = float('inf')
    
    for exp_date_str in exp_list:
        try:
            exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
            diff = abs((exp_date - today).days - 30)
            if diff < min_diff:
                min_diff = diff
                best_expiration = exp_date_str
        except ValueError:
            continue
    
    if not best_expiration:
        print("❌ Aucune expiration proche de 30 jours trouvée")
        return None
    
    print(f"   📅 Expiration sélectionnée: {best_expiration} (écart: {min_diff} jours)")
    
    # Générer les dates historiques
    historical_dates = []
    for i in range(1, days_back + 1):
        date = today - timedelta(days=i)
        # Vérifier que ce n'est pas un weekend
        if date.weekday() < 5:  # 0-4 = Lundi-Vendredi
            historical_dates.append(date.strftime("%Y-%m-%d"))
    
    print(f"   📊 {len(historical_dates)} dates de marché à traiter")
    
    # Fonction pour traiter une date individuelle
    def process_single_date(date_str):
        """Traite une seule date et retourne les données IV30"""
        try:
            # Créer une nouvelle instance d'API pour chaque thread
            thread_api = TradierAPI(TOKEN)
            
            # Récupérer les données d'options pour cette date
            options_data = thread_api.get_historical_options_data("AAPL", best_expiration, date_str)
            
            if options_data is not None and not options_data.empty:
                # Récupérer le prix spot historique pour cette date spécifique
                spot_price = None
                try:
                    # Essayer de récupérer le prix historique pour cette date
                    historical_quote = thread_api.get_historical_quote("AAPL", date_str)
                    if historical_quote and "history" in historical_quote and "day" in historical_quote["history"]:
                        day_data = historical_quote["history"]["day"]
                        if isinstance(day_data, list) and len(day_data) > 0:
                            # Prendre le premier jour (le plus proche de la date demandée)
                            spot_price = float(day_data[0].get("close", 0))
                        elif isinstance(day_data, dict):
                            spot_price = float(day_data.get("close", 0))
                    
                    # Validation du prix spot (AAPL devrait être entre 200-300$ récemment)
                    if spot_price and (spot_price < 150 or spot_price > 350):
                        print(f"      ⚠️  Prix spot suspect pour {date_str}: ${spot_price:.2f}")
                        # Utiliser le prix actuel comme fallback
                        stock_quote = thread_api.get_stock_quote("AAPL")
                        if stock_quote and "quotes" in stock_quote and "quote" in stock_quote["quotes"]:
                            quote_data = stock_quote["quotes"]["quote"]
                            if isinstance(quote_data, list):
                                quote_data = quote_data[0]
                            spot_price = float(quote_data.get("last", 0))
                            print(f"      🔄 Utilisation du prix actuel: ${spot_price:.2f}")
                            
                except Exception as e:
                    print(f"      ❌ Erreur récupération prix historique {date_str}: {e}")
                    # Si échec, utiliser le prix actuel comme fallback
                    stock_quote = thread_api.get_stock_quote("AAPL")
                    if stock_quote and "quotes" in stock_quote and "quote" in stock_quote["quotes"]:
                        quote_data = stock_quote["quotes"]["quote"]
                        if isinstance(quote_data, list):
                            quote_data = quote_data[0]
                        spot_price = float(quote_data.get("last", 0))
                
                if spot_price and spot_price > 0:
                    # Filtrer les options ATM (At The Money) - proches du prix spot
                    # Utiliser une plage plus large pour avoir plus d'options
                    atm_options = options_data[
                        (options_data['Strike'] >= spot_price * 0.90) & 
                        (options_data['Strike'] <= spot_price * 1.10)
                    ]
                    
                    if not atm_options.empty:
                        # Calculer la volatilité implicite à partir des prix des options
                        calculated_ivs = []
                        
                        for _, option in atm_options.iterrows():
                            try:
                                # Utiliser le prix moyen bid-ask ou le dernier prix
                                option_price = None
                                if pd.notna(option['Last']) and option['Last'] > 0:
                                    option_price = option['Last']
                                elif pd.notna(option['Bid']) and pd.notna(option['Ask']) and option['Bid'] > 0 and option['Ask'] > 0:
                                    option_price = (option['Bid'] + option['Ask']) / 2
                                
                                if option_price and option_price > 0:
                                    # Calculer le temps jusqu'à l'expiration
                                    exp_date = datetime.strptime(best_expiration, "%Y-%m-%d")
                                    hist_date = datetime.strptime(date_str, "%Y-%m-%d")
                                    time_to_exp = (exp_date - hist_date).days / 365.25
                                    
                                    if time_to_exp > 0:
                                        # Calculer la volatilité implicite avec Black-Scholes
                                        iv = calculate_implied_volatility(
                                            spot_price=spot_price,
                                            strike=option['Strike'],
                                            time_to_exp=time_to_exp,
                                            option_price=option_price,
                                            option_type=option['Type'].lower(),
                                            risk_free_rate=0.05  # Taux sans risque approximatif
                                        )
                                        
                                        # Filtrer les valeurs aberrantes plus strictement
                                        if iv and 0.05 < iv < 1.0:  # IV entre 5% et 100%
                                            calculated_ivs.append(iv)
                                            
                            except Exception:
                                continue
                        
                        if calculated_ivs and len(calculated_ivs) >= 3:  # Au moins 3 IV valides
                            avg_iv = sum(calculated_ivs) / len(calculated_ivs)
                            
                            # Validation supplémentaire de la cohérence
                            iv_std = (sum((iv - avg_iv)**2 for iv in calculated_ivs) / len(calculated_ivs))**0.5
                            
                            # Si l'écart-type est trop élevé, filtrer les valeurs extrêmes
                            if iv_std > 0.2:  # Écart-type > 20%
                                filtered_ivs = [iv for iv in calculated_ivs if abs(iv - avg_iv) <= 2 * iv_std]
                                if len(filtered_ivs) >= 3:
                                    avg_iv = sum(filtered_ivs) / len(filtered_ivs)
                                    calculated_ivs = filtered_ivs
                            
                            return {
                                'Date': date_str,
                                'Expiration': best_expiration,
                                'Days_to_Exp': (datetime.strptime(best_expiration, "%Y-%m-%d") - datetime.strptime(date_str, "%Y-%m-%d")).days,
                                'Spot_Price': spot_price,
                                'ATM_Options_Count': len(atm_options),
                                'Valid_IV_Count': len(calculated_ivs),
                                'IV30': avg_iv
                            }
            
            return None
            
        except Exception as e:
            print(f"      ❌ Erreur pour {date_str}: {e}")
            return None
    
    # Traitement parallèle des dates
    all_iv_data = []
    completed_count = 0
    
    print(f"   🚀 Démarrage du traitement parallèle...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Soumettre toutes les tâches
        future_to_date = {executor.submit(process_single_date, date): date for date in historical_dates}
        
        # Traiter les résultats au fur et à mesure
        for future in as_completed(future_to_date):
            date = future_to_date[future]
            completed_count += 1
            
            try:
                result = future.result()
                if result:
                    all_iv_data.append(result)
                    print(f"      ✅ [{completed_count}/{len(historical_dates)}] {date}: IV30 = {result['IV30']:.4f}")
                else:
                    print(f"      ⚠️  [{completed_count}/{len(historical_dates)}] {date}: Aucune donnée")
                    
            except Exception as e:
                print(f"      ❌ [{completed_count}/{len(historical_dates)}] {date}: Erreur - {e}")
            
            # Afficher le progrès
            if completed_count % 10 == 0 or completed_count == len(historical_dates):
                elapsed = time.time() - start_time
                rate = completed_count / elapsed if elapsed > 0 else 0
                eta = (len(historical_dates) - completed_count) / rate if rate > 0 else 0
                print(f"   📊 Progrès: {completed_count}/{len(historical_dates)} ({completed_count/len(historical_dates)*100:.1f}%) - ETA: {eta:.1f}s")
    
    total_time = time.time() - start_time
    print(f"   ⏱️  Traitement terminé en {total_time:.1f} secondes")
    
    if not all_iv_data:
        print("❌ Aucune donnée IV30 récupérée")
        return None
    
    # Créer le DataFrame
    df = pd.DataFrame(all_iv_data)
    
    # Trier par date
    df = df.sort_values('Date')
    
    # Convertir les colonnes numériques
    df['IV30'] = pd.to_numeric(df['IV30'], errors='coerce')
    df['Days_to_Exp'] = pd.to_numeric(df['Days_to_Exp'], errors='coerce')
    df['Spot_Price'] = pd.to_numeric(df['Spot_Price'], errors='coerce')
    
    print(f"✅ DataFrame IV30 créé avec {len(df)} points de données")
    print(f"   📊 Période: {df['Date'].min()} à {df['Date'].max()}")
    print(f"   📈 IV30 moyenne: {df['IV30'].mean():.4f}")
    print(f"   📊 IV30 min/max: {df['IV30'].min():.4f} / {df['IV30'].max():.4f}")
    print(f"   ⚡ Vitesse: {len(df)/total_time:.1f} points/seconde")
    
    return df

def get_aapl_historical_iv30(days_back: int = 30) -> Optional[pd.DataFrame]:
    """
    Version séquentielle (pour compatibilité)
    """
    return get_aapl_historical_iv30_parallel(days_back, max_workers=1)

def calculate_implied_volatility(spot_price: float, strike: float, time_to_exp: float, 
                                option_price: float, option_type: str, risk_free_rate: float = 0.05) -> Optional[float]:
    """
    Calcule la volatilité implicite d'une option en utilisant la méthode de Newton-Raphson
    avec le modèle de Black-Scholes
    
    Args:
        spot_price (float): Prix actuel de l'actif sous-jacent
        strike (float): Prix d'exercice de l'option
        time_to_exp (float): Temps jusqu'à l'expiration en années
        option_price (float): Prix observé de l'option
        option_type (str): Type d'option ("call" ou "put")
        risk_free_rate (float): Taux sans risque (par défaut: 5%)
        
    Returns:
        float: Volatilité implicite ou None si le calcul échoue
    """
    import math
    
    try:
        # Fonction de distribution normale cumulative (approximation)
        def norm_cdf(x):
            return 0.5 * (1 + math.erf(x / math.sqrt(2)))
        
        # Fonction de densité de probabilité normale
        def norm_pdf(x):
            return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
        
        # Fonction Black-Scholes
        def black_scholes_price(S, K, T, r, sigma, option_type):
            if T <= 0:
                return max(S - K, 0) if option_type == "call" else max(K - S, 0)
            
            d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
            d2 = d1 - sigma * math.sqrt(T)
            
            if option_type == "call":
                return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
            else:  # put
                return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        
        # Fonction de vega (dérivée du prix par rapport à la volatilité)
        def vega(S, K, T, r, sigma):
            if T <= 0:
                return 0
            d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
            return S * math.sqrt(T) * norm_pdf(d1)
        
        # Méthode de Newton-Raphson pour trouver la volatilité implicite
        sigma = 0.2  # Estimation initiale
        tolerance = 1e-6
        max_iterations = 100
        
        for i in range(max_iterations):
            try:
                price = black_scholes_price(spot_price, strike, time_to_exp, risk_free_rate, sigma, option_type)
                vega_val = vega(spot_price, strike, time_to_exp, risk_free_rate, sigma)
                
                if vega_val == 0:
                    break
                
                diff = price - option_price
                if abs(diff) < tolerance:
                    return sigma
                
                sigma = sigma - diff / vega_val
                
                # S'assurer que la volatilité reste dans des limites raisonnables
                sigma = max(0.001, min(2.0, sigma))
                
            except (ValueError, ZeroDivisionError, OverflowError):
                break
        
        return None
        
    except Exception:
        return None


if __name__ == "__main__":
    main()
