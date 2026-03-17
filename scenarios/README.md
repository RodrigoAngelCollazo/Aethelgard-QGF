# Aethelgard-QGF Scenarios

This directory contains advanced physics scenarios demonstrating different applications of the Aethelgard-QGF engine.

## Available Scenarios

### 1. Black Hole with Quantum Core

**File**: `black_hole_quantum_core.py`

Models a massive object with quantum-repulsive core preventing singularity formation.

**Physics**:

- 1/r² mass distribution (Schwarzschild-like)
- High entropy at core creates antigravity pressure
- Prevents classical singularity
- Results in "gravastar" or "quantum star" configuration

**Run**:

```bash
python -m scenarios.black_hole_quantum_core
```

**Outputs**:

- `black_hole_radial_profiles.png` - Radial profiles of all fields
- `black_hole_2d_slices.png` - 2D cross-sections

---

### 2. Wormhole Stabilization

**File**: `wormhole_stabilization.py`

Explores using quantum pressure to stabilize a wormhole throat without classical exotic matter.

**Physics**:

- Toroidal mass distribution around throat
- Maximum entropy at throat radius
- Quantum pressure provides outward force
- Effective negative energy density

**Run**:

```bash
python -m scenarios.wormhole_stabilization
```

**Outputs**:

- `wormhole_radial_profiles.png` - Radial analysis
- `wormhole_2d_slices.png` - Throat geometry visualization

---

### 3. Dark Energy Cosmology

**File**: `dark_energy_cosmology.py`

Models dark energy as emergent from quantum vacuum entropy.

**Physics**:

- Nearly uniform vacuum entropy
- Quantum fluctuations create structure seeds
- Effective cosmological constant
- Accelerated expansion mechanism

**Run**:

```bash
python -m scenarios.dark_energy_cosmology
```

**Outputs**:

- `dark_energy_statistics.png` - Statistical analysis and power spectrum
- `dark_energy_fields.png` - Spatial field distributions

---

## Running All Scenarios

```bash
# Run each scenario
python -m scenarios.black_hole_quantum_core
python -m scenarios.wormhole_stabilization
python -m scenarios.dark_energy_cosmology
```

All outputs are saved to `scenarios/output/` directory.

## Customizing Scenarios

Each scenario can be customized by modifying parameters:

```python
# Example: Larger grid for higher resolution
create_black_hole_scenario(grid_size=128, domain_size=30.0)

# Example: Different wormhole throat size
# Edit r_throat parameter in wormhole_stabilization.py
```

## Scenario Comparison

| Scenario    | Grid Size | Iterations | Runtime\* | Key Feature            |
| ----------- | --------- | ---------- | --------- | ---------------------- |
| Black Hole  | 64³       | 200        | ~2 min    | Singularity prevention |
| Wormhole    | 48³       | 150        | ~1 min    | Exotic geometry        |
| Dark Energy | 32³       | 100        | ~30 sec   | Cosmological constant  |

\*Approximate runtime on modern CPU

## Physical Interpretations

### Black Hole Scenario

- **Question**: Can quantum effects prevent singularities?
- **Answer**: High entropy at core creates repulsive pressure
- **Result**: Finite-density core instead of infinite-density singularity

### Wormhole Scenario

- **Question**: Can wormholes exist without exotic matter?
- **Answer**: Quantum entropy gradients provide necessary repulsion
- **Result**: Stabilized throat geometry

### Dark Energy Scenario

- **Question**: What is the origin of dark energy?
- **Answer**: Quantum vacuum has intrinsic entropy structure
- **Result**: Emergent cosmological constant from information geometry

## Advanced Usage

### Creating Custom Scenarios

```python
from aethelgard_engine import AethelgardEngine
import numpy as np

# Initialize
engine = AethelgardEngine(grid_size=32, domain_size=10.0)

# Define your custom fields
mass = # ... your mass distribution
entropy = # ... your entropy field

# Solve
metric = engine.solve_field_equations(mass, entropy, iterations=100)

# Analyze results
# ... your analysis code
```

### Combining Scenarios

```python
# Example: Binary black hole system
# Create two black hole cores at different locations

center1 = [3.0, 5.0, 5.0]
center2 = [7.0, 5.0, 5.0]

mass1 = create_gaussian(grid, center1, sigma=1.0)
mass2 = create_gaussian(grid, center2, sigma=1.0)

total_mass = mass1 + mass2
# ... continue with simulation
```

## Troubleshooting

**Scenario runs slowly**:

- Reduce `grid_size` parameter
- Reduce `iterations` parameter
- Use GPU acceleration (see main README)

**Results look uniform**:

- Increase entropy contrast
- Increase mass concentration
- Check parameter values

**Numerical instabilities**:

- Reduce iteration count
- Smooth input fields with gaussian_filter
- Use smaller domain size

## References

Each scenario is inspired by theoretical work:

- **Black Hole**: Mazur & Mottola (2004) on gravastars
- **Wormhole**: Morris & Thorne (1988) on traversable wormholes
- **Dark Energy**: Verlinde (2011) on emergent gravity

---

**Explore the quantum nature of spacetime!** 🌌
