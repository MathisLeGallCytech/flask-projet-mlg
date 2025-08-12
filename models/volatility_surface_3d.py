import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
import json


class VolatilitySurface3D:
    """
    Classe dédiée à la création et gestion des graphiques 3D de surface de volatilité implicite.
    Utilise Plotly pour générer des visualisations interactives avec fond transparent.
    """
    
    def __init__(self, symbol: str = ""):
        """
        Initialise la classe de visualisation 3D.
        
        Args:
            symbol (str): Le symbole de l'actif sous-jacent
        """
        self.symbol = symbol
        self.data = None
        self.layout_config = {
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Fond transparent
            'plot_bgcolor': 'rgba(0,0,0,0)',   # Fond transparent
            'font': {'color': '#ffffff'},
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 50}
        }
    
    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Définit les données pour la visualisation.
        
        Args:
            data (Dict): Dictionnaire contenant les données de volatilité
                - 'strikes': Liste des prix d'exercice
                - 'maturities': Liste des maturités (en années)
                - 'iv': Matrice 2D des volatilités implicites
                - 'spot_price': Prix spot (optionnel)
        """
        self.data = data
    
    def create_surface_plot(self, 
                          colorscale: str = 'Viridis',
                          show_spot_line: bool = True,
                          show_contours: bool = True) -> go.Figure:
        """
        Crée un graphique 3D de surface de volatilité.
        
        Args:
            colorscale (str): Échelle de couleurs pour la surface
            show_spot_line (bool): Afficher une ligne au niveau du prix spot
            show_contours (bool): Afficher les contours sur les axes
            
        Returns:
            go.Figure: Figure Plotly avec la surface 3D
        """
        if not self.data or not self._validate_data():
            raise ValueError("Données invalides ou manquantes pour créer la surface 3D")
        
        # Préparer les données
        x = self.data['strikes']
        y = self.data['maturities']
        z = self.data['iv']
        
        # Convertir les strikes en pourcentages par rapport au prix spot
        if 'spot_price' in self.data and self.data['spot_price']:
            spot_price = self.data['spot_price']
            x_percent = [(strike / spot_price - 1) * 100 for strike in x]
            x_display = x_percent
            hover_x_format = '%{x:.1f}%'
        else:
            x_display = x
            hover_x_format = '$%{x}'
        
        # Créer la trace de surface principale
        surface_trace = go.Surface(
            x=x_display,
            y=y,
            z=z,
            colorscale=colorscale,
            name='Volatilité Implicite',
            hovertemplate=(
                f'<b>Strike:</b> {hover_x_format}<br>' +
                '<b>Maturité:</b> %{y:.2f} ans<br>' +
                '<b>IV:</b> %{z:.2%}<br>' +
                '<extra></extra>'
            ),
            showscale=True,
            colorbar=dict(
                title="Volatilité Implicite",
                titleside="right",
                tickformat=".1%",
                len=0.8
            )
        )
        
        traces = [surface_trace]
        
        # Ajouter la ligne du prix spot si demandé et disponible
        if show_spot_line and 'spot_price' in self.data and self.data['spot_price']:
            spot_line = self._create_spot_line()
            if spot_line:
                traces.append(spot_line)
        
        # Créer la mise en page
        layout = self._create_layout(show_contours)
        
        # Créer la figure
        fig = go.Figure(data=traces, layout=layout)
        
        return fig
    
    def create_heatmap_plot(self, colorscale: str = 'Viridis') -> go.Figure:
        """
        Crée un graphique heatmap 2D de la surface de volatilité.
        
        Args:
            colorscale (str): Échelle de couleurs pour le heatmap
            
        Returns:
            go.Figure: Figure Plotly avec le heatmap
        """
        if not self.data or not self._validate_data():
            raise ValueError("Données invalides ou manquantes pour créer le heatmap")
        
        # Convertir les strikes en pourcentages par rapport au prix spot
        x = self.data['strikes']
        if 'spot_price' in self.data and self.data['spot_price']:
            spot_price = self.data['spot_price']
            x_percent = [(strike / spot_price - 1) * 100 for strike in x]
            x_display = x_percent
            hover_x_format = '%{x:.1f}%'
        else:
            x_display = x
            hover_x_format = '$%{x}'
        
        # Créer le heatmap
        fig = go.Figure(data=go.Heatmap(
            x=x_display,
            y=self.data['maturities'],
            z=self.data['iv'],
            colorscale=colorscale,
            hovertemplate=(
                f'<b>Strike:</b> {hover_x_format}<br>' +
                '<b>Maturité:</b> %{y:.2f} ans<br>' +
                '<b>IV:</b> %{z:.2%}<br>' +
                '<extra></extra>'
            ),
            colorbar=dict(
                title="Volatilité Implicite",
                titleside="right",
                tickformat=".1%"
            )
        ))
        
        # Mise en page
        fig.update_layout(
            title=f"Surface de Volatilité Implicite - {self.symbol}",
            xaxis_title="Strike (% du prix spot)",
            yaxis_title="Maturité (années)",
            **self.layout_config
        )
        
        return fig
    
    def create_comparison_plot(self, 
                             data_sources: Dict[str, Dict],
                             colorscale: str = 'Viridis') -> go.Figure:
        """
        Crée un graphique de comparaison entre plusieurs sources de données.
        
        Args:
            data_sources (Dict): Dictionnaire des sources avec leurs données
            colorscale (str): Échelle de couleurs
            
        Returns:
            go.Figure: Figure Plotly avec les surfaces comparées
        """
        traces = []
        colors = ['Viridis', 'Plasma', 'Inferno', 'Magma']
        
        for i, (source_name, source_data) in enumerate(data_sources.items()):
            if not self._validate_source_data(source_data):
                continue
            
            # Convertir les strikes en pourcentages si le prix spot est disponible
            x = source_data['strikes']
            if 'spot_price' in source_data and source_data['spot_price']:
                spot_price = source_data['spot_price']
                x_percent = [(strike / spot_price - 1) * 100 for strike in x]
                x_display = x_percent
                hover_x_format = '%{x:.1f}%'
            else:
                x_display = x
                hover_x_format = '$%{x}'
                
            trace = go.Surface(
                x=x_display,
                y=source_data['maturities'],
                z=source_data['iv'],
                colorscale=colors[i % len(colors)],
                name=source_name,
                opacity=0.7,
                hovertemplate=(
                    f'<b>{source_name}</b><br>' +
                    f'<b>Strike:</b> {hover_x_format}<br>' +
                    '<b>Maturité:</b> %{y:.2f} ans<br>' +
                    '<b>IV:</b> %{z:.2%}<br>' +
                    '<extra></extra>'
                )
            )
            traces.append(trace)
        
        if not traces:
            raise ValueError("Aucune donnée valide trouvée pour la comparaison")
        
        layout = self._create_layout(show_contours=False)
        layout['title'] = f"Comparaison des Surfaces de Volatilité - {self.symbol}"
        
        fig = go.Figure(data=traces, layout=layout)
        return fig
    
    def get_plot_config(self) -> Dict[str, Any]:
        """
        Retourne la configuration Plotly pour l'affichage.
        
        Returns:
            Dict: Configuration pour Plotly.newPlot
        """
        return {
            'responsive': True,
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'volatility_surface_{self.symbol}',
                'height': 800,
                'width': 1200,
                'scale': 2
            }
        }
    
    def export_to_html(self, 
                      filename: str = None,
                      include_plotlyjs: bool = True) -> str:
        """
        Exporte le graphique en HTML.
        
        Args:
            filename (str): Nom du fichier (optionnel)
            include_plotlyjs (bool): Inclure Plotly.js dans le fichier
            
        Returns:
            str: Contenu HTML du graphique
        """
        if not filename:
            filename = f"volatility_surface_{self.symbol}.html"
        
        fig = self.create_surface_plot()
        return fig.to_html(
            filename=filename,
            include_plotlyjs=include_plotlyjs,
            config=self.get_plot_config()
        )
    
    def _validate_data(self) -> bool:
        """Valide les données de volatilité."""
        required_keys = ['strikes', 'maturities', 'iv']
        
        if not all(key in self.data for key in required_keys):
            return False
        
        if not self.data['strikes'] or not self.data['maturities'] or not self.data['iv']:
            return False
        
        # Vérifier que les dimensions correspondent
        if len(self.data['iv']) != len(self.data['maturities']):
            return False
        
        if len(self.data['iv'][0]) != len(self.data['strikes']):
            return False
        
        return True
    
    def _validate_source_data(self, source_data: Dict) -> bool:
        """Valide les données d'une source spécifique."""
        try:
            return self._validate_data()
        except:
            return False
    
    def _create_layout(self, show_contours: bool = True) -> Dict[str, Any]:
        """Crée la mise en page pour le graphique 3D."""
        layout = {
            'title': f"Surface de Volatilité Implicite - {self.symbol}",
            'scene': {
                'xaxis': {
                    'title': 'Strike (% du prix spot)',
                    'gridcolor': '#444',
                    'zerolinecolor': '#666',
                    'showbackground': False
                },
                'yaxis': {
                    'title': 'Maturité (années)',
                    'gridcolor': '#444',
                    'zerolinecolor': '#666',
                    'showbackground': False
                },
                'zaxis': {
                    'title': 'Volatilité Implicite',
                    'gridcolor': '#444',
                    'zerolinecolor': '#666',
                    'tickformat': '.1%',
                    'showbackground': False
                },
                'camera': {
                    'eye': {'x': 1.5, 'y': 1.5, 'z': 1.5}
                },
                'bgcolor': 'rgba(0,0,0,0)'  # Fond transparent
            },
            **self.layout_config
        }
        
        # Ajouter les contours si demandé
        if show_contours:
            layout['scene']['xaxis']['contours'] = {'show': True, 'color': '#666'}
            layout['scene']['yaxis']['contours'] = {'show': True, 'color': '#666'}
            layout['scene']['zaxis']['contours'] = {'show': True, 'color': '#666'}
        
        return layout
    
    def _create_spot_line(self) -> Optional[go.Scatter3d]:
        """Crée une ligne au niveau du prix spot."""
        if not self.data.get('spot_price'):
            return None
        
        spot_price = self.data['spot_price']
        min_maturity = min(self.data['maturities'])
        max_maturity = max(self.data['maturities'])
        
        # Créer une ligne verticale au niveau du spot (0% en pourcentage)
        return go.Scatter3d(
            x=[0, 0],  # 0% par rapport au prix spot
            y=[min_maturity, max_maturity],
            z=[0, 0.5],  # Plage de volatilité typique
            mode='lines',
            line=dict(color='red', width=3),
            name='Prix Spot',
            hovertemplate=f'<b>Prix Spot:</b> ${spot_price} (0%)<extra></extra>'
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les données de volatilité.
        
        Returns:
            Dict: Statistiques calculées
        """
        if not self.data or not self._validate_data():
            return {}
        
        iv_array = np.array(self.data['iv'])
        
        return {
            'min_iv': float(np.min(iv_array)),
            'max_iv': float(np.max(iv_array)),
            'mean_iv': float(np.mean(iv_array)),
            'std_iv': float(np.std(iv_array)),
            'num_strikes': len(self.data['strikes']),
            'num_maturities': len(self.data['maturities']),
            'spot_price': self.data.get('spot_price', None)
        }
    
    def to_json(self) -> str:
        """
        Convertit les données en JSON.
        
        Returns:
            str: Représentation JSON des données
        """
        return json.dumps({
            'symbol': self.symbol,
            'data': self.data,
            'statistics': self.get_statistics()
        }, indent=2)


# Fonction utilitaire pour créer une instance avec des données
def create_volatility_surface_3d(symbol: str, 
                                strikes: List[float],
                                maturities: List[float],
                                iv_matrix: List[List[float]],
                                spot_price: Optional[float] = None) -> VolatilitySurface3D:
    """
    Fonction utilitaire pour créer une instance de VolatilitySurface3D.
    
    Args:
        symbol (str): Symbole de l'actif
        strikes (List[float]): Liste des prix d'exercice
        maturities (List[float]): Liste des maturités
        iv_matrix (List[List[float]]): Matrice des volatilités implicites
        spot_price (Optional[float]): Prix spot
        
    Returns:
        VolatilitySurface3D: Instance configurée
    """
    vs3d = VolatilitySurface3D(symbol)
    vs3d.set_data({
        'strikes': strikes,
        'maturities': maturities,
        'iv': iv_matrix,
        'spot_price': spot_price
    })
    return vs3d
