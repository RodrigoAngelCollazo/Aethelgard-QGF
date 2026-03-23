"""CLI entry points for Aethelgard-QGF."""


def run_example():
    """Run the example simulation."""
    from example_simulation import main
    main()


def run_viz():
    """Launch the interactive visualizer."""
    from interactive_visualizer import INTERACTIVE_AVAILABLE, InteractiveVisualizer
    if not INTERACTIVE_AVAILABLE:
        raise ImportError("Install with: pip install aethelgard-qgf[viz]")
    viz = InteractiveVisualizer(grid_size=32, domain_size=10.0)
    viz.run(debug=False, port=8050)


def run_benchmark():
    """Run CPU vs GPU benchmark."""
    from aethelgard_engine_gpu import benchmark_cpu_vs_gpu
    benchmark_cpu_vs_gpu(grid_sizes=[32, 64])
