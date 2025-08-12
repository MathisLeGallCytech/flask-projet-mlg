import requests
import json
import time
from datetime import datetime, timedelta
import random

class YahooFinanceAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Optimisations pour la vitesse
        self.session.mount('https://', requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=1
        ))
        
        # Symboles des indices et actions
        self.indices = {
            'CAC40': '^FCHI',
            'S&P500': '^GSPC', 
            'NASDAQ': '^IXIC',
            'DowJones': '^DJI',
            'FTSE100': '^FTSE',
            'NIKKEI': '^N225',
            'DAX': '^GDAXI',
            'STOXX50': '^STOXX50E'
        }
        
        self.stocks = {
            # Tech US (les plus importantes)
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'NVDA': 'NVIDIA Corporation',
            'META': 'Meta Platforms Inc.',
            'NFLX': 'Netflix Inc.',
            'ADBE': 'Adobe Inc.',
            'CRM': 'Salesforce Inc.',
            'INTC': 'Intel Corporation',
            'ORCL': 'Oracle Corporation',
            'CSCO': 'Cisco Systems Inc.',
            'PYPL': 'PayPal Holdings Inc.',
            'AVGO': 'Broadcom Inc.',
            
            # 4 plus grosses du CAC40
            'LVMH.PA': 'LVMH Moët Hennessy Louis Vuitton',
            'ASML.AS': 'ASML Holding N.V.',
            'SAP.DE': 'SAP SE',
            'NESN.SW': 'Nestlé S.A.',
            
            # Actions asiatiques importantes
            '005930.KS': 'Samsung Electronics Co., Ltd.',
            '0700.HK': 'Tencent Holdings Limited',
            
            # Actions européennes importantes
            'AIR.PA': 'Airbus SE',
            'BAYN.DE': 'Bayer AG',
            'BA': 'The Boeing Company',
        }

    def get_quote(self, symbol):
        """Récupère les données de cotation pour un symbole"""
        try:
            # URL de l'API Yahoo Finance
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            
            params = {
                'range': '1d',
                'interval': '1m',
                'includePrePost': 'false',
                'events': 'div,split'
            }
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                
                # Extraire les données
                meta = result.get('meta', {})
                timestamp = result.get('timestamp', [])
                indicators = result.get('indicators', {})
                quote = indicators.get('quote', [{}])[0]
                
                if timestamp and quote.get('close'):
                    current_price = quote['close'][-1]
                    previous_close = meta.get('previousClose', current_price)
                    
                    if current_price and previous_close:
                        change = current_price - previous_close
                        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                        
                        return {
                            'price': current_price,
                            'change': change,
                            'change_percent': change_percent,
                            'volume': quote.get('volume', [0])[-1] if quote.get('volume') else 0,
                            'previous_close': previous_close
                        }
            
            return None
            
        except Exception as e:
            return None

    def get_market_data(self):
        """Récupère les données de marché pour tous les indices et actions"""
        market_data = {
            'indices': {},
            'stocks': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Récupérer les indices en parallèle
        import concurrent.futures
        
        def fetch_quote(symbol, name, is_index=True):
            quote = self.get_quote(symbol)
            if quote:
                if is_index:
                    return ('indices', name, {
                        'symbol': symbol,
                        'name': name,
                        'displayName': name,
                        'price': quote['price'],
                        'change': quote['change'],
                        'change_percent': quote['change_percent'],
                        'volume': quote['volume']
                    })
                else:
                    return ('stocks', symbol, {
                        'symbol': symbol,
                        'name': name,
                        'price': quote['price'],
                        'change': quote['change'],
                        'change_percent': quote['change_percent'],
                        'volume': quote['volume']
                    })
            return None
        
        # Récupération parallèle avec ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Soumettre toutes les tâches
            futures = []
            
            # Indices
            for name, symbol in self.indices.items():
                futures.append(executor.submit(fetch_quote, symbol, name, True))
            
            # Actions
            for symbol, name in self.stocks.items():
                futures.append(executor.submit(fetch_quote, symbol, name, False))
            
            # Collecter les résultats
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    category, key, data = result
                    market_data[category][key] = data
        
        return market_data

    def get_chart_data(self, symbol, timeframe="1mo", start=None, end=None):
        """Récupère les données de graphique pour un symbole"""
        try:
            # Si start et end sont fournis, utiliser period1 et period2
            if start and end:
                try:
                    # Convertir les dates en timestamps Unix
                    start_dt = datetime.strptime(start, '%Y-%m-%d')
                    end_dt = datetime.strptime(end, '%Y-%m-%d')
                    period1 = int(start_dt.timestamp())
                    period2 = int(end_dt.timestamp())
                    
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    params = {
                        'period1': period1,
                        'period2': period2,
                        'interval': '1d',
                        'includePrePost': 'false',
                        'events': 'div,split'
                    }
                except ValueError:
                    # Si les dates ne sont pas au bon format, utiliser le timeframe par défaut
                    pass
            else:
                # Mapping des timeframes
                range_mapping = {
                    "1d": "1d",
                    "5d": "5d", 
                    "1mo": "1mo",
                    "3mo": "3mo",
                    "6mo": "6mo",
                    "1y": "1y",
                    "2y": "2y",
                    "5y": "5y",
                    "max": "max"
                }
                
                interval_mapping = {
                    "1d": "1m",
                    "5d": "5m",
                    "1mo": "1d",
                    "3mo": "1d",
                    "6mo": "1d",
                    "1y": "1d",
                    "2y": "1d",
                    "5y": "1d",
                    "max": "1d"
                }
                
                range_param = range_mapping.get(timeframe, "1mo")
                interval_param = interval_mapping.get(timeframe, "1d")
                
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                params = {
                    'range': range_param,
                    'interval': interval_param,
                    'includePrePost': 'false',
                    'events': 'div,split'
                }
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                
                timestamp = result.get('timestamp', [])
                indicators = result.get('indicators', {})
                quote = indicators.get('quote', [{}])[0]
                close_prices = quote.get('close', [])
                
                if timestamp and close_prices:
                    # Convertir les timestamps en dates
                    dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamp]
                    
                    # Filtrer les valeurs None
                    valid_data = [(date, price) for date, price in zip(dates, close_prices) if price is not None]
                    
                    if valid_data:
                        dates, prices = zip(*valid_data)
                        
                        return {
                            'labels': list(dates),
                            'datasets': [{
                                'label': symbol,
                                'data': list(prices),
                                'borderColor': 'rgb(75, 192, 192)',
                                'backgroundColor': 'rgba(25, 118, 210, 0.3)',
                                'fill': True,
                                'tension': 0.1
                            }]
                        }
            
            return None
            
        except Exception as e:
            return None

# Instance globale
yahoo_api = YahooFinanceAPI()
