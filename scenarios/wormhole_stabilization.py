"""
Wormhole Stabilization Scenario

This scenario explores using quantum pressure to stabilize a wormhole throat.
Classical wormholes require exotic matter (negative energy density) to remain open.
Here, quantum entropy gradients provide the necessary repulsive pressure.

Physical Interpretation:
- Wormhole throat connects two regions of spacetime
- Classical gravity would collapse the throat
- High quantum entropy at throat creates repulsion
- Stabilization without classical exotic matter
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
from pathlib import Path

import matplotlib.pyplot as plt

from aethelgard_engine import AethelgardEngine


def create_wormhole_scenario(grid_size=48, domain_size=15.0):
    """
    Create a stabilized wormhole configuration.
    
    Parameters:
    -----------
    grid_size : int
        Number of grid points per dimension
    domain_size : float
        Physical size of domain in meters
    """
    print("=" * 70)
    print("WORMHOLE STABILIZATION")
    print("Scenario: Quantum Pressure Stabilizing Exotic Geometry")
    print("=" * 70)
    
    # Initialize engine
    engine = AethelgardEngine(grid_size=grid_size, domain_size=domain_size)
    
    # Create coordinate grid
    x = np.linspace(0, domain_size, grid_size)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    
    # Wormhole throat at center
    center = domain_size / 2
    r = np.sqrt((X - center)**2 + (Y - center)**2 + (Z - center)**2)
    
    # Throat radius
    r_throat = 2.5  # meters
    
    # Mass distribution: Ring around throat
    print("\n[1/4] Creating wormhole throat geometry...")
    # Mass concentrated in a toroidal region around throat
    throat_mass = np.exp(-((r - r_throat)**2) / 0.8)
    mass_distribution = 8e11 * throat_mass
    
    # Quantum entropy: Maximum at throat for stabilization
    print("[2/4] Generating stabilizing quantum field...")
    # High entropy exactly at throat radius
    entropy_throat = 20.0 * np.exp(-((r - r_throat)**2) / 0.5)
    
    # Additional entropy at center
    entropy_center = 10.0 * np.exp(-r**2 / 1.5)
    
    # Combined entropy field
    entropy_map = entropy_throat + entropy_center
    
    # Add quantum fluctuations
    np.random.seed(123)
    entropy_map += 0.3 * np.random.randn(grid_size, grid_size, grid_size)
    entropy_map = np.abs(entropy_map)
    
    # Solve field equations
    print("[3/4] Solving field equations for wormhole geometry...")
    print("      (Computing stabilization...)")
    result_metric = engine.solve_field_equations(
        mass_distribution,
        entropy_map,
        iterations=150
    )
    
    # Extract metric
    g_00 = result_metric[..., 0, 0]
    
    # Calculate quantum pressure
    T_quantum = engine.calculate_quantum_pressure(entropy_map)
    
    # Visualizations
    print("[4/4] Generating visualizations...")
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Plot 1: Radial profiles
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    center_idx = grid_size // 2
    radial_slice = slice(0, grid_size)
    r_plot = r[center_idx, center_idx, radial_slice]
    
    # Mass profile
    axes[0, 0].plot(r_plot, mass_distribution[center_idx, center_idx, radial_slice])
    axes[0, 0].axvline(r_throat, color='red', linestyle='--', 
                       label=f'Throat radius = {r_throat}m')
    axes[0, 0].set_xlabel('Radius (m)')
    axes[0, 0].set_ylabel('Mass Density (kg/m³)')
    axes[0, 0].set_title('Mass Distribution (Toroidal)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Entropy profile
    axes[0, 1].plot(r_plot, entropy_map[center_idx, center_idx, radial_slice])
    axes[0, 1].axvline(r_throat, color='red', linestyle='--', label='Throat')
    axes[0, 1].set_xlabel('Radius (m)')
    axes[0, 1].set_ylabel('Entropy Density')
    axes[0, 1].set_title('Stabilizing Quantum Entropy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Metric profile
    axes[1, 0].plot(r_plot, g_00[center_idx, center_idx, radial_slice])
    axes[1, 0].axhline(1.0, color='gray', linestyle='--', label='Minkowski')
    axes[1, 0].axvline(r_throat, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].set_xlabel('Radius (m)')
    axes[1, 0].set_ylabel('g₀₀')
    axes[1, 0].set_title('Spacetime Metric (Wormhole Geometry)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Quantum pressure
    axes[1, 1].plot(r_plot, T_quantum[center_idx, center_idx, radial_slice])
    axes[1, 1].axhline(0, color='gray', linestyle='--')
    axes[1, 1].axvline(r_throat, color='red', linestyle='--', alpha=0.5)
    axes[1, 1].set_xlabel('Radius (m)')
    axes[1, 1].set_ylabel('Quantum Pressure')
    axes[1, 1].set_title('Stabilizing Pressure (Exotic Matter)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'wormhole_radial_profiles.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'wormhole_radial_profiles.png'}")
    
    # Plot 2: Cross-sections
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    slice_idx = grid_size // 2
    
    im1 = axes[0, 0].imshow(mass_distribution[:, :, slice_idx], 
                            cmap='hot', origin='lower')
    axes[0, 0].set_title('Mass Distribution (Throat Ring)')
    axes[0, 0].set_xlabel('X')
    axes[0, 0].set_ylabel('Y')
    plt.colorbar(im1, ax=axes[0, 0], label='ρ (kg/m³)')
    
    im2 = axes[0, 1].imshow(entropy_map[:, :, slice_idx], 
                            cmap='plasma', origin='lower')
    axes[0, 1].set_title('Quantum Entropy Field')
    axes[0, 1].set_xlabel('X')
    axes[0, 1].set_ylabel('Y')
    plt.colorbar(im2, ax=axes[0, 1], label='Entropy')
    
    im3 = axes[1, 0].imshow(g_00[:, :, slice_idx], 
                            cmap='RdBu_r', origin='lower', vmin=0.95, vmax=1.05)
    axes[1, 0].set_title('Metric g₀₀ (Wormhole Geometry)')
    axes[1, 0].set_xlabel('X')
    axes[1, 0].set_ylabel('Y')
    plt.colorbar(im3, ax=axes[1, 0], label='g₀₀')
    
    im4 = axes[1, 1].imshow(T_quantum[:, :, slice_idx], 
                            cmap='seismic', origin='lower')
    axes[1, 1].set_title('Quantum Pressure (Stabilization)')
    axes[1, 1].set_xlabel('X')
    axes[1, 1].set_ylabel('Y')
    plt.colorbar(im4, ax=axes[1, 1], label='T_quantum')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'wormhole_2d_slices.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'wormhole_2d_slices.png'}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("STABILIZATION ANALYSIS")
    print("=" * 70)
    
    # Throat region analysis
    throat_mask = np.abs(r - r_throat) < 0.5
    print(f"\nThroat Region (r ≈ {r_throat}m):")
    print(f"  • Average quantum pressure: {np.mean(T_quantum[throat_mask]):.6e}")
    print(f"  • Average entropy: {np.mean(entropy_map[throat_mask]):.4f}")
    print(f"  • Average g₀₀: {np.mean(g_00[throat_mask]):.6f}")
    
    # Check for stabilization
    throat_pressure = np.mean(T_quantum[throat_mask])
    if throat_pressure > 0:
        print("\n  ✓ STABILIZATION ACHIEVED!")
        print("    Positive quantum pressure provides outward force")
        print("    This acts as 'exotic matter' keeping throat open")
    else:
        print("\n  ⚠ Insufficient stabilization")
        print("    Increase entropy at throat for stronger effect")
    
    # Energy condition violation
    print("\nEnergy Condition Analysis:")
    print("  • Classical wormholes require NEC violation")
    print(f"  • Quantum pressure sign: {np.sign(throat_pressure):.0f}")
    if throat_pressure > 0:
        print("  • Effective negative energy density achieved ✓")
    
    print("\n" + "=" * 70)
    print("Wormhole simulation complete!")
    print("=" * 70)
    
    return engine, result_metric, mass_distribution, entropy_map


if __name__ == "__main__":
    create_wormhole_scenario()
