import os
from flask import Flask, render_template, request, jsonify, send_file, Response
import math
import time
import pandas as pd
from datetime import datetime
from models.options_pricing import OptionPricer
from models.risk_metrics import risk_calculator

# Import du nouveau module Yahoo Finance API
from api.yahoo_finance_api import yahoo_api

# Import du module Finnhub pour la volatilité implicite
from api.finnhub_implied_volatility import get_implied_volatility, get_options_expirations

app = Flask(__name__)
pricer = OptionPricer()

# Approximation rationnelle d'Acklam pour l'inverse de la CDF normale (PPF)
# Source adaptée: https://web.archive.org/web/20151030215612/http://home.online.no/~pjacklam/notes/invnorm/
def _inv_norm_cdf(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p doit être dans (0,1)")

    # Coefficients pour approximation par morceaux
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00,
    ]

    plow = 0.02425
    phigh = 1 - plow

    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    elif phigh < p:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    else:
        q = p - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
        ) / (
            ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1
        )


def _z_from_confidence(conf_level: float) -> float:
    # conf_level dans (0,1), par défaut 0.95
    cl = max(0.5, min(0.999, float(conf_level)))
    tail = 1.0 - (1.0 - cl) / 2.0
    return abs(_inv_norm_cdf(tail))

@app.route('/')
def index():
    """Page d'accueil du dashboard"""
    return render_template('index.html')

@app.route('/cv-mathis-le-gall')
def cv_mathis_le_gall():
    """Page CV Mathis Le Gall"""
    return render_template('cv_mathis_le_gall.html')

@app.route('/indices-actions')
def indices_actions():
    """Page des indices et actions"""
    return render_template('indices_actions.html')

@app.route('/call-put')
def call_put():
    """Page Call & Put"""
    return render_template('call_put.html')



@app.route('/volatility-surface')
def volatility_surface():
    """Page de la surface de volatilité"""
    return render_template('volatility_surface.html')

@app.route('/force-refresh')
def force_refresh():
    """Page pour forcer le rafraîchissement"""
    return render_template('force_refresh.html')

@app.route('/test-vol-surface')
def test_vol_surface():
    """Page de test pour debug de la surface de volatilité"""
    return send_file('test_vol_surface_debug.html')

@app.route('/debug-finnhub')
def debug_finnhub():
    """Page de débogage pour l'API Finnhub"""
    return render_template('debug_finnhub.html')

@app.route('/debug-polygon')
def debug_polygon():
    """Page de débogage pour l'API Polygon.io"""
    return render_template('debug_polygon.html')

@app.route('/test-indices-actions')
def test_indices_actions():
    """Page de test pour les indices et actions"""
    return send_file('test_indices_actions.html')



@app.route('/analyse-actions-indices')
def analyse_actions_indices():
    """Page dédiée: comparaison de performances (Base 100)"""
    return render_template('analyse_actions_indices.html')

@app.route('/description-app')
def description_app():
    """Page de description de l'application"""
    return render_template('description_app.html')

@app.route('/analyse-greeks')
def analyse_greeks():
    """Page d'analyse des grecques"""
    return render_template('analyse_greeks.html')

# APIs pour les données financières
@app.route('/api/market-data')
def api_market_data():
    """API pour récupérer les données de marché"""
    try:
        # Utiliser le nouveau module Yahoo Finance API
        data = yahoo_api.get_market_data()
        
        if data and (data.get('indices') or data.get('stocks')):
            return jsonify(data)
        else:
            return jsonify({
                'error': 'Impossible de récupérer les données via Yahoo Finance.',
                'indices': {},
                'stocks': {},
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart-data/<path:symbol>')
def api_chart_data_legacy(symbol):
    """API pour récupérer les données de graphique (route legacy)"""
    return api_chart_data_v2(symbol)

@app.route('/api/chart-data-v2/<path:symbol>')
def api_chart_data_v2(symbol):
    """API pour récupérer les données de graphique avec timeframe"""
    try:
        # Récupérer le timeframe depuis les paramètres de requête
        timeframe = request.args.get('timeframe', '1mo')
        start = request.args.get('start')  # YYYY-MM-DD
        end = request.args.get('end')      # YYYY-MM-DD
        
        # Utiliser le nouveau module Yahoo Finance API
        test_data = yahoo_api.get_chart_data(symbol, timeframe, start, end)
        
        if test_data:
            return jsonify(test_data)
        else:
            return jsonify({
                'error': f'Impossible de récupérer les données pour {symbol}.',
                'labels': [],
                'datasets': []
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: surface de volatilité implicite
@app.route('/api/vol-surface/<symbol>')
def api_vol_surface(symbol):
    """API endpoint pour récupérer les données de volatilité surface via Finnhub ou Polygon.io"""
    try:
        max_exp = int(request.args.get('maxExp', 6))
        span = float(request.args.get('span', 0.5))
        provider = request.args.get('provider', 'finnhub')  # 'finnhub' ou 'polygon'
        
        # Validation des paramètres
        if max_exp < 1 or max_exp > 12:
            return jsonify({'error': 'maxExp doit être entre 1 et 12'}), 400
            
        if span <= 0 or span > 1:
            return jsonify({'error': 'span doit être entre 0 et 1'}), 400
            
        if provider not in ['finnhub', 'polygon']:
            return jsonify({'error': 'provider doit être "finnhub" ou "polygon"'}), 400
        
        # Choisir le provider
        if provider == 'polygon':
            print(f"🔵 Utilisation de Polygon.io pour {symbol}")
            from api.polygon_options_api import get_polygon_volatility_surface
            result = get_polygon_volatility_surface(symbol, max_exp, span)
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 404
            
            return jsonify(result)
        
        else:  # provider == 'finnhub' (par défaut)
            print(f"🔴 Utilisation de Finnhub pour {symbol}")
            # Utiliser l'API Finnhub pour les vraies données d'options
            from api.finnhub_implied_volatility import get_options_expirations, get_implied_volatility
            
            # Récupérer les dates d'expiration disponibles
            print(f"🔍 Récupération des expirations pour {symbol}...")
            expirations = get_options_expirations(symbol)
            print(f"📅 Expirations reçues: {expirations}")
        
        if not expirations:
            print(f"❌ Aucune expiration trouvée pour {symbol}")
            return jsonify({
                'error': f'Aucune date d\'expiration disponible pour {symbol}'
            }), 404
        
        # Limiter le nombre d'expirations selon maxExp
        expirations_to_use = expirations[:max_exp]
        
        # Récupérer le prix spot actuel
        try:
            import requests
            from api.finnhub_config import FINNHUB_API_KEY, FINNHUB_BASE_URL
            
            url = f"{FINNHUB_BASE_URL}/quote"
            params = {
                'symbol': symbol,
                'token': FINNHUB_API_KEY
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            quote_data = response.json()
            spot_price = float(quote_data.get('c', 0))  # Prix de clôture actuel
        except:
            spot_price = 0
        
        # Collecter toutes les données d'options pour toutes les expirations
        all_options_data = []
        
        print(f"Test de {len(expirations_to_use)} expirations pour {symbol}")
        
        for expiration_timestamp in expirations_to_use:
            try:
                # expiration_timestamp est déjà un timestamp UNIX
                expiration_date = datetime.fromtimestamp(expiration_timestamp).strftime('%Y-%m-%d')
                
                print(f"Récupération des options pour {expiration_date}...")
                
                # Récupérer les données d'options pour cette expiration
                options_data = get_implied_volatility(symbol, expiration_timestamp)
                
                if not options_data.empty:
                    print(f"✅ {len(options_data)} options trouvées pour {expiration_date}")
                    # Ajouter la date d'expiration à chaque option
                    options_data['expiration_date'] = expiration_date
                    all_options_data.append(options_data)
                else:
                    print(f"❌ Aucune option pour {expiration_date}")
                    
            except Exception as e:
                print(f"Erreur pour l'expiration {expiration_date}: {e}")
                continue
        
        print(f"Total d'expirations avec données: {len(all_options_data)}")
        
        if not all_options_data:
            print(f"❌ Aucune donnée d'options collectée pour {symbol}")
            return jsonify({
                'error': f'Aucune option disponible pour {symbol}'
            }), 404
        
        # Combiner toutes les données
        combined_data = pd.concat(all_options_data, ignore_index=True)
        
        # Filtrer par bande autour du spot si le prix spot est disponible
        if spot_price > 0:
            min_strike = spot_price * (1 - span)
            max_strike = spot_price * (1 + span)
            filtered_data = combined_data[
                (combined_data['strike'] >= min_strike) & 
                (combined_data['strike'] <= max_strike)
            ]
            
            # Si le filtrage supprime trop de données, utiliser toutes les données
            if len(filtered_data) < 10:
                print(f"Filtrage trop restrictif, utilisation de toutes les données ({len(combined_data)} options)")
                combined_data = combined_data
            else:
                combined_data = filtered_data
        else:
            print(f"Prix spot non disponible, utilisation de toutes les données ({len(combined_data)} options)")
        
        if combined_data.empty:
            return jsonify({
                'error': f'Aucune option disponible pour {symbol}'
            }), 404
        
        # Organiser les données pour la surface de volatilité
        # Extraire les strikes et expirations uniques
        unique_strikes = sorted(combined_data['strike'].unique())
        unique_expirations = sorted(combined_data['expiration_date'].unique())
        
        # Calculer les maturités en années
        current_date = datetime.now()
        maturities = []
        for exp_date in unique_expirations:
            exp_datetime = datetime.strptime(exp_date, '%Y-%m-%d')
            maturity = (exp_datetime - current_date).days / 365.25
            # S'assurer que la maturité est positive et raisonnable
            if maturity < 0:
                print(f"⚠️  Maturité négative pour {exp_date}: {maturity:.4f} ans")
                maturity = 0.01  # Maturité minimale
            elif maturity > 5:
                print(f"⚠️  Maturité très élevée pour {exp_date}: {maturity:.4f} ans")
                maturity = 5.0  # Maturité maximale
            maturities.append(maturity)
        
        # Créer la matrice de volatilité implicite
        iv_matrix = []
        for i, expiration in enumerate(unique_expirations):
            row = []
            for strike in unique_strikes:
                # Trouver l'option correspondante
                option = combined_data[
                    (combined_data['expiration_date'] == expiration) & 
                    (combined_data['strike'] == strike)
                ]
                
                if not option.empty:
                    # Prendre la moyenne des IV pour les calls et puts
                    iv_values = option['impliedVolatility'].values
                    # Filtrer les valeurs aberrantes (IV > 200% ou < 1%)
                    valid_iv_values = [iv for iv in iv_values if 0.01 <= iv <= 2.0]
                    
                    if valid_iv_values:
                        avg_iv = float(sum(valid_iv_values) / len(valid_iv_values))
                        row.append(avg_iv)
                    else:
                        row.append(None)
                else:
                    row.append(None)
            iv_matrix.append(row)
        
        # Calculer les statistiques sur les données filtrées
        valid_iv_data = combined_data[
            (combined_data['impliedVolatility'] >= 0.01) & 
            (combined_data['impliedVolatility'] <= 2.0)
        ]
        
        if valid_iv_data.empty:
            return jsonify({
                'error': f'Aucune donnée IV valide pour {symbol}'
            }), 404
        
        # Convertir le DataFrame en format JSON
        result = {
            'symbol': symbol,
            'spot_price': spot_price,
            'data_source': 'Finnhub API (Données Réelles)',
            'strikes': unique_strikes,
            'maturities': maturities,
            'iv': iv_matrix,
            'total_options': len(combined_data),
            'calls_count': len(combined_data[combined_data['type'] == 'call']),
            'puts_count': len(combined_data[combined_data['type'] == 'put']),
            'valid_options': len(valid_iv_data),
            'statistics': {
                'min_iv': float(valid_iv_data['impliedVolatility'].min()),
                'max_iv': float(valid_iv_data['impliedVolatility'].max()),
                'avg_iv': float(valid_iv_data['impliedVolatility'].mean()),
                'std_iv': float(valid_iv_data['impliedVolatility'].std())
            },
            'raw_options': combined_data.to_dict('records')  # Données brutes pour debug
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500



@app.route('/api/indices')
def api_indices():
    """API pour récupérer uniquement les indices"""
    try:
        data = yahoo_api.get_market_data()
        return jsonify(data.get('indices', {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks')
def api_stocks():
    """API pour récupérer uniquement les actions"""
    try:
        data = yahoo_api.get_market_data()
        return jsonify(data.get('stocks', {}))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API pour les calculs d'options Call & Put
@app.route('/api/calculate-option', methods=['POST'])
def api_calculate_option():
    """API pour calculer le prix d'une option"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['spotPrice', 'strikePrice', 'timeMaturity', 'riskFreeRate', 'volatility', 'optionType']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ manquant: {field}'}), 400
        
        # Extraction des paramètres
        spot_price = float(data['spotPrice'])
        strike_price = float(data['strikePrice'])
        time_maturity = float(data['timeMaturity'])
        risk_free_rate = float(data['riskFreeRate'])
        volatility = float(data['volatility'])
        option_type = data['optionType']
        model_choice = data['modelChoice']
        
        # Validation des valeurs
        if spot_price <= 0 or strike_price <= 0 or time_maturity <= 0:
            return jsonify({'error': 'Les prix et l\'échéance doivent être positifs'}), 400
        
        if risk_free_rate < 0 or risk_free_rate > 1 or volatility < 0 or volatility > 1:
            return jsonify({'error': 'Le taux sans risque et la volatilité doivent être entre 0 et 1'}), 400
        
        # Si Monte Carlo: simuler les trajectoires pour obtenir prix et IC
        # Toujours calculer Monte Carlo et Black-Scholes pour comparaison
        if True:
            nb_simulations = int(data.get('numSimulations', 10000))
            nb_steps = int(data.get('numSteps', 252))
            confidence_level = float(data.get('confidenceLevel', 0.95))

            t_all_start = time.perf_counter()
            t_mc_start = time.perf_counter()
            mc = pricer.monte_carlo_price_and_greeks(
                S=spot_price,
                K=strike_price,
                T=time_maturity,
                r=risk_free_rate,
                sigma=volatility,
                option_type=option_type,
                nb_simulations=nb_simulations,
                nb_steps=nb_steps,
                return_std=True,
                return_paths=int(data.get('numPaths', 50)),
            )
            t_mc_ms = (time.perf_counter() - t_mc_start) * 1000.0
            try:
                z = _z_from_confidence(confidence_level)
            except Exception:
                z = 1.96

            t_bs_start = time.perf_counter()
            bs_price, bs_delta, bs_gamma, bs_theta, bs_vega, bs_rho = pricer.black_scholes_price_and_greeks(
                S=spot_price,
                K=strike_price,
                T=time_maturity,
                r=risk_free_rate,
                sigma=volatility,
                option_type=option_type,
            )
            t_bs_ms = (time.perf_counter() - t_bs_start) * 1000.0
            t_total_ms = (time.perf_counter() - t_all_start) * 1000.0

            result = {
                'monteCarlo': {
                    'optionPrice': round(mc['price'], 4),
                    'delta': round(mc['delta'], 4) if not math.isnan(mc['delta']) else None,
                    'gamma': round(mc['gamma'], 4) if not math.isnan(mc['gamma']) else None,
                    'theta': round(mc['theta'], 4) if not math.isnan(mc['theta']) else None,
                    'vega': round(mc.get('vega', float('nan')), 4) if not math.isnan(mc.get('vega', float('nan'))) else None,
                    'rho': round(mc.get('rho', float('nan')), 4) if not math.isnan(mc.get('rho', float('nan'))) else None,
                    'confidenceInterval': {
                        'lower': round(mc['price'] - z * mc['stdError'], 4),
                        'mean': round(mc['price'], 4),
                        'upper': round(mc['price'] + z * mc['stdError'], 4),
                        'confidenceLevel': round(confidence_level, 4),
                    },
                    'paths': mc.get('paths'),
                    'timeGrid': mc.get('timeGrid'),
                    'timeMs': round(t_mc_ms, 2),
                },
                'blackScholes': {
                    'optionPrice': round(bs_price, 4),
                    'delta': round(bs_delta, 4),
                    'gamma': round(bs_gamma, 4),
                    'theta': round(bs_theta, 4),
                    'vega': round(bs_vega, 4),
                    'rho': round(bs_rho, 4),
                    'timeMs': round(t_bs_ms, 2),
                },
                'parameters': {
                    'spotPrice': spot_price,
                    'strikePrice': strike_price,
                    'timeMaturity': time_maturity,
                    'riskFreeRate': risk_free_rate,
                    'volatility': volatility,
                    'optionType': option_type,
                    'numSimulations': nb_simulations,
                    'numSteps': nb_steps,
                    'confidenceLevel': round(confidence_level, 4),
                },
                'timings': {
                    'totalMs': round(t_total_ms, 2),
                }
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-metrics/<symbol>')
def api_risk_metrics(symbol):
    """Calculer les métriques de risque pour un symbole donné"""
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        
        # Utiliser le nouveau module Yahoo Finance API avec les dates spécifiées
        data = yahoo_api.get_chart_data(symbol, '1d', start, end)
        
        if not data or 'labels' not in data or 'datasets' not in data:
            return jsonify({'error': 'Données indisponibles'}), 404
        
        # Extraire les prix de clôture
        prices = [float(p) for p in data['datasets'][0]['data'] if p is not None and float(p) > 0]
        
        # Valider les données
        is_valid, message = risk_calculator.validate_data(prices)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Calculer toutes les métriques
        metrics = risk_calculator.calculate_all_metrics(prices)
        
        # Ajouter les informations de période
        result = {
            'symbol': symbol,
            **metrics,
            'period': {
                'start': data['labels'][0] if data['labels'] else None,
                'end': data['labels'][-1] if data['labels'] else None,
                'days': len(prices)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: surface de volatilité 3D optimisée avec fond transparent
@app.route('/api/vol-surface-3d/<symbol>')
def api_vol_surface_3d(symbol):
    """API endpoint optimisé pour la surface de volatilité 3D avec fond transparent"""
    try:
        span = float(request.args.get('span', 0.5))
        provider = request.args.get('provider', 'finnhub')
        
        # Validation des paramètres
        if span <= 0 or span > 1:
            return jsonify({'error': 'span doit être entre 0 et 1'}), 400
            
        if provider not in ['finnhub', 'polygon']:
            return jsonify({'error': 'provider doit être "finnhub" ou "polygon"'}), 400
        
        # Récupérer les données selon le provider
        if provider == 'polygon':
            from api.polygon_options_api import get_polygon_volatility_surface
            # Limiter à 6 expirations pour la performance
            max_expirations = int(request.args.get('maxExp', 6))
            
            try:
                result = get_polygon_volatility_surface(symbol, max_expirations, span)
                
                # Si Polygon.io échoue, essayer avec moins d'expirations
                if 'error' in result and 'limite de taux' in result['error'].lower():
                    print(f"⚠️  Limite de taux Polygon.io atteinte, tentative avec moins d'expirations")
                    result = get_polygon_volatility_surface(symbol, 2, span)  # Réduire à 2 expirations
                    
            except Exception as e:
                print(f"❌ Erreur Polygon.io: {e}")
                result = {'error': f'Erreur API Polygon.io: {str(e)}'}
        else:
            from api.finnhub_implied_volatility import get_options_expirations, get_implied_volatility
            
            # Récupérer les expirations
            expirations = get_options_expirations(symbol)
            if not expirations:
                return jsonify({'error': f'Aucune date d\'expiration disponible pour {symbol}'}), 404
            
            # Limiter le nombre d'expirations pour la performance (par défaut 6)
            max_expirations = int(request.args.get('maxExp', 6))
            expirations_to_use = expirations[:max_expirations]
            
            # Récupérer le prix spot
            try:
                import requests
                from api.finnhub_config import FINNHUB_API_KEY, FINNHUB_BASE_URL
                
                url = f"{FINNHUB_BASE_URL}/quote"
                params = {'symbol': symbol, 'token': FINNHUB_API_KEY}
                response = requests.get(url, params=params)
                response.raise_for_status()
                quote_data = response.json()
                spot_price = float(quote_data.get('c', 0))
            except:
                spot_price = 0
            
            # Collecter les données d'options
            all_options_data = []
            for expiration_timestamp in expirations_to_use:
                try:
                    expiration_date = datetime.fromtimestamp(expiration_timestamp).strftime('%Y-%m-%d')
                    options_data = get_implied_volatility(symbol, expiration_timestamp)
                    
                    if not options_data.empty:
                        options_data['expiration_date'] = expiration_date
                        all_options_data.append(options_data)
                        
                except Exception as e:
                    print(f"Erreur pour l'expiration {expiration_date}: {e}")
                    continue
            
            if not all_options_data:
                return jsonify({'error': f'Aucune donnée d\'options collectée pour {symbol}'}), 404
            
            # Traiter les données pour créer la surface
            result = process_volatility_surface_data(all_options_data, symbol, spot_price, span)
        
        if 'error' in result:
            error_msg = result['error']
            if 'limite de taux' in error_msg.lower() or '429' in error_msg:
                return jsonify({
                    'error': 'API Polygon.io temporairement indisponible (limite de taux). Veuillez réessayer dans quelques secondes.',
                    'details': error_msg
                }), 429
            elif 'aucune donnée' in error_msg.lower():
                return jsonify({
                    'error': f'Aucune donnée disponible pour {symbol} via {provider}',
                    'details': error_msg
                }), 404
            else:
                return jsonify({
                    'error': f'Erreur lors de la récupération des données: {error_msg}',
                    'details': error_msg
                }), 500
        
        # Utiliser notre classe VolatilitySurface3D pour optimiser les données
        try:
            from models.volatility_surface_3d import VolatilitySurface3D
            
            vs3d = VolatilitySurface3D(symbol)
            vs3d.set_data({
                'strikes': result['strikes'],
                'maturities': result['maturities'],
                'iv': result['iv'],
                'spot_price': result.get('spot_price', 0)
            })
            
            # Ajouter les statistiques calculées par la classe
            result['statistics'] = vs3d.get_statistics()
            result['plot_config'] = vs3d.get_plot_config()
            
        except ImportError:
            print("Classe VolatilitySurface3D non disponible, utilisation des données standard")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: Export des données de surface de volatilité 3D
@app.route('/api/vol-surface-3d-export/<symbol>')
def api_vol_surface_3d_export(symbol):
    """API endpoint pour exporter les données de surface de volatilité 3D"""
    try:
        span = float(request.args.get('span', 0.5))
        provider = request.args.get('provider', 'finnhub')
        format_type = request.args.get('format', 'json')  # json, csv, excel
        
        # Validation des paramètres
        if span <= 0 or span > 1:
            return jsonify({'error': 'span doit être entre 0 et 1'}), 400
            
        if provider not in ['finnhub', 'polygon']:
            return jsonify({'error': 'provider doit être "finnhub" ou "polygon"'}), 400
            
        if format_type not in ['json', 'csv', 'excel']:
            return jsonify({'error': 'format doit être "json", "csv" ou "excel"'}), 400
        
        # Récupérer les données selon le provider
        if provider == 'polygon':
            from api.polygon_options_api import get_polygon_volatility_surface
            result = get_polygon_volatility_surface(symbol, 12, span)
        else:
            from api.finnhub_implied_volatility import get_options_expirations, get_implied_volatility
            
            # Récupérer les expirations
            expirations = get_options_expirations(symbol)
            if not expirations:
                return jsonify({'error': f'Aucune date d\'expiration disponible pour {symbol}'}), 404
            
            # Utiliser toutes les expirations disponibles
            expirations_to_use = expirations
            
            # Récupérer le prix spot
            try:
                import requests
                from api.finnhub_config import FINNHUB_API_KEY, FINNHUB_BASE_URL
                
                url = f"{FINNHUB_BASE_URL}/quote"
                params = {'symbol': symbol, 'token': FINNHUB_API_KEY}
                response = requests.get(url, params=params)
                response.raise_for_status()
                quote_data = response.json()
                spot_price = float(quote_data.get('c', 0))
            except:
                spot_price = 0
            
            # Collecter les données d'options
            all_options_data = []
            for expiration_timestamp in expirations_to_use:
                try:
                    expiration_date = datetime.fromtimestamp(expiration_timestamp).strftime('%Y-%m-%d')
                    options_data = get_implied_volatility(symbol, expiration_timestamp)
                    
                    if not options_data.empty:
                        options_data['expiration_date'] = expiration_date
                        all_options_data.append(options_data)
                        
                except Exception as e:
                    print(f"Erreur pour l'expiration {expiration_date}: {e}")
                    continue
            
            if not all_options_data:
                return jsonify({'error': f'Aucune donnée d\'options collectée pour {symbol}'}), 404
            
            # Traiter les données pour créer la surface
            result = process_volatility_surface_data(all_options_data, symbol, spot_price, span)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 404
        
        # Préparer les données d'export
        export_data = {
            'metadata': {
                'symbol': symbol,
                'provider': provider,
                'span': span,
                'export_date': datetime.now().isoformat(),
                'spot_price': result.get('spot_price', 0),
                'maturities_count': len(result.get('maturities', [])),
                'strikes_count': len(result.get('strikes', [])),
                'data_points': sum(len(row) for row in result.get('iv', []) if row)
            },
            'data': {
                'strikes': result.get('strikes', []),
                'maturities': result.get('maturities', []),
                'iv_matrix': result.get('iv', [])
            }
        }
        
        # Ajouter les statistiques si disponibles
        try:
            from models.volatility_surface_3d import VolatilitySurface3D
            vs3d = VolatilitySurface3D(symbol)
            vs3d.set_data({
                'strikes': result['strikes'],
                'maturities': result['maturities'],
                'iv': result['iv'],
                'spot_price': result.get('spot_price', 0)
            })
            export_data['statistics'] = vs3d.get_statistics()
        except ImportError:
            pass
        
        # Retourner selon le format demandé
        if format_type == 'json':
            return jsonify(export_data)
        elif format_type == 'csv':
            # Créer un CSV avec les données de la matrice IV
            import io
            import csv
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # En-tête avec les strikes
            header = ['Maturité (années)'] + [f'Strike ${s:.2f}' for s in result.get('strikes', [])]
            writer.writerow(header)
            
            # Données IV
            for i, maturity in enumerate(result.get('maturities', [])):
                row = [f'{maturity:.3f}'] + [f'{iv:.4f}' if iv is not None else '' for iv in result.get('iv', [])[i]]
                writer.writerow(row)
            
            output.seek(0)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename=volatility_surface_{symbol}_{datetime.now().strftime("%Y%m%d")}.csv'}
            )
        elif format_type == 'excel':
            # Créer un fichier Excel
            try:
                import openpyxl
                from openpyxl.styles import Font, PatternFill
                
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Surface de Volatilité"
                
                # Métadonnées
                ws['A1'] = 'Métadonnées'
                ws['A1'].font = Font(bold=True)
                ws['A2'] = f'Symbole: {symbol}'
                ws['A3'] = f'Fournisseur: {provider}'
                ws['A4'] = f'Prix Spot: ${result.get("spot_price", 0):.2f}'
                ws['A5'] = f'Date d\'export: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                
                # Données IV
                ws['A7'] = 'Matrice de Volatilité Implicite'
                ws['A7'].font = Font(bold=True)
                
                # En-tête avec les strikes
                for j, strike in enumerate(result.get('strikes', []), 1):
                    ws.cell(row=8, column=j+1, value=f'Strike ${strike:.2f}')
                
                # Données IV
                for i, maturity in enumerate(result.get('maturities', []), 8):
                    ws.cell(row=i+1, column=1, value=f'{maturity:.3f}a')
                    for j, iv in enumerate(result.get('iv', [])[i-8], 1):
                        if iv is not None:
                            ws.cell(row=i+1, column=j+1, value=iv)
                
                # Sauvegarder en mémoire
                from io import BytesIO
                output = BytesIO()
                wb.save(output)
                output.seek(0)
                
                return Response(
                    output.getvalue(),
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={'Content-Disposition': f'attachment; filename=volatility_surface_{symbol}_{datetime.now().strftime("%Y%m%d")}.xlsx'}
                )
                
            except ImportError:
                return jsonify({'error': 'openpyxl non installé pour l\'export Excel'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: Smile de volatilité avec une seule maturité (Finnhub uniquement)
@app.route('/api/volatility-smile/<symbol>')
def api_volatility_smile(symbol):
    """API endpoint pour le smile de volatilité avec une seule maturité (Finnhub uniquement)"""
    try:
        maturity_days = int(request.args.get('maturity', 30))  # Maturité en jours
        span = float(request.args.get('span', 0.3))  # Bande autour du spot
        
        # Validation des paramètres
        if maturity_days < 1 or maturity_days > 365:
            return jsonify({'error': 'maturity doit être entre 1 et 365 jours'}), 400
            
        if span <= 0 or span > 1:
            return jsonify({'error': 'span doit être entre 0 et 1'}), 400
        
        # Utiliser uniquement Finnhub pour le smile
        from api.finnhub_volatility_smile import create_volatility_smile
        
        try:
            result = create_volatility_smile(symbol, maturity_days, span)
        except Exception as e:
            print(f"❌ Erreur création smile: {e}")
            result = {'error': f'Erreur création smile: {str(e)}'}
        
        if 'error' in result:
            error_msg = result['error']
            if 'aucune option' in error_msg.lower():
                return jsonify({
                    'error': f'Aucune option disponible pour {symbol} avec maturité ~{maturity_days} jours',
                    'details': error_msg
                }), 404
            else:
                return jsonify({
                    'error': f'Erreur lors de la récupération du smile: {error_msg}',
                    'details': error_msg
                }), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: Symboles disponibles avec leurs APIs supportées
@app.route('/api/available-symbols')
def api_available_symbols():
    """API endpoint pour récupérer les symboles disponibles avec leurs APIs supportées"""
    try:
        # Données basées sur le test des meilleurs symboles (4 symboles avec le plus de maturités)
        symbols_data = {
            'recommended_symbols': [
                {
                    'symbol': 'QQQ',
                    'label': 'QQQ - Invesco QQQ Trust (Recommandé)',
                    'apis': ['finnhub', 'polygon'],
                    'finnhub_count': 8362,
                    'polygon_count': 1000,
                    'finnhub_maturities': 33,
                    'polygon_maturities': 5,
                    'description': 'ETF Nasdaq 100 - 38 maturités totales'
                },
                {
                    'symbol': 'SPY',
                    'label': 'SPY - SPDR S&P 500 ETF (Recommandé)',
                    'apis': ['finnhub', 'polygon'],
                    'finnhub_count': 8852,
                    'polygon_count': 1000,
                    'finnhub_maturities': 32,
                    'polygon_maturities': 5,
                    'description': 'ETF S&P 500 - 37 maturités totales'
                },
                {
                    'symbol': 'AAPL',
                    'label': 'AAPL - Apple Inc (Recommandé)',
                    'apis': ['finnhub', 'polygon'],
                    'finnhub_count': 2298,
                    'polygon_count': 1000,
                    'finnhub_maturities': 20,
                    'polygon_maturities': 10,
                    'description': 'Apple - 30 maturités totales'
                },
                {
                    'symbol': 'TSLA',
                    'label': 'TSLA - Tesla Inc (Recommandé)',
                    'apis': ['finnhub', 'polygon'],
                    'finnhub_count': 4356,
                    'polygon_count': 1000,
                    'finnhub_maturities': 21,
                    'polygon_maturities': 5,
                    'description': 'Tesla - 26 maturités totales'
                }
            ],
            'finnhub_symbols': [],  # Pas de symboles Finnhub seulement
            'polygon_symbols': [],  # Pas de symboles Polygon.io seulement
            'statistics': {
                'total_symbols': 4,
                'recommended_count': 4,
                'finnhub_only_count': 0,
                'polygon_only_count': 0,
                'coverage': {
                    'finnhub': '100%',
                    'polygon': '100%'
                }
            }
        }
        
        return jsonify(symbols_data)
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des symboles: {str(e)}'}), 500


def process_volatility_surface_data(all_options_data, symbol, spot_price, span):
    """Traite les données d'options pour créer une surface de volatilité"""
    try:
        # Combiner toutes les données
        combined_data = pd.concat(all_options_data, ignore_index=True)
        
        # Calculer les maturités en années
        current_date = datetime.now()
        combined_data['maturity_years'] = combined_data['expiration_date'].apply(
            lambda x: (datetime.strptime(x, '%Y-%m-%d') - current_date).days / 365.25
        )
        
        # Filtrer les maturités futures
        combined_data = combined_data[combined_data['maturity_years'] > 0]
        
        if combined_data.empty:
            return {'error': 'Aucune donnée de maturité future disponible'}
        
        # Filtrer par span autour du spot
        if spot_price > 0:
            min_strike = spot_price * (1 - span)
            max_strike = spot_price * (1 + span)
            combined_data = combined_data[
                (combined_data['strike'] >= min_strike) & 
                (combined_data['strike'] <= max_strike)
            ]
        
        if combined_data.empty:
            return {'error': 'Aucune donnée dans la plage de strikes spécifiée'}
        
        # Grouper par maturité et strike pour créer la surface
        unique_maturities = sorted(combined_data['maturity_years'].unique())
        unique_strikes = sorted(combined_data['strike'].unique())
        
        # Créer la matrice de volatilité implicite
        iv_matrix = []
        for maturity in unique_maturities:
            maturity_data = combined_data[combined_data['maturity_years'] == maturity]
            row = []
            for strike in unique_strikes:
                strike_data = maturity_data[maturity_data['strike'] == strike]
                if not strike_data.empty:
                    # Prendre la moyenne des IV pour ce strike/maturité
                    # Vérifier les noms de colonnes possibles
                    iv_column = None
                    for col in ['implied_volatility', 'impliedVolatility', 'iv']:
                        if col in strike_data.columns:
                            iv_column = col
                            break
                    
                    if iv_column:
                        avg_iv = strike_data[iv_column].mean()
                        row.append(avg_iv)
                    else:
                        row.append(None)
                else:
                    row.append(None)
            iv_matrix.append(row)
        
        # Calculer les statistiques
        all_iv_values = []
        for row in iv_matrix:
            all_iv_values.extend([v for v in row if v is not None and not pd.isna(v)])
        
        stats = {}
        if all_iv_values:
            stats = {
                'min_iv': float(min(all_iv_values)),
                'max_iv': float(max(all_iv_values)),
                'mean_iv': float(sum(all_iv_values) / len(all_iv_values))
            }
        
        # Compter les options
        total_options = len(combined_data)
        calls_count = len(combined_data[combined_data['type'] == 'call'])
        puts_count = len(combined_data[combined_data['type'] == 'put'])
        
        return {
            'symbol': symbol,
            'strikes': unique_strikes,
            'maturities': unique_maturities,
            'iv': iv_matrix,
            'spot_price': spot_price,
            'data_source': 'Finnhub API (Données Réelles)',
            'total_options': total_options,
            'calls_count': calls_count,
            'puts_count': puts_count,
            'statistics': stats,
            'raw_options': combined_data.to_dict('records')
        }
        
    except Exception as e:
        return {'error': f'Erreur lors du traitement des données: {str(e)}'}


if __name__ == '__main__':
    # Configuration pour la production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
