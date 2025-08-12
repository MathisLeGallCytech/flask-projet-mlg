#!/usr/bin/env python3
"""
Script final pour extraire la volatilité implicite des options
Utilise Yahoo Finance avec fallback vers des données simulées
"""

import pandas as pd
import numpy as np
import time


def create_simulated_options_data(ticker: str, expiration: str):
    """
    Crée des données d'options simulées pour tester la logique
    """
    # Prix actuel simulé
    current_price = 150.0
    
    # Créer des strikes autour du prix actuel
    strikes = np.arange(current_price - 20, current_price + 21, 5)
    
    # Créer des données pour les calls
    calls_data = []
    for strike in strikes:
        # Volatilité implicite simulée (plus élevée pour les strikes éloignés)
        moneyness = abs(current_price - strike) / current_price
        implied_vol = 0.2 + 0.1 * moneyness + np.random.normal(0, 0.02)
        implied_vol = max(0.05, min(0.5, implied_vol))  # Limiter entre 5% et 50%
        
        # Prix simulé basé sur le modèle Black-Scholes simplifié
        if strike < current_price:
            # In-the-money call
            intrinsic_value = current_price - strike
            time_value = 5.0 + np.random.normal(0, 1)
            last_price = max(intrinsic_value + time_value, 0.01)
        else:
            # Out-of-the-money call
            time_value = max(0.01, 10.0 * np.exp(-(strike - current_price) / 10))
            last_price = time_value
        
        calls_data.append({
            'contractSymbol': f'{ticker}{expiration.replace("-", "")}C{int(strike)}',
            'strike': strike,
            'lastPrice': round(last_price, 2),
            'impliedVolatility': round(implied_vol, 4)
        })
    
    # Créer des données pour les puts
    puts_data = []
    for strike in strikes:
        # Volatilité implicite simulée
        moneyness = abs(current_price - strike) / current_price
        implied_vol = 0.25 + 0.15 * moneyness + np.random.normal(0, 0.02)
        implied_vol = max(0.05, min(0.6, implied_vol))  # Limiter entre 5% et 60%
        
        # Prix simulé
        if strike > current_price:
            # In-the-money put
            intrinsic_value = strike - current_price
            time_value = 5.0 + np.random.normal(0, 1)
            last_price = max(intrinsic_value + time_value, 0.01)
        else:
            # Out-of-the-money put
            time_value = max(0.01, 8.0 * np.exp(-(current_price - strike) / 10))
            last_price = time_value
        
        puts_data.append({
            'contractSymbol': f'{ticker}{expiration.replace("-", "")}P{int(strike)}',
            'strike': strike,
            'lastPrice': round(last_price, 2),
            'impliedVolatility': round(implied_vol, 4)
        })
    
    return pd.DataFrame(calls_data), pd.DataFrame(puts_data)


def get_implied_volatility(ticker: str, expiration: str, force_simulated=False):
    """
    Récupère la volatilité implicite des options pour un ticker et une date d'expiration donnés.
    
    Args:
        ticker (str): Le symbole du titre (ex: "AAPL")
        expiration (str): La date d'expiration des options (ex: "2024-01-19")
        force_simulated (bool): Si True, force l'utilisation de données simulées
    
    Returns:
        pd.DataFrame: DataFrame contenant les données de volatilité implicite
    """
    
    if not force_simulated:
        # Essayer d'abord avec les vraies données Yahoo Finance
        try:
            import yfinance as yf
            
            print(f"Tentative de récupération des vraies données pour {ticker} - expiration: {expiration}")
            
            # Créer un objet Ticker
            ticker_obj = yf.Ticker(ticker)
            
            # Ajouter un délai pour éviter les problèmes de rate limiting
            time.sleep(1)
            
            # Récupérer la chaîne d'options
            options_chain = ticker_obj.option_chain(expiration)
            
            print(f"✅ Données réelles récupérées avec succès")
            print(f"  - Calls: {len(options_chain.calls)} contrats")
            print(f"  - Puts: {len(options_chain.puts)} contrats")
            
            # Extraire les calls et puts
            calls = options_chain.calls
            puts = options_chain.puts
            
            # Vérifier si les colonnes nécessaires existent
            required_columns = ["contractSymbol", "strike", "lastPrice", "impliedVolatility"]
            
            if not all(col in calls.columns for col in required_columns):
                print("⚠️ Colonnes manquantes dans les calls, utilisation de données simulées")
                raise Exception("Colonnes manquantes")
            
            if not all(col in puts.columns for col in required_columns):
                print("⚠️ Colonnes manquantes dans les puts, utilisation de données simulées")
                raise Exception("Colonnes manquantes")
            
            # Sélectionner uniquement les colonnes nécessaires pour les calls
            calls_filtered = calls[required_columns].copy()
            calls_filtered['type'] = 'call'
            
            # Sélectionner uniquement les colonnes nécessaires pour les puts
            puts_filtered = puts[required_columns].copy()
            puts_filtered['type'] = 'put'
            
            # Remplacer les valeurs NaN par 0 dans impliedVolatility
            calls_filtered['impliedVolatility'] = calls_filtered['impliedVolatility'].fillna(0)
            puts_filtered['impliedVolatility'] = puts_filtered['impliedVolatility'].fillna(0)
            
            # Concaténer les deux DataFrames
            combined_df = pd.concat([calls_filtered, puts_filtered], ignore_index=True)
            
            # Trier par strike croissant
            combined_df = combined_df.sort_values('strike')
            
            print(f"✅ DataFrame final créé avec {len(combined_df)} lignes (données réelles)")
            
            return combined_df
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données réelles: {e}")
            print("🔄 Basculement vers les données simulées...")
    
    # Utiliser des données simulées
    print(f"Utilisation de données simulées pour {ticker} - expiration: {expiration}")
    
    # Créer des données simulées
    calls, puts = create_simulated_options_data(ticker, expiration)
    
    print(f"Données simulées créées:")
    print(f"  - Calls: {len(calls)} contrats")
    print(f"  - Puts: {len(puts)} contrats")
    
    # Ajouter la colonne type
    calls['type'] = 'call'
    puts['type'] = 'put'
    
    # Concaténer les deux DataFrames
    combined_df = pd.concat([calls, puts], ignore_index=True)
    
    # Trier par strike croissant
    combined_df = combined_df.sort_values('strike')
    
    print(f"✅ DataFrame final créé avec {len(combined_df)} lignes (données simulées)")
    
    return combined_df


def get_available_expirations(ticker: str):
    """
    Récupère les dates d'expiration disponibles pour un ticker
    """
    try:
        import yfinance as yf
        
        ticker_obj = yf.Ticker(ticker)
        time.sleep(1)  # Délai pour éviter le rate limiting
        
        expirations = ticker_obj.options
        if expirations:
            return expirations
        else:
            # Retourner des dates simulées si aucune n'est disponible
            return ["2024-01-19", "2024-02-16", "2024-03-15"]
            
    except Exception as e:
        print(f"Erreur lors de la récupération des expirations: {e}")
        # Retourner des dates simulées
        return ["2024-01-19", "2024-02-16", "2024-03-15"]


if __name__ == "__main__":
    # Exemple d'utilisation
    ticker = "AAPL"
    
    print("🔍 Extraction de volatilité implicite des options")
    print("=" * 60)
    
    try:
        # Récupérer les dates d'expiration disponibles
        available_expirations = get_available_expirations(ticker)
        
        if available_expirations:
            first_expiration = available_expirations[0]
            print(f"Ticker: {ticker}")
            print(f"Date d'expiration utilisée: {first_expiration}")
            print("-" * 50)
            
            # Récupérer la volatilité implicite
            volatility_data = get_implied_volatility(ticker, first_expiration)
            
            if not volatility_data.empty:
                print(f"\n✅ Données de volatilité implicite récupérées avec succès!")
                
                # Afficher les données
                print("\nDonnées de volatilité implicite (premières 10 lignes):")
                print(volatility_data.head(10))
                
                print(f"\nStatistiques:")
                print(f"Nombre total d'options: {len(volatility_data)}")
                print(f"Nombre de calls: {len(volatility_data[volatility_data['type'] == 'call'])}")
                print(f"Nombre de puts: {len(volatility_data[volatility_data['type'] == 'put'])}")
                
                # Statistiques de volatilité implicite
                print(f"\nStatistiques de volatilité implicite:")
                print(f"Min: {volatility_data['impliedVolatility'].min():.4f}")
                print(f"Max: {volatility_data['impliedVolatility'].max():.4f}")
                print(f"Moyenne: {volatility_data['impliedVolatility'].mean():.4f}")
                print(f"Écart-type: {volatility_data['impliedVolatility'].std():.4f}")
                
                # Afficher quelques exemples par type
                calls_data = volatility_data[volatility_data['type'] == 'call']
                puts_data = volatility_data[volatility_data['type'] == 'put']
                
                print(f"\nExemples de calls:")
                print(calls_data.head(5)[['strike', 'lastPrice', 'impliedVolatility']])
                
                print(f"\nExemples de puts:")
                print(puts_data.head(5)[['strike', 'lastPrice', 'impliedVolatility']])
                
            else:
                print("❌ Aucune donnée de volatilité implicite trouvée.")
        else:
            print(f"❌ Aucune date d'expiration disponible pour {ticker}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()


