#!/usr/bin/env python3
"""
Script pour extraire la volatilité implicite des options
Utilise Yahoo Finance pour récupérer les données d'options
"""

import yfinance as yf
import pandas as pd
import time


def get_implied_volatility(ticker: str, expiration: str):
    """
    Récupère la volatilité implicite des options pour un ticker et une date d'expiration donnés.
    
    Args:
        ticker (str): Le symbole du titre (ex: "AAPL")
        expiration (str): La date d'expiration des options (ex: "2024-01-19")
    
    Returns:
        pd.DataFrame: DataFrame contenant les données de volatilité implicite
    """
    # Créer un objet Ticker
    ticker_obj = yf.Ticker(ticker)
    
    try:
        print(f"Tentative de récupération des options pour {ticker} - expiration: {expiration}")
        
        # Récupérer la chaîne d'options
        options_chain = ticker_obj.option_chain(expiration)
        
        print(f"Chaîne d'options récupérée avec succès")
        print(f"Nombre de calls: {len(options_chain.calls)}")
        print(f"Nombre de puts: {len(options_chain.puts)}")
        
        # Extraire les calls et puts
        calls = options_chain.calls
        puts = options_chain.puts
        
        # Vérifier si les colonnes existent
        required_columns = ["contractSymbol", "strike", "lastPrice", "impliedVolatility"]
        
        print(f"Colonnes disponibles dans calls: {list(calls.columns)}")
        print(f"Colonnes disponibles dans puts: {list(puts.columns)}")
        
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
        
        print(f"DataFrame final créé avec {len(combined_df)} lignes")
        
        return combined_df
        
    except Exception as e:
        print(f"Erreur détaillée lors de la récupération des données d'options: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


if __name__ == "__main__":
    # Exemple d'utilisation
    ticker = "AAPL"
    
    try:
        print("Début du test de récupération des données d'options...")
        
        # Récupérer la première date d'expiration disponible
        ticker_obj = yf.Ticker(ticker)
        print(f"Objet Ticker créé pour {ticker}")
        
        # Ajouter un délai pour éviter les problèmes de rate limiting
        time.sleep(1)
        
        available_expirations = ticker_obj.options
        print(f"Dates d'expiration disponibles: {available_expirations}")
        
        if available_expirations:
            first_expiration = available_expirations[0]
            print(f"Ticker: {ticker}")
            print(f"Date d'expiration utilisée: {first_expiration}")
            print("-" * 50)
            
            # Ajouter un délai avant la prochaine requête
            time.sleep(1)
            
            # Récupérer la volatilité implicite
            volatility_data = get_implied_volatility(ticker, first_expiration)
            
            if not volatility_data.empty:
                print("Données de volatilité implicite:")
                print(volatility_data.head(10))  # Afficher seulement les 10 premières lignes
                print(f"\nNombre total d'options: {len(volatility_data)}")
                print(f"Nombre de calls: {len(volatility_data[volatility_data['type'] == 'call'])}")
                print(f"Nombre de puts: {len(volatility_data[volatility_data['type'] == 'put'])}")
                
                # Afficher quelques statistiques
                print(f"\nStatistiques de volatilité implicite:")
                print(f"Min: {volatility_data['impliedVolatility'].min():.4f}")
                print(f"Max: {volatility_data['impliedVolatility'].max():.4f}")
                print(f"Moyenne: {volatility_data['impliedVolatility'].mean():.4f}")
            else:
                print("Aucune donnée de volatilité implicite trouvée.")
        else:
            print(f"Aucune date d'expiration disponible pour {ticker}")
            
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()
