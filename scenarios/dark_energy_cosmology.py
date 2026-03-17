"""
Dark Energy Cosmology Scenario

This scenario models dark energy as emergent from quantum vacuum entropy.
A nearly uniform entropy field with small perturbations creates
a cosmological constant-like effect, driving accelerated expansion.

Physical Interpretation:
- Quantum vacuum has intrinsic entanglement structure
- Uniform entropy → cosmological constant Λ
- Perturbations → structure formation seeds
- Repulsive pressure → accelerated expansion
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
from pathlib import Path

import matplotlib.pyplot as plt

from aethelgard_engine import AethelgardEngine


def create_dark_energy_scenario(grid_size=32, domain_size=10.0):
    """
    Create a dark energy cosmology simulation.
    
    Parameters:
    -----------
    grid_size : int
        Number of grid points per dimension
    domain_size : float
        Physical size of domain in meters (represents cosmological patch)
    """
    print("=" * 70)
    print("DARK ENERGY FROM QUANTUM VACUUM")
    print("Scenario: Emergent Cosmological Constant")
    print("=" * 70)
    
    # Initialize engine
    engine = AethelgardEngine(grid_size=grid_size, domain_size=domain_size)
    
    # Minimal matter density (nearly empty universe)
    print("\n[1/4] Creating nearly empty universe...")
    mass_distribution = np.ones((grid_size, grid_size, grid_size)) * 1e6  # Very low density
    
    # Add small matter perturbations (structure seeds)
    np.random.seed(42)
    perturbations = 1e7 * np.random.randn(grid_size, grid_size, grid_size)
    mass_distribution += perturbations
    mass_distribution = np.abs(mass_distribution)
    
    # Quantum vacuum entropy: Nearly uniform with fluctuations
    print("[2/4] Generating quantum vacuum entropy field...")
    # Base vacuum entropy
    vacuum_entropy = 5.0  # Uniform background
    
    # Quantum fluctuations (scale-invariant)
    entropy_fluctuations = 0.5 * np.random.randn(grid_size, grid_size, grid_size)
    
    # Total entropy field
    entropy_map = vacuum_entropy + entropy_fluctuations
    entropy_map = np.abs(entropy_map)
    
    # Solve field equations
    print("[3/4] Solving cosmological field equations...")
    result_metric = engine.solve_field_equations(
        mass_distribution,
        entropy_map,
        iterations=100
    )
    
    # Extract metric
    g_00 = result_metric[..., 0, 0]
    
    # Calculate quantum pressure (dark energy)
    T_quantum = engine.calculate_quantum_pressure(entropy_map)
    
    # Visualizations
    print("[4/4] Generating visualizations...")
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Plot 1: Statistical distributions
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Entropy histogram
    axes[0, 0].hist(entropy_map.flatten(), bins=50, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].axvline(vacuum_entropy, color='red', linestyle='--', 
                       label=f'Vacuum level = {vacuum_entropy}')
    axes[0, 0].set_xlabel('Entropy Density')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Quantum Vacuum Entropy Distribution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Quantum pressure histogram
    axes[0, 1].hist(T_quantum.flatten(), bins=50, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].axvline(0, color='red', linestyle='--')
    axes[0, 1].set_xlabel('Quantum Pressure')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Dark Energy Pressure Distribution')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Metric distribution
    axes[1, 0].hist(g_00.flatten(), bins=50, alpha=0.7, color='purple', edgecolor='black')
    axes[1, 0].axvline(1.0, color='red', linestyle='--', label='Minkowski')
    axes[1, 0].set_xlabel('g₀₀')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Metric Component Distribution')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Power spectrum (structure formation)
    # Compute 3D FFT of metric perturbations
    g_perturbation = g_00 - np.mean(g_00)
    fft_3d = np.fft.fftn(g_perturbation)
    power_spectrum = np.abs(fft_3d)**2
    
    # Spherically average
    kx = np.fft.fftfreq(grid_size)
    ky = np.fft.fftfreq(grid_size)
    kz = np.fft.fftfreq(grid_size)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    k_mag = np.sqrt(KX**2 + KY**2 + KZ**2)
    
    k_bins = np.linspace(0, 0.5, 20)
    P_k = []
    k_centers = []
    for i in range(len(k_bins)-1):
        mask = (k_mag >= k_bins[i]) & (k_mag < k_bins[i+1])
        if np.any(mask):
            P_k.append(np.mean(power_spectrum[mask]))
            k_centers.append((k_bins[i] + k_bins[i+1]) / 2)
    
    axes[1, 1].loglog(k_centers, P_k, 'o-', color='orange')
    axes[1, 1].set_xlabel('Wavenumber k')
    axes[1, 1].set_ylabel('Power P(k)')
    axes[1, 1].set_title('Metric Perturbation Power Spectrum')
    axes[1, 1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'dark_energy_statistics.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'dark_energy_statistics.png'}")
    
    # Plot 2: Spatial slices
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    slice_idx = grid_size // 2
    
    im1 = axes[0, 0].imshow(entropy_map[:, :, slice_idx], 
                            cmap='viridis', origin='lower')
    axes[0, 0].set_title('Quantum Vacuum Entropy')
    plt.colorbar(im1, ax=axes[0, 0], label='Entropy')
    
    im2 = axes[0, 1].imshow(T_quantum[:, :, slice_idx], 
                            cmap='RdBu_r', origin='lower')
    axes[0, 1].set_title('Dark Energy Pressure')
    plt.colorbar(im2, ax=axes[0, 1], label='T_quantum')
    
    im3 = axes[1, 0].imshow(g_00[:, :, slice_idx], 
                            cmap='coolwarm', origin='lower')
    axes[1, 0].set_title('Spacetime Metric g₀₀')
    plt.colorbar(im3, ax=axes[1, 0], label='g₀₀')
    
    # Metric perturbation
    g_pert_slice = g_00[:, :, slice_idx] - np.mean(g_00)
    im4 = axes[1, 1].imshow(g_pert_slice, 
                            cmap='seismic', origin='lower')
    axes[1, 1].set_title('Metric Perturbations (Structure Seeds)')
    plt.colorbar(im4, ax=axes[1, 1], label='δg₀₀')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'dark_energy_fields.png', dpi=150)
    print(f"  ✓ Saved: {output_dir / 'dark_energy_fields.png'}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("COSMOLOGICAL ANALYSIS")
    print("=" * 70)
    
    print("\nQuantum Vacuum Properties:")
    print(f"  • Mean entropy: {np.mean(entropy_map):.4f}")
    print(f"  • Entropy std dev: {np.std(entropy_map):.4f}")
    print(f"  • Entropy range: [{np.min(entropy_map):.4f}, {np.max(entropy_map):.4f}]")
    
    print("\nDark Energy Characteristics:")
    mean_pressure = np.mean(T_quantum)
    print(f"  • Mean quantum pressure: {mean_pressure:.6e}")
    print(f"  • Pressure std dev: {np.std(T_quantum):.6e}")
    
    if abs(mean_pressure) < 1e-25:
        print("  • Pressure nearly uniform → Cosmological constant behavior ✓")
    
    print("\nMetric Analysis:")
    print(f"  • Mean g₀₀: {np.mean(g_00):.8f}")
    print(f"  • g₀₀ std dev: {np.std(g_00):.8f}")
    print(f"  • Deviation from Minkowski: {abs(np.mean(g_00) - 1.0):.8f}")
    
    print("\nStructure Formation:")
    perturbation_amplitude = np.std(g_00 - np.mean(g_00))
    print(f"  • Metric perturbation amplitude: {perturbation_amplitude:.8f}")
    if perturbation_amplitude > 1e-6:
        print("  • Perturbations present → Seeds for structure formation ✓")
    
    # Effective cosmological constant
    Lambda_eff = mean_pressure * (8 * np.pi * engine.G / engine.c**4)
    print("\nEffective Cosmological Constant:")
    print(f"  • Λ_eff ≈ {Lambda_eff:.6e} m⁻²")
    print("  • (Compare to observed: Λ_obs ≈ 1.1×10⁻⁵² m⁻²)")
    
    print("\n" + "=" * 70)
    print("Dark energy simulation complete!")
    print("=" * 70)
    
    return engine, result_metric, mass_distribution, entropy_map


if __name__ == "__main__":
    create_dark_energy_scenario()
