import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class PolarizationVisualizer:
    @staticmethod
    def create_heatmap(data: np.ndarray, title: str, colorscale: str = 'hot'):
        """Create an interactive heatmap using Plotly"""
        fig = px.imshow(data, color_continuous_scale=colorscale, title=title)
        fig.update_layout(coloraxis_showscale=True)
        return fig
    
    @staticmethod
    def create_comprehensive_plots(metrics: dict):
        """Create a comprehensive dashboard of all polarization metrics"""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Degree of Polarization', 'Orientation Angle', 
                          'Ellipticity Angle', 'S0 - Intensity', 'S1', 'S2'),
            specs=[[{}, {}, {}],
                   [{}, {}, {}]]
        )
        
        # DOP
        fig.add_trace(go.Heatmap(z=metrics['dop'], colorscale='hot', showscale=False), row=1, col=1)
        # Orientation Angle
        fig.add_trace(go.Heatmap(z=metrics['orientation_angle'], colorscale='hsv', showscale=False), row=1, col=2)
        # Ellipticity Angle
        fig.add_trace(go.Heatmap(z=metrics['ellipticity_angle'], colorscale='RdYlBu', showscale=False), row=1, col=3)
        # S0
        fig.add_trace(go.Heatmap(z=metrics['S0'], colorscale='gray', showscale=False), row=2, col=1)
        # S1
        fig.add_trace(go.Heatmap(z=metrics['S1'], colorscale='rdbu', showscale=False), row=2, col=2)
        fig.add_trace(go.Heatmap(z=metrics['S2'], colorscale='picnic', showscale=False), row=2, col=3)
        
        fig.update_layout(height=600, showlegend=False, title_text="Polarization Analysis Dashboard")
        return fig