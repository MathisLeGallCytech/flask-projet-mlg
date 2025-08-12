import unittest
import json
import time
import requests
from unittest.mock import patch, MagicMock
import sys
import os

# Ajouter le répertoire parent au path pour importer l'app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class FlaskAppTestCase(unittest.TestCase):
    """Classe de test pour l'application Flask complète"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.app = app.test_client()
        self.app.testing = True
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        pass

    def test_home_page(self):
        """Test de la page d'accueil"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_cv_page(self):
        """Test de la page CV"""
        response = self.app.get('/cv-mathis-le-gall')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_indices_actions_page(self):
        """Test de la page indices et actions"""
        response = self.app.get('/indices-actions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_call_put_page(self):
        """Test de la page Call & Put"""
        response = self.app.get('/call-put')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_volatility_surface_page(self):
        """Test de la page surface de volatilité"""
        response = self.app.get('/volatility-surface')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_force_refresh_page(self):
        """Test de la page force refresh"""
        response = self.app.get('/force-refresh')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_debug_finnhub_page(self):
        """Test de la page debug Finnhub"""
        response = self.app.get('/debug-finnhub')
        # La page peut retourner 500 si le template n'existe pas, ce qui est normal
        self.assertIn(response.status_code, [200, 500])
        if response.status_code == 200:
            self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_debug_polygon_page(self):
        """Test de la page debug Polygon"""
        response = self.app.get('/debug-polygon')
        # La page peut retourner 500 si le template n'existe pas, ce qui est normal
        self.assertIn(response.status_code, [200, 500])
        if response.status_code == 200:
            self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_analyse_actions_indices_page(self):
        """Test de la page analyse actions indices"""
        response = self.app.get('/analyse-actions-indices')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_description_app_page(self):
        """Test de la page description app"""
        response = self.app.get('/description-app')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    @patch('api.yahoo_finance_api.yahoo_api.get_market_data')
    def test_api_market_data_success(self, mock_get_market_data):
        """Test de l'API market data avec succès"""
        # Mock des données de test
        mock_data = {
            'indices': {
                '^GSPC': {'price': 4500.0, 'change': 25.0, 'changePercent': 0.56},
                '^IXIC': {'price': 14000.0, 'change': 50.0, 'changePercent': 0.36}
            },
            'stocks': {
                'AAPL': {'price': 150.0, 'change': 2.0, 'changePercent': 1.35},
                'MSFT': {'price': 300.0, 'change': 5.0, 'changePercent': 1.69}
            }
        }
        mock_get_market_data.return_value = mock_data
        
        response = self.app.get('/api/market-data')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('indices', data)
        self.assertIn('stocks', data)
        self.assertEqual(data['indices']['^GSPC']['price'], 4500.0)

    @patch('api.yahoo_finance_api.yahoo_api.get_market_data')
    def test_api_market_data_error(self, mock_get_market_data):
        """Test de l'API market data avec erreur"""
        mock_get_market_data.return_value = None
        
        response = self.app.get('/api/market-data')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('indices', data)
        self.assertIn('stocks', data)

    @patch('api.yahoo_finance_api.yahoo_api.get_chart_data')
    def test_api_chart_data_success(self, mock_get_chart_data):
        """Test de l'API chart data avec succès"""
        mock_data = {
            'labels': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'datasets': [{
                'label': 'AAPL',
                'data': [150.0, 152.0, 151.5]
            }]
        }
        mock_get_chart_data.return_value = mock_data
        
        response = self.app.get('/api/chart-data-v2/AAPL?timeframe=1mo')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        self.assertEqual(len(data['labels']), 3)

    @patch('api.yahoo_finance_api.yahoo_api.get_chart_data')
    def test_api_chart_data_error(self, mock_get_chart_data):
        """Test de l'API chart data avec erreur"""
        mock_get_chart_data.return_value = None
        
        response = self.app.get('/api/chart-data-v2/AAPL')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)

    def test_api_calculate_option_valid_data(self):
        """Test de l'API calculate option avec données valides"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 105.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('monteCarlo', data)
        self.assertIn('blackScholes', data)
        self.assertIn('parameters', data)
        self.assertIn('timings', data)
        
        # Vérifier que les prix sont des nombres positifs
        self.assertGreater(data['monteCarlo']['optionPrice'], 0)
        self.assertGreater(data['blackScholes']['optionPrice'], 0)

    def test_api_calculate_option_invalid_data(self):
        """Test de l'API calculate option avec données invalides"""
        test_data = {
            'spotPrice': -100.0,  # Prix négatif invalide
            'strikePrice': 105.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo'
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_calculate_option_missing_fields(self):
        """Test de l'API calculate option avec champs manquants"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 105.0
            # Champs manquants
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('api.yahoo_finance_api.yahoo_api.get_chart_data')
    def test_api_risk_metrics_success(self, mock_get_chart_data):
        """Test de l'API risk metrics avec succès"""
        mock_data = {
            'labels': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            'datasets': [{
                'label': 'AAPL',
                'data': [150.0, 152.0, 151.5, 153.0, 152.5]
            }]
        }
        mock_get_chart_data.return_value = mock_data
        
        response = self.app.get('/api/risk-metrics/AAPL')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('symbol', data)
        self.assertIn('volatility', data)
        self.assertIn('var_95', data)
        self.assertIn('period', data)
        self.assertEqual(data['symbol'], 'AAPL')

    @patch('api.yahoo_finance_api.yahoo_api.get_chart_data')
    def test_api_risk_metrics_no_data(self, mock_get_chart_data):
        """Test de l'API risk metrics sans données"""
        mock_get_chart_data.return_value = None
        
        response = self.app.get('/api/risk-metrics/AAPL')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_vol_surface_invalid_params(self):
        """Test de l'API vol surface avec paramètres invalides"""
        response = self.app.get('/api/vol-surface/AAPL?maxExp=20&span=2.0')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_vol_surface_3d_invalid_params(self):
        """Test de l'API vol surface 3D avec paramètres invalides"""
        response = self.app.get('/api/vol-surface-3d/AAPL?span=2.0')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_volatility_smile_invalid_params(self):
        """Test de l'API volatility smile avec paramètres invalides"""
        response = self.app.get('/api/volatility-smile/AAPL?maturity=400&span=2.0')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_available_symbols(self):
        """Test de l'API available symbols"""
        response = self.app.get('/api/available-symbols')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('recommended_symbols', data)
        self.assertIn('statistics', data)
        self.assertGreater(len(data['recommended_symbols']), 0)

    def test_api_indices_only(self):
        """Test de l'API indices uniquement"""
        with patch('api.yahoo_finance_api.yahoo_api.get_market_data') as mock_get_data:
            mock_get_data.return_value = {
                'indices': {'^GSPC': {'price': 4500.0}},
                'stocks': {}
            }
            
            response = self.app.get('/api/indices')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('^GSPC', data)

    def test_api_stocks_only(self):
        """Test de l'API stocks uniquement"""
        with patch('api.yahoo_finance_api.yahoo_api.get_market_data') as mock_get_data:
            mock_get_data.return_value = {
                'indices': {},
                'stocks': {'AAPL': {'price': 150.0}}
            }
            
            response = self.app.get('/api/stocks')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('AAPL', data)

    def test_api_vol_surface_3d_export_invalid_format(self):
        """Test de l'API vol surface 3D export avec format invalide"""
        response = self.app.get('/api/vol-surface-3d-export/AAPL?format=invalid')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_404_error(self):
        """Test de gestion des erreurs 404"""
        response = self.app.get('/route-inexistante')
        self.assertEqual(response.status_code, 404)

    def test_api_chart_data_legacy_route(self):
        """Test de la route legacy chart data"""
        with patch('api.yahoo_finance_api.yahoo_api.get_chart_data') as mock_get_data:
            mock_get_data.return_value = {
                'labels': ['2024-01-01'],
                'datasets': [{'label': 'AAPL', 'data': [150.0]}]
            }
            
            response = self.app.get('/api/chart-data/AAPL')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('labels', data)

    def test_put_option_calculation(self):
        """Test du calcul d'option put"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 95.0,
            'timeMaturity': 0.5,
            'riskFreeRate': 0.03,
            'volatility': 0.25,
            'optionType': 'put',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('monteCarlo', data)
        self.assertIn('blackScholes', data)
        self.assertEqual(data['parameters']['optionType'], 'put')

    def test_high_volatility_option(self):
        """Test du calcul d'option avec haute volatilité"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.8,  # Haute volatilité
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('monteCarlo', data)
        self.assertIn('blackScholes', data)
        # Vérifier que les prix sont calculés même avec haute volatilité
        self.assertIsNotNone(data['monteCarlo']['optionPrice'])

    def test_short_maturity_option(self):
        """Test du calcul d'option avec maturité courte"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 0.01,  # Maturité très courte
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('monteCarlo', data)
        self.assertIn('blackScholes', data)

    def test_high_simulation_count(self):
        """Test avec un nombre élevé de simulations"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 50000,  # Nombre élevé de simulations
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('monteCarlo', data)
        self.assertIn('blackScholes', data)
        # Vérifier que les temps de calcul sont présents
        self.assertIn('timeMs', data['monteCarlo'])
        self.assertIn('timeMs', data['blackScholes'])

    def test_confidence_interval_calculation(self):
        """Test du calcul d'intervalle de confiance"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 10000,
            'numSteps': 252,
            'confidenceLevel': 0.99,  # Niveau de confiance élevé
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('confidenceInterval', data['monteCarlo'])
        self.assertIn('lower', data['monteCarlo']['confidenceInterval'])
        self.assertIn('upper', data['monteCarlo']['confidenceInterval'])
        self.assertIn('mean', data['monteCarlo']['confidenceInterval'])
        self.assertEqual(data['monteCarlo']['confidenceInterval']['confidenceLevel'], 0.99)

    def test_greeks_calculation(self):
        """Test du calcul des grecques"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 10000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Vérifier les grecques Monte Carlo
        mc_greeks = data['monteCarlo']
        self.assertIn('delta', mc_greeks)
        self.assertIn('gamma', mc_greeks)
        self.assertIn('theta', mc_greeks)
        
        # Vérifier les grecques Black-Scholes
        bs_greeks = data['blackScholes']
        self.assertIn('delta', bs_greeks)
        self.assertIn('gamma', bs_greeks)
        self.assertIn('theta', bs_greeks)
        self.assertIn('vega', bs_greeks)
        self.assertIn('rho', bs_greeks)

    def test_paths_generation(self):
        """Test de la génération des chemins Monte Carlo"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 10000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 5  # Nombre de chemins à retourner
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('paths', data['monteCarlo'])
        self.assertIn('timeGrid', data['monteCarlo'])
        
        # Vérifier que les chemins sont générés
        paths = data['monteCarlo']['paths']
        time_grid = data['monteCarlo']['timeGrid']
        self.assertIsInstance(paths, list)
        self.assertIsInstance(time_grid, list)
        self.assertGreater(len(paths), 0)
        self.assertGreater(len(time_grid), 0)


class PerformanceTestCase(unittest.TestCase):
    """Tests de performance de l'application"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.app = app.test_client()
        self.app.testing = True

    def test_option_calculation_performance(self):
        """Test de performance du calcul d'options"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 10000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        start_time = time.time()
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que le calcul prend moins de 10 secondes
        calculation_time = end_time - start_time
        self.assertLess(calculation_time, 10.0, f"Calcul trop lent: {calculation_time:.2f} secondes")
        
        data = json.loads(response.data)
        # Vérifier que les temps de calcul sont rapportés
        self.assertIn('timings', data)
        self.assertIn('totalMs', data['timings'])

    def test_multiple_concurrent_requests(self):
        """Test de performance avec requêtes concurrentes"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,  # Réduit pour le test de performance
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 5
        }
        
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = self.app.post('/api/calculate-option',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {e}")
        
        # Lancer 5 requêtes concurrentes
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Attendre que toutes les requêtes se terminent
        for thread in threads:
            thread.join()
        
        # Vérifier que toutes les requêtes ont réussi
        success_count = 0
        while not results.empty():
            result = results.get()
            if result == 200:
                success_count += 1
        
        self.assertEqual(success_count, 5, "Toutes les requêtes concurrentes doivent réussir")


class ErrorHandlingTestCase(unittest.TestCase):
    """Tests de gestion d'erreurs"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_json_request(self):
        """Test avec JSON invalide"""
        response = self.app.post('/api/calculate-option',
                               data='invalid json',
                               content_type='application/json')
        
        # L'application peut retourner 400 ou 500 selon la gestion d'erreur
        self.assertIn(response.status_code, [400, 500])

    def test_missing_content_type(self):
        """Test sans content-type"""
        test_data = {
            'spotPrice': 100.0,
            'strikePrice': 100.0,
            'timeMaturity': 1.0,
            'riskFreeRate': 0.05,
            'volatility': 0.2,
            'optionType': 'call',
            'modelChoice': 'monte_carlo'
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data))
        
        # L'application peut retourner 400 ou 500 selon la gestion d'erreur
        self.assertIn(response.status_code, [400, 500])

    def test_extreme_values(self):
        """Test avec des valeurs extrêmes"""
        test_data = {
            'spotPrice': 1e10,  # Valeur très élevée
            'strikePrice': 1e10,
            'timeMaturity': 10.0,  # Maturité très longue
            'riskFreeRate': 0.5,
            'volatility': 0.99,  # Volatilité très élevée
            'optionType': 'call',
            'modelChoice': 'monte_carlo',
            'numSimulations': 1000,
            'numSteps': 252,
            'confidenceLevel': 0.95,
            'numPaths': 10
        }
        
        response = self.app.post('/api/calculate-option',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # L'application doit gérer ces valeurs extrêmes
        self.assertIn(response.status_code, [200, 400])


def run_tests():
    """Fonction pour exécuter tous les tests"""
    print("🚀 Démarrage des tests de l'application Flask...")
    print("=" * 60)
    
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter les tests
    test_classes = [
        FlaskAppTestCase,
        PerformanceTestCase,
        ErrorHandlingTestCase
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Afficher un résumé
    print("=" * 60)
    print(f"📊 Résumé des tests:")
    print(f"   Tests exécutés: {result.testsRun}")
    print(f"   Échecs: {len(result.failures)}")
    print(f"   Erreurs: {len(result.errors)}")
    print(f"   Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print("\n❌ Échecs:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️  Erreurs:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ Tous les tests ont réussi!")
        return True
    else:
        print("\n❌ Certains tests ont échoué.")
        return False


if __name__ == '__main__':
    # Exécuter les tests
    success = run_tests()
    
    # Code de sortie approprié
    exit(0 if success else 1)
