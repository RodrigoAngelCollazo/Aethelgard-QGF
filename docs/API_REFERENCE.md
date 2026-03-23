# Aethelgard-QGF API Reference

**Version:** 1.0.0  
**Spec format:** OpenAPI-style for Python library

---

## 1. Package Overview

```python
import aethelgard
```

| Export | Type | Description |
|--------|------|-------------|
| `AethelgardEngine` | class | CPU solver for modified Einstein field equations |
| `AethelgardEngineGPU` | class | GPU-accelerated solver (CuPy, CPU fallback) |
| `AethelgardEngineTimeEvolution` | class | Time-dependent spacetime evolution (3+1 ADM) |
| `calculate_flux_anomaly` | function | Quantum gravitational flux shift |
| `simulate_antigravity_flux` | function | Antigravity flux simulation |
| `__version__` | str | Package version |

---

## 2. Core Engine: `AethelgardEngine`

### Constructor

```python
AethelgardEngine(
    grid_size: int = 32,
    domain_size: float = 10.0
) -> AethelgardEngine
```

| Parameter | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| `grid_size` | int | 32 | 1 ≤ N ≤ 256 | Grid points per dimension |
| `domain_size` | float | 10.0 | > 0 | Physical domain size (m) |

**Raises:** `ValueError` if constraints violated

**Attributes (read-only):**
- `N`: grid size
- `L`: domain size
- `dx`: grid spacing
- `G`, `c`, `hbar`: physical constants
- `causality_limit`: (0.1, 10.0) for g₀₀ clamping
- `metric`: `ndarray` shape `(N, N, N, 4, 4)` — spacetime metric tensor

---

### Methods

#### `calculate_quantum_pressure`

```python
calculate_quantum_pressure(entropy_field: np.ndarray) -> np.ndarray
```

Computes repulsive stress-energy from entanglement entropy gradients.

| Parameter | Type | Shape | Description |
|-----------|------|-------|-------------|
| `entropy_field` | ndarray | `(N, N, N)` | Quantum entropy S(x,y,z) |

**Returns:** `ndarray` shape `(N, N, N)` — T_quantum (antigravity term)

---

#### `solve_field_equations`

```python
solve_field_equations(
    mass_distribution: np.ndarray,
    entropy_map: np.ndarray,
    iterations: int = 50,
    verbose: bool = True
) -> np.ndarray
```

Iterative solver for G_μν + Λ·g_μν = 8πG·T_μν.

| Parameter | Type | Shape | Constraints | Description |
|-----------|------|-------|-------------|-------------|
| `mass_distribution` | ndarray | `(N, N, N)` | Must match grid | Mass density ρ (kg/m³) |
| `entropy_map` | ndarray | `(N, N, N)` | Must match grid | Entropy field S |
| `iterations` | int | — | 1 ≤ i ≤ 10000 | Solver iterations |
| `verbose` | bool | — | — | Log progress |

**Returns:** `ndarray` shape `(N, N, N, 4, 4)` — metric tensor g_μν

**Raises:** `ValueError` if shapes or iteration limits violated

---

#### `calculate_paradox_hazard`

```python
calculate_paradox_hazard() -> float
```

Estimates causality paradox risk from metric curvature.

**Returns:** `float` in [0.0, 1.0] — 0 = safe, 1 = imminent paradox

---

## 3. GPU Engine: `AethelgardEngineGPU`

Extends engine interface with GPU support. **Interface is a superset of `AethelgardEngine`.**

### Constructor

```python
AethelgardEngineGPU(
    grid_size: int = 32,
    domain_size: float = 10.0,
    use_gpu: bool = True
) -> AethelgardEngineGPU
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_gpu` | bool | True | Use CuPy if available; else NumPy |

**Optional dependency:** `cupy-cuda12x` for GPU acceleration

---

### Additional Methods

#### `to_cpu`

```python
to_cpu(array: np.ndarray | cp.ndarray) -> np.ndarray
```

Transfer array from GPU to CPU.

#### `to_gpu`

```python
to_gpu(array: np.ndarray) -> cp.ndarray
```

Transfer array from CPU to GPU.

#### `get_memory_usage`

```python
get_memory_usage() -> dict
```

**Returns:** `{'free': float, 'total': float, 'used': float}` (GB) or `{'message': str}` in CPU mode

---

## 4. Time Evolution: `AethelgardEngineTimeEvolution`

Subclass of `AethelgardEngine` adding time-stepping.

### Constructor

```python
AethelgardEngineTimeEvolution(
    grid_size: int = 32,
    domain_size: float = 10.0,
    dt: float = 0.01
) -> AethelgardEngineTimeEvolution
```

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `dt` | float | 0 < dt ≤ 1000 | Time step (s) |

---

### Methods

#### `evolve_metric`

```python
evolve_metric(
    mass_distribution: np.ndarray,
    entropy_map: np.ndarray | Callable[[float], np.ndarray],
    time_steps: int = 100,
    entropy_evolution: bool = False,
    verbose: bool = True
) -> dict
```

Evolve spacetime metric forward in time (3+1 ADM).

| Parameter | Type | Description |
|-----------|------|-------------|
| `entropy_map` | ndarray or callable | Static field or `f(t) -> entropy` |
| `time_steps` | int | 1 ≤ steps ≤ 5000 |
| `entropy_evolution` | bool | Allow entropy diffusion |

**Returns:** `dict` with keys `time`, `metric_mean`, `metric_std`, `K_mean`, `entropy_mean`

---

#### `visualize_evolution`

```python
visualize_evolution(output_dir: str = 'output') -> matplotlib.figure.Figure
```

Save time evolution plots. **Rejects** `..`, absolute paths, and `:` in `output_dir`.

---

## 5. Antigravity Module

### `calculate_flux_anomaly`

```python
calculate_flux_anomaly(mass: float, radius: float) -> tuple[float, float]
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `mass` | float | Mass (kg) |
| `radius` | float | Radius (m) |

**Returns:** `(quantum_shift, flux_density)`

---

### `simulate_antigravity_flux`

```python
simulate_antigravity_flux(mass: float, radius: float) -> str
```

**Returns:** Formatted string with flux density and predicted shift

---

## 6. Scenarios (Entry Points)

| Name | Module | Function | Description |
|------|--------|----------|-------------|
| `black_hole` | `scenarios.black_hole_quantum_core` | `create_black_hole_scenario` | Black hole with quantum core |
| `wormhole` | `scenarios.wormhole_stabilization` | `create_wormhole_scenario` | Wormhole stabilization |
| `dark_energy` | `scenarios.dark_energy_cosmology` | `create_dark_energy_scenario` | Dark energy cosmology |

```python
from importlib.metadata import entry_points
scenarios = entry_points(group='aethelgard.scenarios')
create_bh = scenarios['black_hole'].load()
engine, metric, mass, entropy = create_bh(grid_size=64, domain_size=20.0)
```

---

## 7. CLI Entry Points

| Command | Description |
|---------|-------------|
| `aethelgard-example` | Run example simulation |
| `aethelgard-viz` | Launch interactive visualizer (requires `[viz]`) |
| `aethelgard-benchmark` | CPU vs GPU benchmark |

---

## 8. Error Handling

| Exception | Condition |
|-----------|-----------|
| `ValueError` | Invalid `grid_size`, `domain_size`, `iterations`, `time_steps`, shape mismatch, path traversal |
| `ImportError` | Missing optional deps when used (e.g. CuPy, Plotly/Dash) |

---

## 9. Array Conventions

- **Mass distribution:** kg/m³, positive
- **Entropy field:** dimensionless, typically positive
- **Metric:** g_μν in (t,x,y,z) order; g₀₀ clamped to [0.1, 10.0]
- **Grid:** Cartesian, `indexing='ij'`, domain [0, L]³
