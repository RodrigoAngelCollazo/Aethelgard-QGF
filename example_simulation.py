"""
Example simulation demonstrating the Aethelgard-QGF engine.
This creates a scenario with localized mass and quantum entropy fields
to observe the interplay between attractive and repulsive geometric effects.
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from aethelgard_engine import AethelgardEngine


def create_gaussian_distribution(grid_size, center, sigma):
    """Create a 3D Gaussian distribution centered at a point."""
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    z = np.linspace(0, 10, grid_size)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    dist = np.sqrt((X - center[0])**2 + (Y - center[1])**2 + (Z - center[2])**2)
    return np.exp(-dist**2 / (2 * sigma**2))

def visualize_slice(data, title, slice_idx=16):
    """Visualize a 2D slice of 3D data."""
    plt.figure(figsize=(8, 6))
    plt.imshow(data[:, :, slice_idx], cmap='viridis', origin='lower')
    plt.colorbar(label='Intensity')
    plt.title(f'{title} (z-slice at {slice_idx})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.tight_layout()
    return plt.gcf()

def main():
    print("=" * 60)
    print("Aethelgard-QGF Simulation")
    print("Quantum Gravitational Field with Antigravity Effects")
    print("=" * 60)
    
    # Initialize engine
    grid_size = 32
    engine = AethelgardEngine(grid_size=grid_size, domain_size=10.0)
    
    # Create mass distribution (e.g., a massive object at center)
    print("\n[1/4] Creating mass distribution...")
    mass_center = [5.0, 5.0, 5.0]
    mass_distribution = create_gaussian_distribution(grid_size, mass_center, sigma=1.5)
    mass_distribution *= 1e10  # Scale to realistic mass density
    
    # Create quantum entropy map (high entropy regions create repulsion)
    print("[2/4] Generating quantum entropy field...")
    entropy_center = [5.0, 5.0, 5.0]
    entropy_map = create_gaussian_distribution(grid_size, entropy_center, sigma=2.0)
    
    # Add some quantum fluctuations
    np.random.seed(42)
    entropy_map += 0.1 * np.random.randn(grid_size, grid_size, grid_size)
    entropy_map = np.abs(entropy_map)  # Entropy must be positive
    
    # Solve field equations
    print("[3/4] Solving modified Einstein field equations...")
    result_metric = engine.solve_field_equations(
        mass_distribution, 
        entropy_map, 
        iterations=100
    )
    
    # Visualize results
    print("[4/4] Generating visualizations...")
    
    # Extract g_00 component (time-time metric component)
    g_00 = result_metric[..., 0, 0]
    
    # Create visualizations
    visualize_slice(mass_distribution, 'Mass Distribution')
    plt.savefig('mass_distribution.png', dpi=150)
    
    visualize_slice(entropy_map, 'Quantum Entropy Field')
    plt.savefig('entropy_field.png', dpi=150)
    
    visualize_slice(g_00, 'Spacetime Metric (g_00 component)')
    plt.savefig('metric_g00.png', dpi=150)
    
    # Calculate quantum pressure for visualization
    T_quantum = engine.calculate_quantum_pressure(entropy_map)
    visualize_slice(T_quantum, 'Quantum Pressure (Antigravity Term)')
    plt.savefig('quantum_pressure.png', dpi=150)
    
    print("\n" + "=" * 60)
    print("Simulation Complete!")
    print("=" * 60)
    print("\nGenerated outputs:")
    print("  • mass_distribution.png")
    print("  • entropy_field.png")
    print("  • metric_g00.png")
    print("  • quantum_pressure.png")
    print("\nMetric Statistics:")
    print(f"  • g_00 mean: {np.mean(g_00):.6f}")
    print(f"  • g_00 std:  {np.std(g_00):.6e}")
    print(f"  • g_00 min:  {np.min(g_00):.6f}")
    print(f"  • g_00 max:  {np.max(g_00):.6f}")
    print("\nQuantum Pressure Statistics:")
    print(f"  • T_quantum mean: {np.mean(T_quantum):.6e}")
    print(f"  • T_quantum std:  {np.std(T_quantum):.6e}")

if __name__ == "__main__":
    main()
