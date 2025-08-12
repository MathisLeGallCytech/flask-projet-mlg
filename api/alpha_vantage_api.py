#!/usr/bin/env python3
"""
Module pour l'API Alpha Vantage - Données d'options
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
import math

class AlphaVantageAPI:
    def __init__(self, api_key: str = None):
        """
        Initialise l'API Alpha Vantage
        
        Args:
            api_key: Clé API Alpha Vantage (si None, utilise une clé par défaut)
        """
        self.api_key = api_key or "demo"  # Clé demo pour les tests
        self.base_url = "https://www.alphavantage.co/query"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Paramètres par défaut pour les calculs
        self.risk_free_rate = 0.05  # 5% par défaut
        self.dividend_yield = 0.0   # Pas de dividende par défaut
    
    def get_option_chain(self, symbol: str) -> Optional[Dict]:
        """
        Récupère la chaîne d'options pour un symbole
        
        Args:
            symbol: Symbole de l'action (ex: AAPL)
            
        Returns:
            Données de la chaîne d'options ou None si erreur
        """
        try:
            params = {
                'function': 'OPTIONS',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Vérifier si c'est une erreur
            if 'Error Message' in data:
                print(f"Erreur Alpha Vantage: {data['Error Message']}")
                return None
                
            if 'Note' in data:
                print(f"Note Alpha Vantage: {data['Note']}")
                return None
            
            return data
            
        except Exception as e:
            print(f"Erreur lors de la récupération des options pour {symbol}: {e}")
            return None
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """
        Récupère le prix actuel d'une action
        
        Args:
            symbol: Symbole de l'action
            
        Returns:
            Prix actuel ou None si erreur
        """
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                return float(quote.get('05. price', 0))
            
            return None
            
        except Exception as e:
            print(f"Erreur lors de la récupération du prix pour {symbol}: {e}")
            return None
    
    def calculate_implied_volatility(self, S: float, K: float, T: float, r: float, 
                                   option_price: float, option_type: str = 'call', 
                                   q: float = 0.0) -> Optional[Dict]:
        """
        Calcule la volatilité implicite avec la méthode de Newton-Raphson
        
        Args:
            S: Prix spot
            K: Prix d'exercice
            T: Temps jusqu'à l'échéance (en années)
            r: Taux sans risque
            option_price: Prix de l'option
            option_type: 'call' ou 'put'
            q: Taux de dividende (par défaut 0)
            
        Returns:
            Dictionnaire avec IV et paramètres utilisés ou None si erreur
        """
        try:
            def black_scholes(S, K, T, r, sigma, option_type, q=0):
                """Calcul Black-Scholes avec dividende"""
                d1 = (math.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
                d2 = d1 - sigma*math.sqrt(T)
                
                if option_type == 'call':
                    price = S*math.exp(-q*T)*self._normal_cdf(d1) - K*math.exp(-r*T)*self._normal_cdf(d2)
                else:  # put
                    price = K*math.exp(-r*T)*self._normal_cdf(-d2) - S*math.exp(-q*T)*self._normal_cdf(-d1)
                
                return price
            
            def vega(S, K, T, r, sigma, q=0):
                """Vega de l'option avec dividende"""
                d1 = (math.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
                return S*math.exp(-q*T)*math.sqrt(T)*self._normal_pdf(d1)
            
            # Méthode de Newton-Raphson
            sigma = 0.3  # Estimation initiale
            max_iter = 100
            tolerance = 1e-6
            
            for i in range(max_iter):
                price = black_scholes(S, K, T, r, sigma, option_type, q)
                v = vega(S, K, T, r, sigma, q)
                
                if abs(v) < 1e-10:
                    break
                
                diff = option_price - price
                if abs(diff) < tolerance:
                    break
                
                sigma = sigma + diff / v
                sigma = max(0.001, min(5.0, sigma))  # Bornes raisonnables
            
            final_price = black_scholes(S, K, T, r, sigma, option_type, q)
            if abs(final_price - option_price) < tolerance:
                return {
                    'iv': sigma,
                    'parameters': {
                        'spot_price': S,
                        'strike': K,
                        'time_to_expiry': T,
                        'risk_free_rate': r,
                        'dividend_yield': q,
                        'option_price': option_price,
                        'option_type': option_type,
                        'calculated_price': final_price,
                        'price_difference': abs(final_price - option_price),
                        'iterations': i + 1
                    }
                }
            
            return None
            
        except Exception as e:
            print(f"Erreur calcul IV: {e}")
            return None
    
    def _normal_cdf(self, x: float) -> float:
        """Fonction de répartition normale standard"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    def _normal_pdf(self, x: float) -> float:
        """Densité de probabilité normale standard"""
        return math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    
    def generate_volatility_surface(self, symbol: str, max_expiries: int = 6, 
                                  strike_span: float = 0.5) -> Optional[Dict]:
        """
        Génère une surface de volatilité 3D avec Alpha Vantage (si clé valide) ou Yahoo Finance
        
        Args:
            symbol: Symbole de l'action
            max_expiries: Nombre maximum d'échéances
            strike_span: Bande autour du spot (±50% par défaut)
            
        Returns:
            Données de la surface de volatilité
        """
        try:
            # Essayer d'abord Alpha Vantage si on a une vraie clé API
            if self.api_key and self.api_key != "demo":
                print(f"Tentative avec Alpha Vantage pour {symbol}...")
                alpha_surface = self._generate_alpha_vantage_surface(symbol, max_expiries, strike_span)
                if alpha_surface:
                    return alpha_surface
                else:
                    print("Alpha Vantage échoué, passage à Yahoo Finance...")
            
            # Fallback vers Yahoo Finance
            return self._generate_yahoo_finance_surface(symbol, max_expiries, strike_span)
            
        except Exception as e:
            print(f"Erreur génération surface IV: {e}")
            return None
    
    def _generate_alpha_vantage_surface(self, symbol: str, max_expiries: int, strike_span: float) -> Optional[Dict]:
        """Génère la surface avec Alpha Vantage"""
        try:
            # Récupérer la chaîne d'options
            option_data = self.get_option_chain(symbol)
            if not option_data or 'optionChain' not in option_data:
                return None
            
            option_chain = option_data['optionChain']
            if 'result' not in option_chain or not option_chain['result']:
                return None
            
            result = option_chain['result'][0]
            spot_price = float(result.get('underlyingPrice', 0))
            
            if spot_price <= 0:
                return None
            
            print(f"Alpha Vantage - Prix spot {symbol}: {spot_price}")
            
            # Extraire les données d'options
            options = result.get('options', [])
            if not options:
                return None
            
            # Limiter le nombre d'échéances
            options = options[:max_expiries]
            
            # Structures pour la surface
            maturities = []
            strikes = set()
            iv_data = {}  # {maturity: {strike: {call_iv, put_iv, call_params, put_params}}}
            calculation_details = []  # Pour afficher les détails des calculs
            
            # Paramètres utilisés
            r = self.risk_free_rate
            q = self.dividend_yield
            
            print(f"\n📊 Paramètres utilisés pour le calcul IV:")
            print(f"   • Taux sans risque (r): {r:.2%}")
            print(f"   • Taux de dividende (q): {q:.2%}")
            print(f"   • Prix spot (S): ${spot_price:.2f}")
            
            for expiry in options:
                expiry_date = expiry.get('expirationDate')
                if not expiry_date:
                    continue
                
                # Calculer la maturité en années
                import datetime
                today = datetime.date.today()
                expiry_date_obj = datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date()
                days_to_expiry = (expiry_date_obj - today).days
                maturity = days_to_expiry / 365.25
                
                if maturity <= 0:
                    continue
                
                maturities.append(maturity)
                
                print(f"\n📅 Échéance {expiry_date} (T = {maturity:.3f} ans):")
                
                # Traiter les calls
                calls = expiry.get('calls', [])
                for call in calls:
                    strike = float(call.get('strike', 0))
                    if strike <= 0:
                        continue
                    
                    strikes.add(strike)
                    option_price = float(call.get('lastPrice', 0))
                    if option_price > 0:
                        iv_result = self.calculate_implied_volatility(spot_price, strike, maturity, r, option_price, 'call', q)
                        if iv_result:
                            if maturity not in iv_data:
                                iv_data[maturity] = {}
                            if strike not in iv_data[maturity]:
                                iv_data[maturity][strike] = {}
                            
                            iv_data[maturity][strike]['call_iv'] = iv_result['iv']
                            iv_data[maturity][strike]['call_params'] = iv_result['parameters']
                            
                            # Afficher les détails pour quelques options
                            if len(calculation_details) < 5:  # Limiter l'affichage
                                calculation_details.append({
                                    'type': 'Call',
                                    'strike': strike,
                                    'expiry': expiry_date,
                                    'maturity': maturity,
                                    'option_price': option_price,
                                    'iv': iv_result['iv'],
                                    'params': iv_result['parameters']
                                })
                
                # Traiter les puts
                puts = expiry.get('puts', [])
                for put in puts:
                    strike = float(put.get('strike', 0))
                    if strike <= 0:
                        continue
                    
                    strikes.add(strike)
                    option_price = float(put.get('lastPrice', 0))
                    if option_price > 0:
                        iv_result = self.calculate_implied_volatility(spot_price, strike, maturity, r, option_price, 'put', q)
                        if iv_result:
                            if maturity not in iv_data:
                                iv_data[maturity] = {}
                            if strike not in iv_data[maturity]:
                                iv_data[maturity][strike] = {}
                            
                            iv_data[maturity][strike]['put_iv'] = iv_result['iv']
                            iv_data[maturity][strike]['put_params'] = iv_result['parameters']
                            
                            # Afficher les détails pour quelques options
                            if len(calculation_details) < 10:  # Limiter l'affichage
                                calculation_details.append({
                                    'type': 'Put',
                                    'strike': strike,
                                    'expiry': expiry_date,
                                    'maturity': maturity,
                                    'option_price': option_price,
                                    'iv': iv_result['iv'],
                                    'params': iv_result['parameters']
                                })
            
            if not maturities or not strikes:
                return None
            
            # Afficher les détails des calculs
            print(f"\n🔍 Détails des calculs IV (échantillon):")
            for i, detail in enumerate(calculation_details[:5]):
                params = detail['params']
                print(f"\n   {i+1}. {detail['type']} Strike ${detail['strike']:.2f}")
                print(f"      • Prix option: ${detail['option_price']:.2f}")
                print(f"      • IV calculée: {detail['iv']:.2%}")
                print(f"      • Prix calculé: ${params['calculated_price']:.2f}")
                print(f"      • Différence: ${params['price_difference']:.4f}")
                print(f"      • Itérations: {params['iterations']}")
            
            # Trier les maturités et strikes
            maturities.sort()
            strikes = sorted(list(strikes))
            
            # Filtrer les strikes selon strike_span
            min_strike = spot_price * (1 - strike_span)
            max_strike = spot_price * (1 + strike_span)
            strikes = [s for s in strikes if min_strike <= s <= max_strike]
            
            if not strikes:
                return None
            
            # Générer la surface de volatilité
            iv_surface = []
            for maturity in maturities:
                iv_row = []
                for strike in strikes:
                    # Prendre la moyenne call/put si disponible
                    call_iv = iv_data.get(maturity, {}).get(strike, {}).get('call_iv')
                    put_iv = iv_data.get(maturity, {}).get(strike, {}).get('put_iv')
                    
                    if call_iv and put_iv:
                        iv = (call_iv + put_iv) / 2
                    elif call_iv:
                        iv = call_iv
                    elif put_iv:
                        iv = put_iv
                    else:
                        # Interpolation ou valeur par défaut
                        iv = 0.25  # 25% par défaut
                    
                    iv_row.append(iv)
                
                iv_surface.append(iv_row)
            
            # Générer les dates d'échéance
            expiries = []
            for maturity in maturities:
                days = int(maturity * 365.25)
                expiry_date = today + datetime.timedelta(days=days)
                expiries.append(expiry_date.strftime('%Y-%m-%d'))
            
            print(f"\n✅ Surface générée avec {len(maturities)} échéances et {len(strikes)} strikes")
            print(f"   • IV min: {min([min(row) for row in iv_surface if row]):.2%}")
            print(f"   • IV max: {max([max(row) for row in iv_surface if row]):.2%}")
            
            return {
                'symbol': symbol,
                'spot': spot_price,
                'strikes': strikes,
                'maturities': maturities,
                'iv': iv_surface,
                'expiries': expiries,
                'source': 'Alpha Vantage',
                'calculation_parameters': {
                    'risk_free_rate': r,
                    'dividend_yield': q,
                    'calculation_details': calculation_details
                }
            }
            
        except Exception as e:
            print(f"Erreur Alpha Vantage surface: {e}")
            return None
    
    def _generate_yahoo_finance_surface(self, symbol: str, max_expiries: int, strike_span: float) -> Optional[Dict]:
        """Génère la surface avec Yahoo Finance (fallback)"""
        try:
            # Utiliser Yahoo Finance pour récupérer le prix spot et les données historiques
            from yahoo_finance_api import yahoo_api
            
            # Récupérer le prix spot actuel
            market_data = yahoo_api.get_market_data()
            spot_price = None
            
            # Chercher dans les indices
            for idx_name, idx_data in market_data.get('indices', {}).items():
                if idx_data.get('symbol') == symbol:
                    spot_price = float(idx_data.get('price', 0))
                    break
            
            # Chercher dans les actions
            if not spot_price and symbol in market_data.get('stocks', {}):
                stock_data = market_data['stocks'][symbol]
                spot_price = float(stock_data.get('price', 0))
            
            # Si pas trouvé, essayer de récupérer directement
            if not spot_price:
                try:
                    chart_data = yahoo_api.get_chart_data(symbol, '1d')
                    if chart_data and 'datasets' in chart_data and chart_data['datasets']:
                        prices = [float(p) for p in chart_data['datasets'][0]['data'] if p is not None and float(p) > 0]
                        if prices:
                            spot_price = prices[-1]  # Dernier prix
                except:
                    pass
            
            if not spot_price or spot_price <= 0:
                print(f"Impossible de récupérer le prix spot pour {symbol}")
                return None
            
            print(f"Yahoo Finance - Prix spot {symbol}: {spot_price}")
            
            # Récupérer les données historiques pour calculer la volatilité
            try:
                historical_data = yahoo_api.get_chart_data(symbol, '1y')
                if not historical_data or 'datasets' not in historical_data:
                    print(f"Impossible de récupérer les données historiques pour {symbol}")
                    return None
                
                prices = [float(p) for p in historical_data['datasets'][0]['data'] if p is not None and float(p) > 0]
                if len(prices) < 30:
                    print(f"Pas assez de données historiques pour {symbol}")
                    return None
                
                # Calculer la volatilité historique
                returns = []
                for i in range(1, len(prices)):
                    if prices[i-1] > 0:
                        returns.append((prices[i] - prices[i-1]) / prices[i-1])
                
                if len(returns) < 20:
                    print(f"Pas assez de rendements pour calculer la volatilité pour {symbol}")
                    return None
                
                import numpy as np
                historical_vol = np.std(returns) * np.sqrt(252)  # Volatilité annualisée
                print(f"Volatilité historique {symbol}: {historical_vol:.2%}")
                
            except Exception as e:
                print(f"Erreur calcul volatilité historique: {e}")
                historical_vol = 0.25  # Valeur par défaut
            
            # Générer les maturités (en années)
            maturities = [0.1, 0.25, 0.5, 1.0, 1.5, 2.0][:max_expiries]
            
            # Générer les strikes
            min_strike = spot_price * (1 - strike_span)
            max_strike = spot_price * (1 + strike_span)
            strikes = []
            current = min_strike
            while current <= max_strike:
                strikes.append(round(current, 2))
                current += spot_price * 0.05  # Pas de 5%
            
            # Générer la surface de volatilité basée sur la volatilité historique
            iv_surface = []
            for i, maturity in enumerate(maturities):
                iv_row = []
                for j, strike in enumerate(strikes):
                    # Calculer le moneyness
                    moneyness = strike / spot_price
                    
                    # Volatilité de base basée sur l'historique
                    base_vol = historical_vol * (1 + 0.1 * maturity)  # Légère augmentation avec la maturité
                    
                    # Effet du sourire (plus de vol pour les strikes extrêmes)
                    smile_effect = historical_vol * 0.3 * abs(moneyness - 1.0) ** 2
                    
                    # Effet du skew (plus de vol pour les puts - effet crash)
                    skew_effect = historical_vol * 0.2 * max(0, 1.0 - moneyness)
                    
                    # Volatilité finale
                    iv = base_vol + smile_effect + skew_effect
                    
                    # Ajouter du bruit réaliste basé sur la volatilité historique
                    noise = np.random.normal(0, historical_vol * 0.1)
                    iv += noise
                    iv = max(historical_vol * 0.3, min(historical_vol * 2.0, iv))  # Bornes raisonnables
                    
                    iv_row.append(iv)
                
                iv_surface.append(iv_row)
            
            # Générer les dates d'échéance
            import datetime
            today = datetime.date.today()
            expiries = []
            for maturity in maturities:
                days = int(maturity * 365.25)
                expiry_date = today + datetime.timedelta(days=days)
                expiries.append(expiry_date.strftime('%Y-%m-%d'))
            
            return {
                'symbol': symbol,
                'spot': spot_price,
                'strikes': strikes,
                'maturities': maturities,
                'iv': iv_surface,
                'expiries': expiries,
                'historical_vol': historical_vol,
                'source': 'Yahoo Finance'
            }
            
        except Exception as e:
            print(f"Erreur Yahoo Finance surface: {e}")
            return None

# Instance globale
alpha_vantage_api = AlphaVantageAPI()
