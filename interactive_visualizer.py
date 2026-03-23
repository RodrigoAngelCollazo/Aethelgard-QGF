"""
Interactive 3D Visualization Tool for Aethelgard-QGF

This module provides an interactive web-based visualization using Plotly.
Allows real-time exploration of 3D fields, metric components, and quantum effects.

Installation:
    pip install plotly dash

Usage:
    python interactive_visualizer.py
    
Then open your browser to: http://localhost:8050
"""


import warnings

import numpy as np

try:
    import dash
    import plotly.graph_objects as go
    from dash import dcc, html
    from dash.dependencies import Input, Output, State
    from plotly.subplots import make_subplots
    INTERACTIVE_AVAILABLE = True
except ImportError:
    INTERACTIVE_AVAILABLE = False
    warnings.warn(
        "Plotly/Dash not installed. Install with: pip install -r requirements-optional.txt",
        RuntimeWarning,
        stacklevel=2,
    )

from aethelgard_engine import AethelgardEngine


class InteractiveVisualizer:
    """
    Interactive 3D visualizer for Aethelgard-QGF simulations.
    """
    
    def __init__(self, grid_size=32, domain_size=10.0):
        """
        Initialize visualizer.
        
        Parameters:
        -----------
        grid_size : int
            Grid resolution
        domain_size : float
            Domain size in meters
        """
        if not INTERACTIVE_AVAILABLE:
            raise ImportError("Plotly and Dash required. Install with: pip install plotly dash")
        
        self.engine = AethelgardEngine(grid_size=grid_size, domain_size=domain_size)
        self.grid_size = grid_size
        self.domain_size = domain_size
        
        # Create coordinate grids
        x = np.linspace(0, domain_size, grid_size)
        self.X, self.Y, self.Z = np.meshgrid(x, x, x, indexing='ij')
        
        # Storage for current simulation
        self.mass_dist = None
        self.entropy_map = None
        self.metric = None
        self.quantum_pressure = None
        
        # Dash app
        self.app = dash.Dash(__name__)
        self._setup_layout()
        self._setup_callbacks()
    
    def _setup_layout(self):
        """Setup Dash app layout."""
        self.app.layout = html.Div([
            html.H1("Aethelgard-QGF Interactive Visualizer", 
                   style={'textAlign': 'center', 'color': '#2c3e50'}),
            
            html.Div([
                html.H3("Scenario Selection"),
                dcc.Dropdown(
                    id='scenario-dropdown',
                    options=[
                        {'label': 'Black Hole with Quantum Core', 'value': 'blackhole'},
                        {'label': 'Wormhole Stabilization', 'value': 'wormhole'},
                        {'label': 'Dark Energy Vacuum', 'value': 'darkenergy'},
                        {'label': 'Supernova Collapse', 'value': 'supernova'},
                        {'label': 'Custom Gaussian', 'value': 'custom'}
                    ],
                    value='blackhole'
                ),
                
                html.Br(),
                html.Button('Run Simulation', id='run-button', n_clicks=0,
                           style={'fontSize': '16px', 'padding': '10px 20px'}),
                html.Div(id='status-output', style={'marginTop': '10px', 'fontSize': '14px'}),
            ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'margin': '20px'}),
            
            html.Div([
                html.H3("Visualization Controls"),
                
                html.Label("Field to Display:"),
                dcc.Dropdown(
                    id='field-dropdown',
                    options=[
                        {'label': 'Mass Distribution', 'value': 'mass'},
                        {'label': 'Quantum Entropy', 'value': 'entropy'},
                        {'label': 'Metric g₀₀', 'value': 'metric'},
                        {'label': 'Quantum Pressure', 'value': 'pressure'}
                    ],
                    value='metric'
                ),
                
                html.Br(),
                html.Label("Slice Plane:"),
                dcc.RadioItems(
                    id='slice-plane',
                    options=[
                        {'label': 'XY (Z-slice)', 'value': 'xy'},
                        {'label': 'XZ (Y-slice)', 'value': 'xz'},
                        {'label': 'YZ (X-slice)', 'value': 'yz'}
                    ],
                    value='xy',
                    inline=True
                ),
                
                html.Br(),
                html.Label("Slice Position:"),
                dcc.Slider(
                    id='slice-slider',
                    min=0,
                    max=self.grid_size-1,
                    value=self.grid_size//2,
                    marks={i: str(i) for i in range(0, self.grid_size, 8)},
                    step=1
                ),
                
                html.Br(),
                html.Label("Visualization Type:"),
                dcc.RadioItems(
                    id='viz-type',
                    options=[
                        {'label': '2D Heatmap', 'value': 'heatmap'},
                        {'label': '3D Surface', 'value': 'surface'},
                        {'label': '3D Isosurface', 'value': 'isosurface'}
                    ],
                    value='heatmap',
                    inline=True
                ),
            ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'margin': '20px'}),
            
            html.Div([
                dcc.Graph(id='main-plot', style={'height': '700px'})
            ]),
            
            html.Div([
                html.H3("Statistics"),
                html.Div(id='stats-output', style={'fontFamily': 'monospace', 'fontSize': '14px'})
            ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'margin': '20px'})
        ])
    
    def _setup_callbacks(self):
        """Setup Dash callbacks."""
        
        @self.app.callback(
            Output('status-output', 'children'),
            Input('run-button', 'n_clicks'),
            State('scenario-dropdown', 'value')
        )
        def run_simulation(n_clicks, scenario):
            if n_clicks == 0:
                return "Ready to run simulation..."
            
            # Create scenario
            if scenario == 'blackhole':
                self._create_blackhole_scenario()
                return "✓ Black hole scenario loaded!"
            elif scenario == 'wormhole':
                self._create_wormhole_scenario()
                return "✓ Wormhole scenario loaded!"
            elif scenario == 'darkenergy':
                self._create_darkenergy_scenario()
                return "✓ Dark energy scenario loaded!"
            elif scenario == 'supernova':
                self._create_supernova_scenario()
                return "✓ Supernova scenario loaded!"
            else:
                self._create_custom_scenario()
                return "✓ Custom scenario loaded!"
        
        @self.app.callback(
            [Output('main-plot', 'figure'),
             Output('stats-output', 'children')],
            [Input('field-dropdown', 'value'),
             Input('slice-plane', 'value'),
             Input('slice-slider', 'value'),
             Input('viz-type', 'value'),
             Input('run-button', 'n_clicks')]
        )
        def update_plot(field, plane, slice_pos, viz_type, n_clicks):
            if self.metric is None:
                # No simulation run yet
                empty_fig = go.Figure()
                empty_fig.update_layout(title="Run a simulation first!")
                return empty_fig, "No data yet"
            
            # Get field data
            if field == 'mass':
                data = self.mass_dist
                title = "Mass Distribution"
                colorscale = 'Hot'
            elif field == 'entropy':
                data = self.entropy_map
                title = "Quantum Entropy"
                colorscale = 'Viridis'
            elif field == 'metric':
                data = self.metric[..., 0, 0]
                title = "Metric g₀₀"
                colorscale = 'RdBu_r'
            else:  # pressure
                data = self.quantum_pressure
                title = "Quantum Pressure"
                colorscale = 'Seismic'
            
            # Extract slice
            if plane == 'xy':
                slice_data = data[:, :, slice_pos]
                xlabel, ylabel = 'X', 'Y'
            elif plane == 'xz':
                slice_data = data[:, slice_pos, :]
                xlabel, ylabel = 'X', 'Z'
            else:  # yz
                slice_data = data[slice_pos, :, :]
                xlabel, ylabel = 'Y', 'Z'
            
            # Create figure
            if viz_type == 'heatmap':
                fig = go.Figure(data=go.Heatmap(
                    z=slice_data,
                    colorscale=colorscale,
                    colorbar=dict(title=title)
                ))
                fig.update_layout(
                    title=f"{title} - {plane.upper()} Slice at {slice_pos}",
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    height=700
                )
            
            elif viz_type == 'surface':
                fig = go.Figure(data=go.Surface(
                    z=slice_data,
                    colorscale=colorscale,
                    colorbar=dict(title=title)
                ))
                fig.update_layout(
                    title=f"{title} - 3D Surface",
                    scene=dict(
                        xaxis_title=xlabel,
                        yaxis_title=ylabel,
                        zaxis_title=title
                    ),
                    height=700
                )
            
            else:  # isosurface
                # Create 3D isosurface
                isovalue = np.median(data)
                fig = go.Figure(data=go.Isosurface(
                    x=self.X.flatten(),
                    y=self.Y.flatten(),
                    z=self.Z.flatten(),
                    value=data.flatten(),
                    isomin=isovalue * 0.9,
                    isomax=isovalue * 1.1,
                    surface_count=3,
                    colorscale=colorscale,
                    caps=dict(x_show=False, y_show=False, z_show=False)
                ))
                fig.update_layout(
                    title=f"{title} - 3D Isosurface",
                    scene=dict(
                        xaxis_title='X',
                        yaxis_title='Y',
                        zaxis_title='Z'
                    ),
                    height=700
                )
            
            # Compute statistics
            stats_text = self._compute_statistics(data, title)
            
            return fig, stats_text
    
    def _create_blackhole_scenario(self):
        """Create black hole scenario."""
        r = np.sqrt((self.X - self.domain_size/2)**2 + 
                   (self.Y - self.domain_size/2)**2 + 
                   (self.Z - self.domain_size/2)**2)
        r = np.maximum(r, 0.1)
        
        self.mass_dist = 5e12 / (r**2 + 0.5)
        self.entropy_map = 15.0 * np.exp(-r**2 / 4.0)
        
        self.metric = self.engine.solve_field_equations(
            self.mass_dist, self.entropy_map, iterations=100, verbose=False
        )
        self.quantum_pressure = self.engine.calculate_quantum_pressure(self.entropy_map)
    
    def _create_wormhole_scenario(self):
        """Create wormhole scenario."""
        r = np.sqrt((self.X - self.domain_size/2)**2 + 
                   (self.Y - self.domain_size/2)**2 + 
                   (self.Z - self.domain_size/2)**2)
        
        r_throat = 2.5
        self.mass_dist = 8e11 * np.exp(-((r - r_throat)**2) / 0.8)
        self.entropy_map = 20.0 * np.exp(-((r - r_throat)**2) / 0.5)
        
        self.metric = self.engine.solve_field_equations(
            self.mass_dist, self.entropy_map, iterations=100, verbose=False
        )
        self.quantum_pressure = self.engine.calculate_quantum_pressure(self.entropy_map)
    
    def _create_darkenergy_scenario(self):
        """Create dark energy scenario."""
        shape = (self.grid_size, self.grid_size, self.grid_size)
        self.entropy_map = 5.0 + 0.5 * np.random.randn(*shape)
        self.entropy_map = np.abs(self.entropy_map)
        
        self.metric = self.engine.solve_field_equations(
            self.mass_dist, self.entropy_map, iterations=100, verbose=False
        )
        self.quantum_pressure = self.engine.calculate_quantum_pressure(self.entropy_map)
    
    def _create_custom_scenario(self):
        """Create custom Gaussian scenario."""
        center = self.domain_size / 2
        r2 = (self.X-center)**2 + (self.Y-center)**2 + (self.Z-center)**2
        self.mass_dist = 1e11 * np.exp(-r2 / 4.0)
        self.entropy_map = 10.0 * np.exp(-r2 / 6.0)
        
        self.metric = self.engine.solve_field_equations(
            self.mass_dist, self.entropy_map, iterations=100, verbose=False
        )
        self.quantum_pressure = self.engine.calculate_quantum_pressure(self.entropy_map)

    def _create_supernova_scenario(self):
        """Create supernova collapse scenario."""
        r = np.sqrt((self.X - self.domain_size/2)**2 + 
                   (self.Y - self.domain_size/2)**2 + 
                   (self.Z - self.domain_size/2)**2)
        
        # High density core, expanding shell
        self.mass_dist = 2e12 * np.exp(-r**2 / 1.0) + 5e11 * np.exp(-(r-4)**2 / 0.5)
        self.entropy_map = 25.0 * np.exp(-r**2 / 2.0)
        
        self.metric = self.engine.solve_field_equations(
            self.mass_dist, self.entropy_map, iterations=100, verbose=False
        )
        self.quantum_pressure = self.engine.calculate_quantum_pressure(self.entropy_map)
    
    def _compute_statistics(self, data, field_name):
        """Compute statistics for display."""
        stats = f"""
        Field: {field_name}
        ─────────────────────────────────
        Mean:     {np.mean(data):.6e}
        Std Dev:  {np.std(data):.6e}
        Min:      {np.min(data):.6e}
        Max:      {np.max(data):.6e}
        Median:   {np.median(data):.6e}
        """
        return html.Pre(stats)
    
    def run(self, debug=False, port=8050):
        """
        Run the interactive visualizer.
        
        Parameters:
        -----------
        debug : bool
            Run in debug mode
        port : int
            Port number for web server
        """
        print("=" * 70)
        print("AETHELGARD-QGF INTERACTIVE VISUALIZER")
        print("=" * 70)
        print(f"\nStarting web server on port {port}...")
        print(f"Open your browser to: http://localhost:{port}")
        print("\n   Press Ctrl+C to stop the server")
        print("=" * 70)
        
        self.app.run_server(debug=debug, port=port)


def create_static_3d_visualization(
    engine, metric, mass_dist, entropy_map, output_file='3d_visualization.html'
):
    """
    Create a static 3D visualization and save as HTML.
    
    Parameters:
    -----------
    engine : AethelgardEngine
        Engine instance
    metric : ndarray
        Metric tensor
    mass_dist : ndarray
        Mass distribution
    entropy_map : ndarray
        Entropy field
    output_file : str
        Output HTML file path
    """
    if not INTERACTIVE_AVAILABLE:
        print("Plotly not available. Install with: pip install -r requirements-optional.txt")
        return
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Mass Distribution', 'Quantum Entropy', 
                       'Metric g₀₀', 'Quantum Pressure'),
        specs=[[{'type': 'surface'}, {'type': 'surface'}],
               [{'type': 'surface'}, {'type': 'surface'}]]
    )
    
    # Get slice
    N = metric.shape[0]
    slice_idx = N // 2
    
    # Mass
    fig.add_trace(
        go.Surface(z=mass_dist[:, :, slice_idx], colorscale='Hot', showscale=False),
        row=1, col=1
    )
    
    # Entropy
    fig.add_trace(
        go.Surface(z=entropy_map[:, :, slice_idx], colorscale='Viridis', showscale=False),
        row=1, col=2
    )
    
    # Metric
    g_00 = metric[..., 0, 0]
    fig.add_trace(
        go.Surface(z=g_00[:, :, slice_idx], colorscale='RdBu_r', showscale=False),
        row=2, col=1
    )
    
    # Quantum pressure
    T_quantum = engine.calculate_quantum_pressure(entropy_map)
    fig.add_trace(
        go.Surface(z=T_quantum[:, :, slice_idx], colorscale='Seismic', showscale=False),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Aethelgard-QGF 3D Visualization",
        height=800,
        showlegend=False
    )
    
    fig.write_html(output_file)
    print(f"Saved interactive 3D visualization to: {output_file}")


if __name__ == "__main__":
    if INTERACTIVE_AVAILABLE:
        # Create and run visualizer
        viz = InteractiveVisualizer(grid_size=32, domain_size=10.0)
        viz.run(debug=False, port=8050)
    else:
        print("\nCannot run interactive visualizer without Plotly and Dash.")
        print("Install with: pip install -r requirements-optional.txt")
