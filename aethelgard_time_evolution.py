"""
Time Evolution Module for Aethelgard-QGF

This module extends the Aethelgard engine to support time evolution of spacetime metrics.
Implements a simplified 3+1 formalism for dynamic gravitational fields.

Physical Framework:
- ADM (Arnowitt-Deser-Misner) decomposition of spacetime
- Time slicing of 4D spacetime into 3D spatial slices
- Evolution of metric and extrinsic curvature
- Quantum entropy dynamics

Note: This is a simplified implementation for educational purposes.
Full numerical relativity requires more sophisticated methods (BSSN, etc.)
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
from pathlib import Path

import matplotlib.pyplot as plt

from aethelgard_engine import AethelgardEngine


class AethelgardEngineTimeEvolution(AethelgardEngine):
    """
    Time-evolution capable Aethelgard engine.
    
    Extends base engine with time-stepping capabilities.
    """
    
    def __init__(self, grid_size=32, domain_size=10.0, dt=0.01):
        """
        Initialize time-evolution engine.
        
        Parameters:
        -----------
        grid_size : int
            Number of grid points per dimension
        domain_size : float
            Physical size of domain in meters
        dt : float
            Time step size in seconds
        """
        super().__init__(grid_size, domain_size)
        
        # Security: Input validation
        if not isinstance(dt, (int, float)) or dt <= 0:
            raise ValueError("Time step (dt) must be a positive number.")
        if dt > 1000.0:
            raise ValueError("Time step (dt) is too large.")

        self.dt = dt
        self.current_time = 0.0
        
        # Extrinsic curvature (measures how spatial slice is embedded in spacetime)
        self.K = np.zeros((self.N, self.N, self.N, 3, 3))
        
        # Lapse function (time dilation between slices)
        self.alpha = np.ones((self.N, self.N, self.N))
        
        # Shift vector (motion of coordinates)
        self.beta = np.zeros((self.N, self.N, self.N, 3))
        
        # History storage
        self.history = {
            'time': [],
            'metric_mean': [],
            'metric_std': [],
            'K_mean': [],
            'entropy_mean': []
        }
    
    def evolve_metric(self, mass_distribution, entropy_map, time_steps=100, 
                     entropy_evolution=False, verbose=True):
        """
        Evolve the spacetime metric forward in time.
        
        Parameters:
        -----------
        mass_distribution : ndarray
            Initial mass density field
        entropy_map : ndarray or callable
            If ndarray: static entropy field
            If callable: function(t) returning entropy at time t
        time_steps : int
            Number of time steps to evolve
        entropy_evolution : bool
            If True, allow entropy to evolve dynamically
        verbose : bool
            Print progress
            
        Returns:
        --------
        history : dict
            Time evolution history
        """
        # Security: Input validation
        if not isinstance(time_steps, int) or time_steps <= 0:
            raise ValueError("Time steps must be a positive integer.")
        if time_steps > 5000:
            raise ValueError("Time steps exceeds maximum limit of 5000 to prevent resource exhaustion.")

        if verbose:
            print("=" * 70)
            print("TIME EVOLUTION SIMULATION")
            print(f"Time steps: {time_steps}, dt = {self.dt}s")
            print(f"Total time: {time_steps * self.dt}s")
            print("=" * 70)
        
        # Initialize entropy
        if callable(entropy_map):
            current_entropy = entropy_map(0.0)
        else:
            current_entropy = entropy_map.copy()
        
        for step in range(time_steps):
            # Update entropy if dynamic
            if callable(entropy_map):
                current_entropy = entropy_map(self.current_time)
            elif entropy_evolution:
                # Simple entropy diffusion
                current_entropy = self._evolve_entropy(current_entropy)
            
            # Compute stress-energy
            T_classic = mass_distribution * (self.c**2)
            T_quantum = self.calculate_quantum_pressure(current_entropy)
            T_total = T_classic - T_quantum
            
            # Update metric using simplified ADM evolution
            self._update_metric_adm(T_total)
            
            # Update extrinsic curvature
            self._update_extrinsic_curvature(T_total)
            
            # Advance time
            self.current_time += self.dt
            
            # Record history
            g_00 = self.metric[..., 0, 0]
            self.history['time'].append(self.current_time)
            self.history['metric_mean'].append(np.mean(g_00))
            self.history['metric_std'].append(np.std(g_00))
            self.history['K_mean'].append(np.mean(np.abs(self.K)))
            self.history['entropy_mean'].append(np.mean(current_entropy))
            
            # Progress
            if verbose and (step + 1) % 20 == 0:
                print(f"  Step {step+1}/{time_steps}, t = {self.current_time:.3f}s")
        
        if verbose:
            print("Evolution complete.")
        
        return self.history
    
    def _update_metric_adm(self, stress_energy):
        """
        Update metric using simplified ADM formalism.
        
        In full ADM:
        ∂_t g_ij = -2α K_ij + ∇_i β_j + ∇_j β_i
        
        Simplified version for educational purposes.
        """
        # Compute metric update from stress-energy
        curvature_source = (8 * np.pi * self.G / self.c**4) * stress_energy
        
        # Update spatial metric components (simplified)
        for i in range(1, 4):  # Spatial indices
            for j in range(i, 4):
                # Apply update to g_ij
                if i == j:
                    self.metric[..., i, i] += self.dt * curvature_source * 0.01

        # Update g_00 (time-time component)
        self.metric[..., 0, 0] += self.dt * curvature_source * 0.01
    
    def _update_extrinsic_curvature(self, stress_energy):
        """
        Update extrinsic curvature.
        
        In full ADM:
        ∂_t K_ij = -∇_i ∇_j α + α(R_ij - 2K_ik K^k_j + K K_ij) + ...
        
        Simplified version.
        """
        # Simplified: K evolves based on stress-energy
        K_source = (4 * np.pi * self.G / self.c**4) * stress_energy
        
        # Update diagonal components
        for i in range(3):
            self.K[..., i, i] += self.dt * K_source * 0.005
    
    def _evolve_entropy(self, entropy):
        """
        Evolve entropy field via diffusion.
        
        Simple model: ∂S/∂t = D ∇²S
        where D is diffusion coefficient.
        """
        D = 0.01  # Diffusion coefficient
        
        # Compute Laplacian
        grad_S = np.gradient(entropy, self.dx)
        laplacian_S = np.zeros_like(entropy)
        for i, g in enumerate(grad_S):
            laplacian_S += np.gradient(g, self.dx)[i]
        
        # Update entropy
        entropy_new = entropy + self.dt * D * laplacian_S
        
        # Keep entropy positive
        entropy_new = np.abs(entropy_new)
        
        return entropy_new
    
    def visualize_evolution(self, output_dir='output'):
        """
        Create visualizations of time evolution.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save plots
        """
        # Security: Prevent path traversal
        if ".." in output_dir or output_dir.startswith("/") or output_dir.startswith("\\") or ":" in output_dir:
            raise ValueError("Invalid output directory. Path traversal or absolute paths not allowed.")
            
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        times = np.array(self.history['time'])
        
        # Metric evolution
        axes[0, 0].plot(times, self.history['metric_mean'], 'b-', linewidth=2)
        axes[0, 0].fill_between(times,
                                np.array(self.history['metric_mean']) - np.array(self.history['metric_std']),
                                np.array(self.history['metric_mean']) + np.array(self.history['metric_std']),
                                alpha=0.3)
        axes[0, 0].axhline(1.0, color='gray', linestyle='--', label='Minkowski')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('⟨g₀₀⟩')
        axes[0, 0].set_title('Metric Evolution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Extrinsic curvature
        axes[0, 1].plot(times, self.history['K_mean'], 'r-', linewidth=2)
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('⟨|K|⟩')
        axes[0, 1].set_title('Extrinsic Curvature Evolution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Entropy evolution
        axes[1, 0].plot(times, self.history['entropy_mean'], 'g-', linewidth=2)
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('⟨S⟩')
        axes[1, 0].set_title('Quantum Entropy Evolution')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Metric standard deviation (measure of inhomogeneity)
        axes[1, 1].plot(times, self.history['metric_std'], 'm-', linewidth=2)
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('σ(g₀₀)')
        axes[1, 1].set_title('Metric Inhomogeneity')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / 'time_evolution.png', dpi=150)
        print(f"Saved: {output_path / 'time_evolution.png'}")
        
        return fig


def example_gravitational_wave():
    """
    Example: Simulate a gravitational wave passing through the grid.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE: GRAVITATIONAL WAVE PROPAGATION")
    print("=" * 70)
    
    # Initialize
    engine = AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=0.02)
    
    # Minimal mass (nearly empty space)
    mass = np.ones((32, 32, 32)) * 1e5
    
    # Time-dependent entropy (simulates passing wave)
    def entropy_wave(t):
        """Entropy wave traveling in x-direction."""
        x = np.linspace(0, 10, 32)
        X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
        
        # Wave parameters
        wavelength = 3.0  # meters
        amplitude = 2.0
        velocity = 1.0  # m/s
        
        # Traveling wave
        k = 2 * np.pi / wavelength
        omega = k * velocity
        phase = k * X - omega * t
        
        entropy = amplitude * (1 + 0.5 * np.sin(phase))
        return entropy
    
    # Evolve
    history = engine.evolve_metric(mass, entropy_wave, time_steps=100, verbose=True)
    
    # Visualize
    engine.visualize_evolution(output_dir='scenarios/output')
    
    print("\nGravitational wave simulation complete.")
    return engine, history


def example_collapsing_star():
    """
    Example: Simulate a collapsing star with quantum core.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE: COLLAPSING STAR WITH QUANTUM BOUNCE")
    print("=" * 70)
    
    # Initialize
    engine = AethelgardEngineTimeEvolution(grid_size=32, domain_size=10.0, dt=0.01)
    
    # Spherical mass distribution
    x = np.linspace(0, 10, 32)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    r = np.sqrt((X-5)**2 + (Y-5)**2 + (Z-5)**2)
    
    # Initial mass (stellar core)
    mass = 5e11 * np.exp(-r**2 / 4.0)
    
    # Time-dependent entropy (increases during collapse)
    def entropy_collapse(t):
        """Entropy increases as star collapses."""
        # Entropy grows at core
        base_entropy = 2.0 * (1 + 0.5 * t)  # Grows with time
        entropy = base_entropy * np.exp(-r**2 / (3.0 - 0.5*t))  # Core shrinks
        return np.abs(entropy)
    
    # Evolve
    history = engine.evolve_metric(mass, entropy_collapse, time_steps=80, verbose=True)
    
    # Visualize
    engine.visualize_evolution(output_dir='scenarios/output')
    
    # Check for bounce
    metric_evolution = np.array(history['metric_mean'])
    if len(metric_evolution) > 10:
        # Look for minimum (bounce point)
        min_idx = np.argmin(metric_evolution)
        if 10 < min_idx < len(metric_evolution) - 10:
            print(f"\n✓ Quantum bounce detected at t = {history['time'][min_idx]:.3f}s!")
            print("  Entropy-driven repulsion prevented complete collapse.")
        else:
            print("\n  Collapse continues (no bounce in simulation time)")
    
    return engine, history


if __name__ == "__main__":
    # Run examples
    print("Running time evolution examples...\n")
    
    # Example 1: Gravitational wave
    engine1, history1 = example_gravitational_wave()
    
    # Example 2: Collapsing star
    engine2, history2 = example_collapsing_star()
    
    print("\n" + "=" * 70)
    print("All time evolution examples complete!")
    print("Check 'scenarios/output/' for visualizations.")
    print("=" * 70)
