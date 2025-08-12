import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import math

class RiskMetricsCalculator:
    """Calculateur de métriques de risque financier"""
    
    def __init__(self):
        pass
    
    def calculate_volatility(self, returns: List[float]) -> float:
        """Calculer la volatilité annualisée en %"""
        if len(returns) < 2:
            return 0.0
        
        returns_array = np.array(returns)
        daily_vol = np.std(returns_array)
        annual_vol = daily_vol * math.sqrt(252)  # 252 jours de trading
        return annual_vol * 100  # Convertir en %
    
    def calculate_var_95(self, returns: List[float]) -> float:
        """Calculer la Value at Risk 95% en %"""
        if len(returns) < 10:
            return 0.0
        
        returns_array = np.array(returns)
        var_95 = np.percentile(returns_array, 5)  # 5ème percentile
        return var_95 * 100  # Convertir en %
    
    def calculate_max_drawdown(self, prices: List[float]) -> float:
        """Calculer le maximum drawdown en %"""
        if len(prices) < 2:
            return 0.0
        
        prices_array = np.array(prices)
        peak = prices_array[0]
        max_dd = 0.0
        
        for price in prices_array[1:]:
            if price > peak:
                peak = price
            else:
                drawdown = (peak - price) / peak
                if drawdown > max_dd:
                    max_dd = drawdown
        
        return max_dd * 100  # Convertir en %
    
    def calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.0) -> float:
        """Calculer le ratio de Sharpe"""
        if len(returns) < 2:
            return 0.0
        
        returns_array = np.array(returns)
        excess_returns = returns_array - risk_free_rate/252  # Taux sans risque quotidien
        
        mean_excess_return = np.mean(excess_returns)
        std_excess_return = np.std(excess_returns)
        
        if std_excess_return == 0:
            return 0.0
        
        sharpe = mean_excess_return / std_excess_return * math.sqrt(252)  # Annualisé
        return sharpe
    
    def calculate_total_return(self, prices: List[float]) -> float:
        """Calculer le rendement total en %"""
        if len(prices) < 2:
            return 0.0

        initial_price = prices[0]
        final_price = prices[-1]
        total_return = (final_price - initial_price) / initial_price
        return total_return * 100  # Convertir en %

    def calculate_annualized_return(self, prices: List[float]) -> float:
        """Calculer le rendement annuel (annualisé) en %"""
        if len(prices) < 2:
            return 0.0

        initial_price = prices[0]
        final_price = prices[-1]
        total_return = (final_price - initial_price) / initial_price
        
        # Calculer le nombre d'années (approximatif basé sur 252 jours de trading)
        days = len(prices) - 1
        years = days / 252.0
        
        if years <= 0:
            return 0.0
        
        # Calculer le rendement annualisé
        # (1 + r_total)^(1/years) - 1
        annualized_return = ((1 + total_return) ** (1 / years) - 1) * 100
        return annualized_return

    def calculate_all_metrics(self, prices: List[float]) -> Dict[str, float]:
        """Calculer toutes les métriques de risque"""
        if len(prices) < 2:
            return {
                'volatility': 0.0,
                'var_95': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'total_return': 0.0,
                'annualized_return': 0.0
            }

        # Calculer les rendements
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])

        if len(returns) < 2:
            return {
                'volatility': 0.0,
                'var_95': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'total_return': 0.0,
                'annualized_return': 0.0
            }

        # Calculer toutes les métriques
        metrics = {
            'volatility': self.calculate_volatility(returns),
            'var_95': self.calculate_var_95(returns),
            'max_drawdown': self.calculate_max_drawdown(prices),
            'sharpe_ratio': self.calculate_sharpe_ratio(returns),
            'total_return': self.calculate_total_return(prices),
            'annualized_return': self.calculate_annualized_return(prices)
        }

        return metrics
    
    def validate_data(self, prices: List[float]) -> Tuple[bool, str]:
        """Valider les données d'entrée"""
        if not prices:
            return False, "Aucune donnée fournie"
        
        if len(prices) < 2:
            return False, "Au moins 2 points de données requis"
        
        # Vérifier que tous les prix sont positifs
        if any(p <= 0 for p in prices):
            return False, "Tous les prix doivent être positifs"
        
        # Vérifier qu'il n'y a pas de valeurs NaN ou infinies
        if any(not math.isfinite(p) for p in prices):
            return False, "Données invalides (NaN ou infini)"
        
        return True, "OK"

# Instance globale
risk_calculator = RiskMetricsCalculator()
