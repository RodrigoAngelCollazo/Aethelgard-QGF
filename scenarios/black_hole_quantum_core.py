"""
Black Hole with Quantum Core Scenario

This scenario models a massive object with a quantum-repulsive core,
preventing the formation of a classical singularity. The high entropy
at the center creates antigravity pressure that balances gravitational collapse.

Physical Interpretation:
- Classical black hole would have r^-2 density profile
- Quantum core has high entanglement entropy
- Repulsive pressure prevents singularity formation
- Results in a "gravastar" or "quantum star" configuration
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
from pathlib import Path

import matplotlib.pyplot as plt

from aethelgard_engine import AethelgardEngine


def create_black_hole_scenario(grid_size=64, domain_size=20.0):
    """
    Create a black hole with quantum core.
    
    Parameters:
    -----------
    grid_size : int
        Number of grid points per dimension
    domain_size : float
        Physical size of domain in meters
    """
    print("=" * 70)
    print("BLACK HOLE WITH QUANTUM CORE")
    print("Scenario: Singularity Prevention via Quantum Repulsion")
    print("=" * 70)
    
    # Initialize engine
    engine = AethelgardEngine(grid_size=grid_size, domain_size=domain_size)
    
    # Create coordinate grid
    x = np.linspace(0, domain_size, grid_size)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    
    # Radial distance from center
    center = domain_size / 2
    r = np.sqrt((X - center)**2 + (Y - center)**2 + (Z - center)**2)
    r = np.maximum(r, 0.1)  # Avoid division by zero
    
    # Mass distribution: 1/r^2 profile (like Schwarzschild)
    print("\n[1/4] Creating black hole mass distribution (1/r² profile)...")
    # Scale mass to astrophysical densities (~1e27 kg/m³) to observe GR effects
    mass_scale = 1e27
    mass_distribution = 5.0 * mass_scale / (r**2 + 0.5)  # kg/m³
    
    # Quantum entropy: High at core, decreasing outward
    print("[2/4] Generating quantum core (high entropy region)...")
    r_core = 2.0  # Core radius in meters
    # Entropy must be ~10^66 to create pressure comparable to gravity in SI units
    # (Bekenstein-Hawking entropy S = A/4Lp^2 ~ 10^70 for macroscopic objects)
    entropy_scale = 1e67
    entropy_map = 15.0 * entropy_scale * np.exp(-r**2 / r_core**2)
    
    # Add quantum fluctuations
    np.random.seed(42)
    entropy_map += 0.5 * entropy_scale * np.random.randn(grid_size, grid_size, grid_size)
    entropy_map = np.abs(entropy_map)
    
    # Solve field equations
    print("[3/4] Solving modified Einstein equations...")
    print("      (This may take a minute for 64³ grid...)")
    result_metric = engine.solve_field_equations(
        mass_distribution,
        entropy_map,
        iterations=200
    )
    
    # Extract metric component
    g_00 = result_metric[..., 0, 0]

    # Control Run: Classical Black Hole (No Quantum Core)
    print("\n[3.5/4] Running classical control simulation (no quantum core)...")
    engine_classic = AethelgardEngine(grid_size=grid_size, domain_size=domain_size)
    metric_classic = engine_classic.solve_field_equations(
        mass_distribution,
        np.zeros_like(entropy_map),
        iterations=200
    )
    g_00_classic = metric_classic[..., 0, 0]

    # Calculate Quantum Shift
    quantum_shift = g_00 - g_00_classic
    
    # Calculate quantum pressure
    T_quantum = engine.calculate_quantum_pressure(entropy_map)
    
    # Visualizations
    print("[4/4] Generating visualizations...")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Plot 1: Radial profiles
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Extract radial slice through center
    center_idx = grid_size // 2
    radial_slice = slice(center_idx, grid_size)
    r_plot = r[center_idx, center_idx, radial_slice]
    
    # Mass profile
    axes[0, 0].semilogy(r_plot, mass_distribution[center_idx, center_idx, radial_slice])
    axes[0, 0].set_xlabel('Radius (m)')
    axes[0, 0].set_ylabel('Mass Density (kg/m³)')
    axes[0, 0].set_title('Mass Distribution (1/r² profile)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Entropy profile
    axes[0, 1].plot(r_plot, entropy_map[center_idx, center_idx, radial_slice])
    axes[0, 1].set_xlabel('Radius (m)')
    axes[0, 1].set_ylabel('Entropy Density')
    axes[0, 1].set_title('Quantum Entropy (Core Concentration)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axvline(r_core, color='red', linestyle='--', label=f'Core radius = {r_core}m')
    axes[0, 1].legend()
    
    # Metric profile
    axes[1, 0].plot(r_plot, g_00[center_idx, center_idx, radial_slice])
    axes[1, 0].axhline(1.0, color='gray', linestyle='--', label='Minkowski (g₀₀=1)')
    axes[1, 0].set_xlabel('Radius (m)')
    axes[1, 0].set_ylabel('g₀₀')
    axes[1, 0].set_title('Spacetime Metric Component')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Quantum pressure profile
    axes[1, 1].plot(r_plot, T_quantum[center_idx, center_idx, radial_slice], label='Pressure')
    axes[1, 1].plot(r_plot, quantum_shift[center_idx, center_idx, radial_slice],
                    color='purple', linestyle='--', label='Metric Shift')
    axes[1, 1].axhline(0, color='gray', linestyle='--')
    axes[1, 1].set_xlabel('Radius (m)')
    axes[1, 1].set_ylabel('Amplitude')
    axes[1, 1].set_title('Antigravity Pressure & Metric Shift')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'black_hole_radial_profiles.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'black_hole_radial_profiles.png'}")
    
    # Plot 2: 2D slices
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    slice_idx = grid_size // 2
    
    im1 = axes[0, 0].imshow(np.log10(mass_distribution[:, :, slice_idx] + 1e-10), 
                            cmap='hot', origin='lower')
    axes[0, 0].set_title('Mass Distribution (log scale)')
    plt.colorbar(im1, ax=axes[0, 0], label='log₁₀(ρ)')
    
    im2 = axes[0, 1].imshow(entropy_map[:, :, slice_idx], cmap='viridis', origin='lower')
    axes[0, 1].set_title('Quantum Entropy Field')
    plt.colorbar(im2, ax=axes[0, 1], label='Entropy')
    
    im3 = axes[1, 0].imshow(g_00[:, :, slice_idx], cmap='RdBu_r', origin='lower')
    axes[1, 0].set_title('Metric g₀₀')
    plt.colorbar(im3, ax=axes[1, 0], label='g₀₀')
    
    im4 = axes[1, 1].imshow(T_quantum[:, :, slice_idx], cmap='seismic', origin='lower')
    axes[1, 1].set_title('Quantum Pressure')
    plt.colorbar(im4, ax=axes[1, 1], label='T_quantum')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'black_hole_2d_slices.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'black_hole_2d_slices.png'}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS RESULTS")
    print("=" * 70)
    
    print("\nCore Properties (r < 2m):")
    core_mask = r < r_core
    print(f"  • Average g₀₀ in core: {np.mean(g_00[core_mask]):.6f}")
    print(f"  • Average entropy in core: {np.mean(entropy_map[core_mask]):.4f}")
    print(f"  • Average quantum pressure: {np.mean(T_quantum[core_mask]):.6e}")
    
    print("\nOuter Region (r > 5m):")
    outer_mask = r > 5.0
    print(f"  • Average g₀₀ outer: {np.mean(g_00[outer_mask]):.6f}")
    print(f"  • Average entropy outer: {np.mean(entropy_map[outer_mask]):.4f}")

    print("\nQuantum Shift Analysis (Anti-Gravity Anomalies):")
    max_shift = np.max(quantum_shift)
    min_shift = np.min(quantum_shift)
    print(f"  • Max Positive Shift (Antigravity): {max_shift:.6f}")
    print(f"  • Min Negative Shift: {min_shift:.6f}")

    core_shift = np.mean(quantum_shift[core_mask])
    print(f"  • Average Shift in Core: {core_shift:.6f}")

    if max_shift > 0.1:
        print("  ✓ SIGNIFICANT ANTI-GRAVITY ANOMALY DETECTED")
        print("    The quantum core is effectively screening the gravitational mass.")
    
    print("\nSingularity Prevention:")
    central_g00 = g_00[center_idx, center_idx, center_idx]
    print(f"  • Central g₀₀ value: {central_g00:.6f}")
    print(f"  • Classical g₀₀ would be: {g_00_classic[center_idx, center_idx, center_idx]:.6f}")

    if central_g00 > 0.5:
        print("  ✓ Singularity avoided! Quantum pressure prevents collapse.")
    else:
        print("  ⚠ Weak quantum effect. Increase entropy for stronger repulsion.")
    
    print("\n" + "=" * 70)
    print("Simulation complete! Check the 'output' directory for plots.")
    print("=" * 70)
    
    return engine, result_metric, mass_distribution, entropy_map


if __name__ == "__main__":
    create_black_hole_scenario()
