"""
GPU-Accelerated Aethelgard Engine

This module provides GPU acceleration for the Aethelgard-QGF engine using CuPy.
CuPy is a NumPy-compatible library that runs on NVIDIA GPUs with CUDA.

Installation:
    pip install cupy-cuda12x  # For CUDA 12.x
    # Or see https://docs.cupy.dev/en/stable/install.html for other versions

Usage:
    from aethelgard_engine_gpu import AethelgardEngineGPU
    
    engine = AethelgardEngineGPU(grid_size=128, domain_size=20.0)
    # ... rest is identical to CPU version
"""

import warnings

import numpy as np

try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    warnings.warn(
        "CuPy not found; falling back to CPU (NumPy). Install with: pip install cupy-cuda12x",
        RuntimeWarning,
        stacklevel=2,
    )
    # Fallback: use numpy as cp
    import numpy as cp


class AethelgardEngineGPU:
    """
    GPU-accelerated AGI-optimized solver for Aethelgard-QGF.
    
    Identical interface to AethelgardEngine but runs on GPU when available.
    Automatically falls back to CPU if CuPy is not installed.
    """
    
    def __init__(self, grid_size=32, domain_size=10.0, use_gpu=True):
        """
        Initialize the GPU-accelerated engine.
        
        Parameters:
        -----------
        grid_size : int
            Number of grid points per dimension
        domain_size : float
            Physical size of simulation domain in meters
        use_gpu : bool
            If True and GPU available, use GPU. If False, use CPU.
        """
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
        
        # Determine compute backend
        self.use_gpu = use_gpu and GPU_AVAILABLE
        self.xp = cp if self.use_gpu else np
        
        if self.use_gpu:
            print("Using GPU acceleration (CuPy)")
            # Print GPU info
            try:
                device = cp.cuda.Device()
                print(f"   Device: {device.compute_capability}")
                mem_info = cp.cuda.runtime.memGetInfo()
                print(f"   Free memory: {mem_info[0] / 1e9:.2f} GB")
            except Exception:
                pass
        else:
            print("Using CPU (NumPy)")
        
        # Physical Constraints & Limits
        self.causality_limit = (0.1, 10.0)

        # Initialize Spacetime Grid (Minkowski start)
        self.metric = self.xp.zeros((self.N, self.N, self.N, 4, 4))
        for i in range(4):
            self.metric[..., i, i] = 1.0  # Diagonal components
    
    def calculate_quantum_pressure(self, entropy_field):
        """
        Implements the 'Antigravity' component via Negative Energy Density.
        
        GPU-accelerated version using CuPy arrays.
        
        Parameters:
        -----------
        entropy_field : cupy.ndarray or numpy.ndarray
            Quantum entropy field
            
        Returns:
        --------
        T_quantum : cupy.ndarray or numpy.ndarray
            Quantum pressure field
        """
        # Ensure input is on correct device
        if self.use_gpu and isinstance(entropy_field, np.ndarray):
            entropy_field = cp.asarray(entropy_field)
        elif not self.use_gpu and hasattr(entropy_field, 'get'):
            entropy_field = entropy_field.get()
        
        # S = A / 4G_hbar -> Localized entropy gradients
        grad_S = self.xp.gradient(entropy_field, self.dx)
        laplacian_S = self.xp.zeros_like(entropy_field)
        
        for i, g in enumerate(grad_S):
            laplacian_S += self.xp.gradient(g, self.dx)[i]
        
        # The 'Antigravity' Term: Repulsive Stress-Energy (T_quantum)
        T_quantum = (self.hbar * self.c / (self.dx**4)) * laplacian_S
        return T_quantum
    
    def solve_field_equations(self, mass_distribution, entropy_map, iterations=50, verbose=True):
        """
        Iterative solver for G_mu_nu + Lambda*g_mu_nu = 8*pi*G*T_mu_nu.
        
        GPU-accelerated version.
        
        Parameters:
        -----------
        mass_distribution : array-like
            Mass density field (kg/m³)
        entropy_map : array-like
            Quantum entropy field
        iterations : int
            Number of solver iterations
        verbose : bool
            Print progress messages
            
        Returns:
        --------
        metric : cupy.ndarray or numpy.ndarray
            Spacetime metric tensor
        """
        # Security: Input validation
        if not isinstance(iterations, int) or iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")
        if iterations > 10000:
            raise ValueError("Iterations exceeds maximum limit of 10000.")

        target_shape = (self.N, self.N, self.N)
        if hasattr(mass_distribution, 'shape') and mass_distribution.shape != target_shape:
            raise ValueError(
                f"Mass distribution shape {mass_distribution.shape} "
                f"must match grid size {target_shape}."
            )

        if hasattr(entropy_map, 'shape') and entropy_map.shape != target_shape:
            raise ValueError(
                f"Entropy map shape {entropy_map.shape} "
                f"must match grid size {target_shape}."
            )

        if verbose:
            backend = "GPU (CuPy)" if self.use_gpu else "CPU (NumPy)"
            print(f"Synthesizing metric for Aethelgard-QGF on {backend}...")
        
        # Transfer data to GPU if needed
        if self.use_gpu:
            if isinstance(mass_distribution, np.ndarray):
                mass_distribution = cp.asarray(mass_distribution)
            if isinstance(entropy_map, np.ndarray):
                entropy_map = cp.asarray(entropy_map)
        else:
            if hasattr(mass_distribution, 'get'):
                mass_distribution = mass_distribution.get()
            if hasattr(entropy_map, 'get'):
                entropy_map = entropy_map.get()
        
        current_geometry = self.metric.copy()
        
        # Pre-compute quantum pressure (doesn't change during iteration)
        T_repulsive = self.calculate_quantum_pressure(entropy_map)
        
        for i in range(iterations):
            # 1. Compute Classical Stress (Attractive)
            T_classic = mass_distribution * (self.c**2)
            
            # 2. Total Stress-Energy Tensor T_total
            T_total = T_classic - T_repulsive  # Negative sign allows for 'antigravity' effects
            
            # 3. Update Metric based on Einstein Tensor G_mu_nu
            curvature_update = (8 * self.xp.pi * self.G / self.c**4) * T_total
            current_geometry[..., 0, 0] += 0.01 * curvature_update
            
            # PHYSICAL CONSTRAINT: Causality Clamp
            current_geometry[..., 0, 0] = self.xp.clip(
                current_geometry[..., 0, 0], 
                self.causality_limit[0], 
                self.causality_limit[1]
            )

            # Progress indicator
            if verbose and (i + 1) % 20 == 0:
                print(f"  Iteration {i+1}/{iterations}")
        
        self.metric = current_geometry
        return self.metric
    
    def to_cpu(self, array):
        """
        Transfer array from GPU to CPU.
        
        Parameters:
        -----------
        array : cupy.ndarray or numpy.ndarray
            Array to transfer
            
        Returns:
        --------
        numpy.ndarray
            Array on CPU
        """
        if hasattr(array, 'get'):
            return array.get()
        return array
    
    def to_gpu(self, array):
        """
        Transfer array from CPU to GPU.
        
        Parameters:
        -----------
        array : numpy.ndarray or cupy.ndarray
            Array to transfer
            
        Returns:
        --------
        cupy.ndarray
            Array on GPU
        """
        if self.use_gpu and isinstance(array, np.ndarray):
            return cp.asarray(array)
        return array
    
    def get_memory_usage(self):
        """
        Get current GPU memory usage.
        
        Returns:
        --------
        dict
            Memory usage statistics
        """
        if self.use_gpu:
            mem_info = cp.cuda.runtime.memGetInfo()
            return {
                'free': mem_info[0] / 1e9,  # GB
                'total': mem_info[1] / 1e9,  # GB
                'used': (mem_info[1] - mem_info[0]) / 1e9  # GB
            }
        else:
            return {'message': 'CPU mode - no GPU memory tracking'}


def benchmark_cpu_vs_gpu(grid_sizes=None):
    """
    Benchmark CPU vs GPU performance.

    Parameters:
    -----------
    grid_sizes : list, optional
        List of grid sizes to test. Defaults to [32, 64, 128].
    """
    if grid_sizes is None:
        grid_sizes = [32, 64, 128]
    import time
    
    print("=" * 70)
    print("CPU vs GPU BENCHMARK")
    print("=" * 70)
    
    results = []
    
    for N in grid_sizes:
        print(f"\nGrid size: {N}³ ({N**3:,} points)")
        
        # Create test data
        mass = np.random.rand(N, N, N) * 1e10
        entropy = np.random.rand(N, N, N) * 5.0
        
        # CPU benchmark
        print("  Testing CPU...")
        engine_cpu = AethelgardEngineGPU(grid_size=N, use_gpu=False)
        start = time.time()
        engine_cpu.solve_field_equations(mass, entropy, iterations=50, verbose=False)
        cpu_time = time.time() - start
        print(f"    CPU time: {cpu_time:.2f} seconds")
        
        # GPU benchmark (if available)
        if GPU_AVAILABLE:
            print("  Testing GPU...")
            engine_gpu = AethelgardEngineGPU(grid_size=N, use_gpu=True)
            
            # Warm-up
            _ = engine_gpu.solve_field_equations(mass, entropy, iterations=5, verbose=False)
            
            # Actual benchmark
            start = time.time()
            engine_gpu.solve_field_equations(
                mass, entropy, iterations=50, verbose=False
            )
            gpu_time = time.time() - start
            print(f"    GPU time: {gpu_time:.2f} seconds")
            
            speedup = cpu_time / gpu_time
            print(f"    Speedup: {speedup:.2f}x")
            
            results.append({
                'grid_size': N,
                'cpu_time': cpu_time,
                'gpu_time': gpu_time,
                'speedup': speedup
            })
        else:
            results.append({
                'grid_size': N,
                'cpu_time': cpu_time,
                'gpu_time': None,
                'speedup': None
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)
    print(f"{'Grid Size':<12} {'CPU Time':<12} {'GPU Time':<12} {'Speedup':<12}")
    print("-" * 70)
    for r in results:
        gpu_str = f"{r['gpu_time']:.2f}s" if r['gpu_time'] else "N/A"
        speedup_str = f"{r['speedup']:.2f}x" if r['speedup'] else "N/A"
        points = r['grid_size']**3
        cpu_t = r['cpu_time']
        print(f"{points:<12,} {cpu_t:.2f}s{'':<7} {gpu_str:<12} {speedup_str:<12}")
    
    return results


if __name__ == "__main__":
    # Run benchmark
    benchmark_cpu_vs_gpu(grid_sizes=[32, 64])
