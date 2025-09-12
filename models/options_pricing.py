import numpy as np
import math


class OptionPricer:
    """Service de pricing d'options: Monte Carlo (GBM) et Black-Scholes.

    Conçu pour être stateless et réutilisable.
    """

    @staticmethod
    def _validate_mc_inputs(T: float, nb_steps: int, nb_simulations: int) -> None:
        if T <= 0 or nb_steps <= 0 or nb_simulations <= 0:
            raise ValueError("T, nb_steps et nb_simulations doivent être strictement positifs")

    def monte_carlo_price(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str,
        nb_simulations: int,
        nb_steps: int,
        return_std: bool = False,
    ):
        """Monte Carlo (GBM) vectorisé avec NumPy.

        Optimisé: calcule directement la distribution terminale (1 step) pour le pricing
        et utilise nb_steps uniquement si on demande des chemins ailleurs.
        Retourne le prix, et optionnellement l'erreur standard (discounted payoff SE).
        """
        self._validate_mc_inputs(T, max(1, nb_steps), nb_simulations)

        # Terminal distribution exact (1 step)
        Z = np.random.standard_normal(size=(nb_simulations,))
        X = (r - 0.5 * sigma * sigma) * T + sigma * math.sqrt(T) * Z
        ST = S * np.exp(X)

        opt = option_type.lower().strip()
        if opt == "call":
            payoffs = np.maximum(ST - K, 0.0)
        elif opt == "put":
            payoffs = np.maximum(K - ST, 0.0)
        else:
            raise ValueError("option_type doit être 'call' ou 'put'")

        discount = math.exp(-r * T)
        mean_payoff = float(np.mean(payoffs))
        price = discount * mean_payoff

        if not return_std:
            return float(price)

        # Erreur standard du payoff actualisé
        std_payoff = float(np.std(payoffs, ddof=1))
        std_error = discount * (std_payoff / math.sqrt(nb_simulations))
        return float(price), float(std_error)

    def monte_carlo_price_and_greeks(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str,
        nb_simulations: int,
        nb_steps: int,
        bump_relative: float = 0.01,
        bump_relative_sigma: float = 0.01,
        bump_abs_r: float = 1e-4,
        theta_dt: float = None,
        return_std: bool = True,
        return_paths: int = 0,
    ):
        """Monte Carlo: prix + greeks (delta, gamma, theta) par bump-and-revalue avec CRN.

        - delta, gamma: bump sur S (S*(1±ε)) avec mêmes Z (CRN)
        - theta: bump sur T -> T - dT (si possible) avec mêmes Z et nb_steps constant
        - return_paths: renvoie jusqu'à N chemins (N limité à 50) et la grille des temps
        """
        self._validate_mc_inputs(T, nb_steps, nb_simulations)
        eps = max(1e-6, float(bump_relative))
        if theta_dt is None:
            # pas de temps annuel minimal pour theta
            theta_dt = max(T / nb_steps, 1.0 / 365.0)

        # Pricing via terminal distribution (1 step)
        Z = np.random.standard_normal(size=(nb_simulations,))
        X = (r - 0.5 * sigma * sigma) * T + sigma * math.sqrt(T) * Z
        expX = np.exp(X)

        # Prix (base)
        ST = S * expX
        if option_type.lower().strip() == "call":
            payoffs = np.maximum(ST - K, 0.0)
        else:
            payoffs = np.maximum(K - ST, 0.0)
        discount = math.exp(-r * T)
        mean_payoff = float(np.mean(payoffs))
        price = discount * mean_payoff

        # Ecart-type du payoff actualisé
        std_error = None
        if return_std:
            std_payoff = float(np.std(payoffs, ddof=1))
            std_error = discount * (std_payoff / math.sqrt(nb_simulations))

        # Delta/Gamma via bump sur S (CRN)
        S_up = S * (1.0 + eps)
        S_dn = S * (1.0 - eps)
        ST_up = S_up * expX
        ST_dn = S_dn * expX
        if option_type.lower().strip() == "call":
            payoff_up = np.maximum(ST_up - K, 0.0)
            payoff_dn = np.maximum(ST_dn - K, 0.0)
        else:
            payoff_up = np.maximum(K - ST_up, 0.0)
            payoff_dn = np.maximum(K - ST_dn, 0.0)
        price_up = discount * float(np.mean(payoff_up))
        price_dn = discount * float(np.mean(payoff_dn))
        h = eps * S
        delta = (price_up - price_dn) / (2.0 * h)
        gamma = (price_up - 2.0 * price + price_dn) / (h * h)

        # Vega via bump sur sigma (CRN, single-step)
        eps_sig = max(1e-6, float(bump_relative_sigma))
        sigma_up = sigma * (1.0 + eps_sig)
        sigma_dn = sigma * (1.0 - eps_sig)
        Xu = (r - 0.5 * sigma_up * sigma_up) * T + sigma_up * math.sqrt(T) * Z
        Xd = (r - 0.5 * sigma_dn * sigma_dn) * T + sigma_dn * math.sqrt(T) * Z
        STu = S * np.exp(Xu)
        STd = S * np.exp(Xd)
        if option_type.lower().strip() == "call":
            payoff_u = np.maximum(STu - K, 0.0)
            payoff_d = np.maximum(STd - K, 0.0)
        else:
            payoff_u = np.maximum(K - STu, 0.0)
            payoff_d = np.maximum(K - STd, 0.0)
        price_u = math.exp(-r * T) * float(np.mean(payoff_u))
        price_d = math.exp(-r * T) * float(np.mean(payoff_d))
        # Vega: sensibilité à un changement de 1% dans la volatilité (même unité que Black-Scholes)
        # Pour un bump relatif eps_sig, la sensibilité à 1% est:
        # (price_u - price_d) / (2 * eps_sig * sigma) * 0.01
        # où eps_sig * sigma est le bump absolu en volatilité
        vega = (price_u - price_d) / (2.0 * eps_sig * sigma) * 0.01

        # Rho via bump sur r (CRN, single-step)
        dr = max(1e-6, float(bump_abs_r))
        Xru = (r + dr - 0.5 * sigma * sigma) * T + sigma * math.sqrt(T) * Z
        Xrd = (r - dr - 0.5 * sigma * sigma) * T + sigma * math.sqrt(T) * Z
        ST_ru = S * np.exp(Xru)
        ST_rd = S * np.exp(Xrd)
        disc_u = math.exp(-(r + dr) * T)
        disc_d = math.exp(-(r - dr) * T)
        if option_type.lower().strip() == "call":
            payoff_ru = np.maximum(ST_ru - K, 0.0)
            payoff_rd = np.maximum(ST_rd - K, 0.0)
        else:
            payoff_ru = np.maximum(K - ST_ru, 0.0)
            payoff_rd = np.maximum(K - ST_rd, 0.0)
        price_ru = disc_u * float(np.mean(payoff_ru))
        price_rd = disc_d * float(np.mean(payoff_rd))
        # Rho: sensibilité à un changement de 1% dans le taux d'intérêt (même unité que Black-Scholes)
        # Pour un bump de 1 point de base (0.0001), on divise par 0.0001 pour avoir la sensibilité à 1, puis on multiplie par 0.01 pour avoir la sensibilité à 1%
        rho = (price_ru - price_rd) / (2.0 * dr) * 0.01

        # Theta (calendrier) via bump sur T -> T - dT (si possible)
        if T > theta_dt:
            Tm = T - theta_dt
            # Re-use CRN with single-step formula
            Xm = (r - 0.5 * sigma * sigma) * Tm + sigma * math.sqrt(Tm) * Z
            STm = S * np.exp(Xm)
            if option_type.lower().strip() == "call":
                payoff_m = np.maximum(STm - K, 0.0)
            else:
                payoff_m = np.maximum(K - STm, 0.0)
            price_m = math.exp(-r * Tm) * float(np.mean(payoff_m))
            # Theta = dV/dt (calendrier). Quand le temps avance de dt, T diminue de dt.
            # Approximation: theta ≈ (V(T - dt) - V(T)) / dt
            # Conversion en sensibilité à un changement de 1 jour de trading (1/252)
            theta = (price_m - price) / (theta_dt) * (1.0 / 252.0)
        else:
            theta = float('nan')

        # Chemins pour visualisation
        paths = None
        time_grid = None
        n_paths = int(min(max(0, return_paths), 200))
        if n_paths > 0:
            # Construire chemins pour n_paths premières simulations
            max_steps = 300
            steps_used = int(min(max_steps, max(2, nb_steps)))
            dtp = T / steps_used
            Zp = np.random.standard_normal(size=(n_paths, steps_used))
            incp = (r - 0.5 * sigma * sigma) * dtp + sigma * math.sqrt(dtp) * Zp
            csum = np.cumsum(incp, axis=1)
            exp_csum = np.exp(csum)
            paths = (S * np.hstack([np.ones((n_paths, 1)), exp_csum])).tolist()
            time_grid = (np.arange(steps_used + 1) * dtp).tolist()

        out = {
            'price': float(price),
            'delta': float(delta),
            'gamma': float(gamma),
            'theta': float(theta),
            'vega': float(vega),
            'rho': float(rho),
        }
        if return_std:
            out['stdError'] = float(std_error)
        if paths is not None:
            out['paths'] = paths
            out['timeGrid'] = time_grid
        return out

    @staticmethod
    def _normal_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @staticmethod
    def _normal_pdf(x: float) -> float:
        return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

    def black_scholes_price_and_greeks(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str,
    ):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
            raise ValueError("Paramètres invalides pour Black-Scholes")

        d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        is_call = option_type.lower().strip() == "call"
        if is_call:
            price = S * self._normal_cdf(d1) - K * math.exp(-r * T) * self._normal_cdf(d2)
            delta = self._normal_cdf(d1)
        else:
            price = K * math.exp(-r * T) * self._normal_cdf(-d2) - S * self._normal_cdf(-d1)
            delta = self._normal_cdf(d1) - 1.0

        gamma = self._normal_pdf(d1) / (S * sigma * math.sqrt(T))
        
        # Theta (sensibilité à un changement de 1 jour)
        # Formule Black-Scholes correcte pour theta
        if is_call:
            theta = (
                -(S * self._normal_pdf(d1) * sigma) / (2.0 * math.sqrt(T))
                - r * K * math.exp(-r * T) * self._normal_cdf(d2)
            ) * (1.0 / 252.0)  # Conversion en sensibilité à un changement de 1 jour de trading
        else:
            theta = (
                -(S * self._normal_pdf(d1) * sigma) / (2.0 * math.sqrt(T))
                + r * K * math.exp(-r * T) * self._normal_cdf(-d2)
            ) * (1.0 / 252.0)  # Conversion en sensibilité à un changement de 1 jour de trading
        
        # Vega (sensibilité à un changement de 1% dans la volatilité)
        vega = S * self._normal_pdf(d1) * math.sqrt(T) * 0.01
        
        # Rho (sensibilité à un changement de 1% dans le taux d'intérêt)
        if is_call:
            rho = K * T * math.exp(-r * T) * self._normal_cdf(d2) * 0.01
        else:
            rho = -K * T * math.exp(-r * T) * self._normal_cdf(-d2) * 0.01

        return (
            float(price),
            float(delta),
            float(gamma),
            float(theta),
            float(vega),
            float(rho),
        )


# Compatibilité: fonction simple qui s'appuie sur la classe
def monte_carlo_option_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str,
    nb_simulations: int,
    nb_steps: int,
) -> float:
    return OptionPricer().monte_carlo_price(
        S, K, T, r, sigma, option_type, nb_simulations, nb_steps, return_std=False
    )


