"""
Aethelgard-QGF: Quantum Gravitational Field Engine

Production-grade solver for spacetime metrics where quantum information
density modifies gravity. Entanglement entropy gradients create repulsive
geometric pressure—a potential antigravity mechanism.

Usage:
    from aethelgard import AethelgardEngine, AethelgardEngineGPU

    engine = AethelgardEngine(grid_size=32, domain_size=10.0)
    metric = engine.solve_field_equations(mass, entropy)
"""

from aethelgard_engine import AethelgardEngine
from aethelgard_engine_gpu import AethelgardEngineGPU
from aethelgard_time_evolution import AethelgardEngineTimeEvolution
from antigravity_engine import calculate_flux_anomaly, simulate_antigravity_flux

__version__ = "1.0.0"
__all__ = [
    "AethelgardEngine",
    "AethelgardEngineGPU",
    "AethelgardEngineTimeEvolution",
    "calculate_flux_anomaly",
    "simulate_antigravity_flux",
    "__version__",
]
