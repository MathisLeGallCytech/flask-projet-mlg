import numpy as np
import math

class GreeksCalculator:
    """
    Calculateur des Greeks et du payoff pour les options européennes
    utilisant les formules Black-Scholes
    """
    
    def __init__(self):
        pass
    
    def normal_cdf(self, x):
        """Fonction de répartition cumulative de la loi normale"""
        return 0.5 * (1 + self.erf(x / math.sqrt(2)))
    
    def normal_pdf(self, x):
        """Densité de probabilité de la loi normale"""
        return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    
    def erf(self, x):
        """Approximation de la fonction d'erreur"""
        # Approximation de Abramowitz et Stegun
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911
        
        sign = 1 if x >= 0 else -1
        x = abs(x)
        
        t = 1.0 / (1.0 + p * x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
        
        return sign * y
    
    def calculate_d1_d2(self, S, K, T, r, sigma):
        """Calcul des paramètres d1 et d2 pour Black-Scholes"""
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return d1, d2
    
    def calculate_black_scholes_price(self, S, K, T, r, sigma, option_type='call'):
        """Calcul du prix d'une option européenne avec Black-Scholes"""
        d1, d2 = self.calculate_d1_d2(S, K, T, r, sigma)
        
        if option_type.lower() == 'call':
            price = S * self.normal_cdf(d1) - K * math.exp(-r * T) * self.normal_cdf(d2)
        else:  # put
            price = K * math.exp(-r * T) * self.normal_cdf(-d2) - S * self.normal_cdf(-d1)
        
        return price
    
    def calculate_payoff(self, S, K, option_type='call'):
        """Calcul du payoff à l'échéance"""
        if option_type.lower() == 'call':
            return max(0, S - K)
        else:  # put
            return max(0, K - S)
    
    def calculate_delta(self, S, K, T, r, sigma, option_type='call'):
        """Calcul du Delta (sensibilité au prix du sous-jacent)"""
        d1, _ = self.calculate_d1_d2(S, K, T, r, sigma)
        
        if option_type.lower() == 'call':
            return self.normal_cdf(d1)
        else:  # put
            return self.normal_cdf(d1) - 1
    
    def calculate_gamma(self, S, K, T, r, sigma):
        """Calcul du Gamma (sensibilité du Delta au prix du sous-jacent)"""
        d1, _ = self.calculate_d1_d2(S, K, T, r, sigma)
        return self.normal_pdf(d1) / (S * sigma * math.sqrt(T))
    
    def calculate_theta(self, S, K, T, r, sigma, option_type='call'):
        """Calcul du Theta (sensibilité au temps)"""
        d1, d2 = self.calculate_d1_d2(S, K, T, r, sigma)
        
        term1 = -(S * self.normal_pdf(d1) * sigma) / (2 * math.sqrt(T))
        
        if option_type.lower() == 'put':
            # Formule correcte pour les puts : term1 + r*K*exp(-r*T)*N(-d2)
            term2 = r * K * math.exp(-r * T) * self.normal_cdf(-d2)
            theta = term1 + term2
        else:  # call
            # Formule pour les calls : term1 - r*K*exp(-r*T)*N(d2)
            term2 = -r * K * math.exp(-r * T) * self.normal_cdf(d2)
            theta = term1 + term2
        
        # Conversion en sensibilité à un changement de 1 jour de trading (1/252)
        return theta * (1.0 / 252.0)
    
    def calculate_vega(self, S, K, T, r, sigma):
        """Calcul du Vega (sensibilité à la volatilité)"""
        d1, _ = self.calculate_d1_d2(S, K, T, r, sigma)
        vega = S * self.normal_pdf(d1) * math.sqrt(T)
        
        # Conversion en sensibilité à un changement de 1% dans la volatilité
        return vega * 0.01
    
    def calculate_rho(self, S, K, T, r, sigma, option_type='call'):
        """Calcul du Rho (sensibilité au taux d'intérêt)"""
        d1, d2 = self.calculate_d1_d2(S, K, T, r, sigma)
        
        if option_type.lower() == 'call':
            rho = K * T * math.exp(-r * T) * self.normal_cdf(d2)
        else:  # put
            rho = -K * T * math.exp(-r * T) * self.normal_cdf(-d2)
        
        # Conversion en sensibilité à un changement de 1% dans le taux d'intérêt
        return rho * 0.01
    
    def generate_greek_curves(self, S, K, T, r, sigma, option_type='call', spot_range=None):
        """
        Génère les courbes pour tous les Greeks sur une plage de prix spot
        
        Args:
            S: Prix spot actuel
            K: Prix d'exercice
            T: Temps jusqu'à l'échéance
            r: Taux sans risque
            sigma: Volatilité
            option_type: Type d'option ('call' ou 'put')
            spot_range: Plage de prix spot (défaut: 0 à max(S,K)*2)
        
        Returns:
            dict: Dictionnaire contenant les courbes pour chaque Greek
        """
        if spot_range is None:
            # Générer une plage dynamique de 0 à max(S,K)*2
            max_value = max(S, K)
            x_max = max_value * 2
            step = max(0.5, x_max / 100)  # Pas adaptatif pour avoir environ 100 points
            spot_range = np.arange(0, x_max + step, step)
        
        curves = {
            'spot_prices': spot_range.tolist(),
            'payoff': [],
            'option_price': [],
            'delta': [],
            'gamma': [],
            'theta': [],
            'vega': [],
            'rho': []
        }
        
        for i, S in enumerate(spot_range):
            # Éviter les valeurs nulles ou négatives
            S = max(S, 0.01)
            
            # Calculer tous les Greeks
            curves['payoff'].append(self.calculate_payoff(S, K, option_type))
            curves['option_price'].append(self.calculate_black_scholes_price(S, K, T, r, sigma, option_type))
            curves['delta'].append(self.calculate_delta(S, K, T, r, sigma, option_type))
            curves['gamma'].append(self.calculate_gamma(S, K, T, r, sigma))
            
            # Calcul du Theta
            theta_value = self.calculate_theta(S, K, T, r, sigma, option_type)
            curves['theta'].append(theta_value)
            
            curves['vega'].append(self.calculate_vega(S, K, T, r, sigma))
            curves['rho'].append(self.calculate_rho(S, K, T, r, sigma, option_type))
        
        return curves
    
    def get_greek_values_at_spot(self, S, K, T, r, sigma, option_type='call'):
        """
        Calcule toutes les valeurs des Greeks pour un prix spot donné
        
        Returns:
            dict: Dictionnaire avec toutes les valeurs des Greeks
        """
        return {
            'payoff': self.calculate_payoff(S, K, option_type),
            'option_price': self.calculate_black_scholes_price(S, K, T, r, sigma, option_type),
            'delta': self.calculate_delta(S, K, T, r, sigma, option_type),
            'gamma': self.calculate_gamma(S, K, T, r, sigma),
            'theta': self.calculate_theta(S, K, T, r, sigma, option_type),
            'vega': self.calculate_vega(S, K, T, r, sigma),
            'rho': self.calculate_rho(S, K, T, r, sigma, option_type)
        }
    
    def generate_volatility_sensitivity_matrix(self, S, K, T, r, base_volatility, option_type='call', 
                                             volatility_range=0.1, num_points=7):
        """
        Génère une matrice de sensibilité des Greeks pour différentes valeurs de volatilité
        
        Args:
            S: Prix spot de l'actif sous-jacent
            K: Prix d'exercice
            T: Temps jusqu'à l'échéance
            r: Taux sans risque
            base_volatility: Volatilité de base (ex: 0.20)
            option_type: Type d'option ('call' ou 'put')
            volatility_range: Plage de variation autour de la volatilité de base (ex: 0.1 pour ±10%)
            num_points: Nombre de points à calculer (doit être impair pour inclure la valeur de base)
        
        Returns:
            dict: Dictionnaire contenant les matrices de sensibilité pour chaque Greek
        """
        # Nouvelle logique automatique :
        # Min: max(valeur_utilisateur - 0.10, 0.05)
        # Max: valeur_utilisateur + 0.20
        # Pas: 0.05
        min_volatility = max(base_volatility - 0.10, 0.05)
        max_volatility = base_volatility + 0.20
        step = 0.05
        
        # Générer les valeurs de volatilité
        volatility_values = []
        vol = min_volatility
        while vol <= max_volatility:
            volatility_values.append(round(vol, 3))
            vol += step
        
        # Générer une plage de prix spot pour les courbes
        max_value = max(S, K)
        x_max = max_value * 2
        spot_step = max(0.5, x_max / 100)  # Pas adaptatif pour avoir environ 100 points
        spot_range = np.arange(0, x_max + spot_step, spot_step)
        
        # Matrices pour stocker les résultats
        matrices = {
            'volatility_values': volatility_values,
            'spot_prices': spot_range.tolist(),
            'curves_by_volatility': {}
        }
        
        # Calculer les courbes complètes pour chaque valeur de volatilité
        for vol in volatility_values:
            # S'assurer que la volatilité est positive
            vol = max(vol, 0.001)
            
            # Générer les courbes pour cette volatilité
            curves = {
                'delta': [],
                'gamma': [],
                'theta': [],
                'vega': [],
                'rho': [],
                'option_price': []
            }
            
            for spot_price in spot_range:
                # Éviter les valeurs nulles ou négatives
                spot_price = max(spot_price, 0.01)
                
                curves['delta'].append(self.calculate_delta(spot_price, K, T, r, vol, option_type))
                curves['gamma'].append(self.calculate_gamma(spot_price, K, T, r, vol))
                curves['theta'].append(self.calculate_theta(spot_price, K, T, r, vol, option_type))
                curves['vega'].append(self.calculate_vega(spot_price, K, T, r, vol))
                curves['rho'].append(self.calculate_rho(spot_price, K, T, r, vol, option_type))
                curves['option_price'].append(self.calculate_black_scholes_price(spot_price, K, T, r, vol, option_type))
            
            matrices['curves_by_volatility'][vol] = curves
        
        # Calculer aussi les valeurs au prix spot actuel pour chaque volatilité
        matrices['values_at_spot'] = {}
        for vol in volatility_values:
            vol = max(vol, 0.001)
            matrices['values_at_spot'][vol] = {
                'delta': self.calculate_delta(S, K, T, r, vol, option_type),
                'gamma': self.calculate_gamma(S, K, T, r, vol),
                'theta': self.calculate_theta(S, K, T, r, vol, option_type),
                'vega': self.calculate_vega(S, K, T, r, vol),
                'rho': self.calculate_rho(S, K, T, r, vol, option_type),
                'option_price': self.calculate_black_scholes_price(S, K, T, r, vol, option_type)
            }
        
        return matrices
    
    def generate_maturity_sensitivity_matrix(self, S, K, T, r, sigma, option_type='call', maturity_range=0.9, num_points=6):
        """
        Génère une matrice de sensibilité des Greeks selon la maturité
        
        Args:
            S: Prix spot actuel
            K: Prix d'exercice
            T: Maturité de base (années)
            r: Taux sans risque
            sigma: Volatilité
            option_type: Type d'option ('call' ou 'put')
            maturity_range: Plage de maturité (±années par rapport à T)
            num_points: Nombre de points de maturité à calculer
        
        Returns:
            dict: Matrice de sensibilité avec les courbes pour chaque maturité
        """
        # Générer la plage de maturités : de 0.1 à T + 1.0 par pas de 0.2
        maturity_values = []
        start_maturity = 0.1
        end_maturity = T + 1.0
        step = 0.2
        
        current_maturity = start_maturity
        while current_maturity <= end_maturity:
            rounded_maturity = round(current_maturity, 1)
            maturity_values.append(rounded_maturity)
            current_maturity += step
        
        # S'assurer que la maturité utilisateur exacte est incluse
        user_maturity_rounded = round(T, 1)
        
        # Ajouter la maturité utilisateur si elle n'est pas déjà présente
        if user_maturity_rounded not in maturity_values:
            maturity_values.append(user_maturity_rounded)
            maturity_values.sort()  # Trier pour maintenir l'ordre
        
        # Normaliser toutes les maturités pour éviter les problèmes de type
        # Convertir toutes les maturités en float pour assurer la cohérence
        maturity_values = [float(m) for m in maturity_values]
        maturity_values.sort()
        
        # Générer la plage de prix spot
        max_value = max(S, K)
        x_max = max_value * 2
        step_spot = max(0.5, x_max / 100)
        spot_prices = np.arange(0, x_max + step_spot, step_spot)
        
        # Initialiser la matrice
        matrices = {
            'maturity_values': maturity_values,
            'spot_prices': spot_prices.tolist(),
            'curves_by_maturity': {}
        }
        
        # Calculer les courbes pour chaque maturité
        for maturity in maturity_values:
            curves = {
                'payoff': [],
                'option_price': [],
                'delta': [],
                'gamma': [],
                'theta': [],
                'vega': [],
                'rho': []
            }
            
            for spot in spot_prices:
                spot = max(spot, 0.01)  # Éviter les prix nuls ou négatifs
                
                # Calculer tous les Greeks pour cette maturité
                curves['payoff'].append(self.calculate_payoff(spot, K, option_type))
                curves['option_price'].append(self.calculate_black_scholes_price(spot, K, maturity, r, sigma, option_type))
                curves['delta'].append(self.calculate_delta(spot, K, maturity, r, sigma, option_type))
                curves['gamma'].append(self.calculate_gamma(spot, K, maturity, r, sigma))
                curves['theta'].append(self.calculate_theta(spot, K, maturity, r, sigma, option_type))
                curves['vega'].append(self.calculate_vega(spot, K, maturity, r, sigma))
                curves['rho'].append(self.calculate_rho(spot, K, maturity, r, sigma, option_type))
            
            # Stocker avec la maturité comme clé float pour assurer la cohérence
            matrices['curves_by_maturity'][float(maturity)] = curves
        
        return matrices

# Instance globale du calculateur
greeks_calculator = GreeksCalculator()
