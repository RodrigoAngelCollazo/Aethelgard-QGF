import numpy as np


class AethelgardEngine:
    """
    AGI-optimized solver for Aethelgard-QGF.
    Solves for spacetime metrics where quantum information density 
    modifies the gravitational constant G into an effective G_eff.
    """
    def __init__(self, grid_size=32, domain_size=10.0):
        # Security: Input validation
        if not isinstance(grid_size, int) or grid_size <= 0:
            raise ValueError("Grid size must be a positive integer.")
        if grid_size > 256:
            raise ValueError(
                "Grid size exceeds maximum limit of 256 to prevent resource exhaustion."
            )
        if not isinstance(domain_size, (int, float)) or domain_size <= 0:
            raise ValueError("Domain size must be a positive number.")

        self.N = grid_size
        self.L = domain_size
        self.dx = self.L / self.N
        
        # Physical Constants
        self.G = 6.674e-11
        self.c = 3.0e8
        self.hbar = 1.054e-34

        # Physical Constraints & Limits
        self.causality_limit = (0.1, 10.0)
        
        # Initialize Spacetime Grid (Minkowski-like start)
        self.metric = np.zeros((self.N, self.N, self.N, 4, 4))
        for i in range(4): 
            self.metric[..., i, i] = 1.0  # Diagonal components

    def calculate_quantum_pressure(self, entropy_field):
        """
        Implements the 'Antigravity' component via Negative Energy Density.
        In QGF, high gradients of Entanglement Entropy (S) create 
        repulsive geometric pressure.
        """
        # S = A / 4G_hbar -> Localized entropy gradients
        grad_S = np.gradient(entropy_field, self.dx)
        laplacian_S = np.zeros_like(entropy_field)
        for i, g in enumerate(grad_S):
            laplacian_S += np.gradient(g, self.dx)[i]
            
        # The 'Antigravity' Term: Repulsive Stress-Energy (T_quantum)
        # Effectively a local Dark Energy/Lambda term
        T_quantum = (self.hbar * self.c / (self.dx**4)) * laplacian_S
        return T_quantum

    def solve_field_equations(self, mass_distribution, entropy_map, iterations=50, verbose=True):
        """
        Iterative solver for G_mu_nu + Lambda*g_mu_nu = 8*pi*G*T_mu_nu.
        Balances standard mass (attractive) vs quantum info (repulsive).
        """
        # Security: Input validation
        if not isinstance(iterations, int) or iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")
        if iterations > 10000:
            raise ValueError("Iterations exceeds maximum limit of 10000.")

        target_shape = (self.N, self.N, self.N)
        if mass_distribution.shape != target_shape:
            raise ValueError(
                f"Mass distribution shape {mass_distribution.shape} "
                f"must match grid size {target_shape}."
            )

        if entropy_map.shape != target_shape:
            raise ValueError(
                f"Entropy map shape {entropy_map.shape} "
                f"must match grid size {target_shape}."
            )

        if verbose:
            print("Synthesizing metric for Aethelgard-QGF...")
        
        current_geometry = self.metric.copy()
        
        # Pre-compute stresses (assuming static distributions for this solver run)
        T_classic = mass_distribution * (self.c**2)
        T_repulsive = self.calculate_quantum_pressure(entropy_map)
        T_total = T_classic - T_repulsive

        for _ in range(iterations):
            # Update Metric based on Einstein Tensor G_mu_nu
            # Solving for g_mu_nu using a linearized approximation
            curvature_update = (8 * np.pi * self.G / self.c**4) * T_total
            current_geometry[..., 0, 0] += 0.01 * curvature_update
            
            # PHYSICAL CONSTRAINT: Causality Clamp
            current_geometry[..., 0, 0] = np.clip(
                current_geometry[..., 0, 0], 
                self.causality_limit[0], 
                self.causality_limit[1]
            )
            
        self.metric = current_geometry
        return self.metric

    def calculate_paradox_hazard(self):
        """
        Calculates the risk of a causality paradox based on metric curvature.
        Hazard level ranges from 0.0 (safe) to 1.0 (imminent paradox).
        Uses metric variance as a proxy for instability.
        """
        # Simple heuristic: how much does g_00 deviate from Minkowski (1.0)
        deviation = np.abs(self.metric[..., 0, 0] - 1.0)
        max_deviation = np.max(deviation)
        
        # Normalize to 0-1 range based on causality limits
        # Max deviation is ~9.0 if g_00 is 10.0 (limit)
        hazard = np.clip(max_deviation / 9.0, 0.0, 1.0)
        return float(hazard)
