# Quick Start Guide

## Installation (5 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Purmamarca/Aethelgard-QGF.git
cd Aethelgard-QGF
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `numpy` - Numerical computing
- `matplotlib` - Visualization

Optional:

```bash
pip install -r requirements-optional.txt   # plotly, dash
pip install -r requirements-dev.txt        # pytest, pytest-cov, ruff
```

### Step 3: Run the Example

```bash
python example_simulation.py
```

**Expected Output:**

```
============================================================
Aethelgard-QGF Simulation
Quantum Gravitational Field with Antigravity Effects
============================================================

[1/4] Creating mass distribution...
[2/4] Generating quantum entropy field...
[3/4] Solving modified Einstein field equations...
Synthesizing metric for Aethelgard-QGF...
[4/4] Generating visualizations...

============================================================
Simulation Complete!
============================================================

Generated outputs:
  • mass_distribution.png
  • entropy_field.png
  • metric_g00.png
  • quantum_pressure.png

Metric Statistics:
  • g_00 mean: 1.000XXX
  • g_00 std:  X.XXXe-XX
  ...
```

### Step 4: View Results

The simulation generates four PNG files:

1. **mass_distribution.png** - Shows the Gaussian mass distribution
2. **entropy_field.png** - Quantum entropy field with fluctuations
3. **metric_g00.png** - Spacetime curvature (time-time metric component)
4. **quantum_pressure.png** - Antigravity pressure from entropy gradients

## Basic Usage

### Minimal Example

```python
from aethelgard_engine import AethelgardEngine
import numpy as np

# Create engine
engine = AethelgardEngine(grid_size=32, domain_size=10.0)

# Define inputs
mass = np.zeros((32, 32, 32))
mass[15:17, 15:17, 15:17] = 1e10  # Central mass

entropy = np.random.rand(32, 32, 32)  # Quantum fluctuations

# Solve
metric = engine.solve_field_equations(mass, entropy, iterations=100)

# Extract time-time component
g_00 = metric[..., 0, 0]
print(f"Metric range: [{g_00.min():.4f}, {g_00.max():.4f}]")
```

### Custom Scenario: Black Hole with Quantum Core

```python
import numpy as np
from aethelgard_engine import AethelgardEngine

# Initialize
engine = AethelgardEngine(grid_size=64, domain_size=20.0)

# Create massive central object
x = np.linspace(0, 20, 64)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
r = np.sqrt((X-10)**2 + (Y-10)**2 + (Z-10)**2)

# Mass distribution (1/r² profile)
mass = 1e12 / (r**2 + 0.1)  # Avoid singularity with +0.1

# High entropy at core (quantum repulsion)
entropy = np.exp(-r**2 / 0.5)  # Concentrated at center

# Solve
metric = engine.solve_field_equations(mass, entropy, iterations=200)

# Analyze
g_00 = metric[..., 0, 0]
print(f"Central g_00: {g_00[32,32,32]:.6f}")
print(f"Edge g_00: {g_00[0,0,0]:.6f}")
```

## Understanding the Physics

### What Does Each Component Mean?

| Component             | Physical Meaning                 | Effect                  |
| --------------------- | -------------------------------- | ----------------------- |
| **Mass Distribution** | Classical matter density (kg/m³) | Attractive gravity      |
| **Entropy Field**     | Quantum information density      | Repulsive "antigravity" |
| **Metric g_00**       | Time dilation factor             | g_00 > 1: time slows    |
| **Quantum Pressure**  | Repulsive stress-energy          | Counteracts collapse    |

### Interpreting Results

**Metric Component g_00:**

- **g_00 = 1.0**: Flat spacetime (Minkowski)
- **g_00 > 1.0**: Positive curvature (mass attraction dominates)
- **g_00 < 1.0**: Negative curvature (quantum repulsion dominates)

**Quantum Pressure:**

- **Positive values**: Repulsive effect (antigravity)
- **Negative values**: Attractive enhancement
- **Zero**: No quantum contribution

## Common Use Cases

### 1. Dark Energy Simulation

Model cosmological expansion from quantum vacuum:

```python
# Uniform low-level entropy (quantum vacuum)
entropy = np.ones((32, 32, 32)) * 0.1

# Add small perturbations
entropy += 0.01 * np.random.randn(32, 32, 32)

# Minimal mass
mass = np.zeros((32, 32, 32))

metric = engine.solve_field_equations(mass, entropy, iterations=100)
```

### 2. Wormhole Stabilization

Use quantum pressure to prevent wormhole collapse:

```python
# Create wormhole throat geometry
r = np.sqrt((X-10)**2 + (Y-10)**2 + (Z-10)**2)
mass = 1e11 * np.exp(-r**2 / 2.0)  # Throat mass

# High entropy at throat for stabilization
entropy = 5.0 * np.exp(-r**2 / 1.0)

metric = engine.solve_field_equations(mass, entropy, iterations=150)
```

### 3. Quantum Star (Gravastar)

Model a star with quantum core preventing collapse:

```python
# Stellar mass distribution
mass = 1e12 * np.exp(-r**2 / 5.0)

# Quantum core (high entropy inside)
entropy = np.where(r < 2.0, 10.0, 0.1)

metric = engine.solve_field_equations(mass, entropy, iterations=200)
```

## Troubleshooting

### Issue: Simulation is slow

**Solution:** Reduce grid size or iterations

```python
engine = AethelgardEngine(grid_size=16, domain_size=10.0)  # Faster
metric = engine.solve_field_equations(mass, entropy, iterations=50)
```

### Issue: Results look uniform

**Solution:** Increase mass or entropy contrast

```python
mass[15:17, 15:17, 15:17] = 1e15  # Stronger mass
entropy = 10.0 * np.random.rand(32, 32, 32)  # Larger entropy range
```

### Issue: Numerical instabilities

**Solution:**

1. Reduce iteration count
2. Smooth input fields
3. Use smaller domain size

```python
from scipy.ndimage import gaussian_filter

# Smooth inputs
mass = gaussian_filter(mass, sigma=1.0)
entropy = gaussian_filter(entropy, sigma=1.0)
```

## Running Tests

Verify installation:

```bash
python -m unittest test_aethelgard -v
```

Expected: All tests pass (11-12 tests)

## Next Steps

1. **Read the README.md** - Overview and theoretical background
2. **Read TECHNICAL_DOCS.md** - Deep dive into mathematics
3. **Modify example_simulation.py** - Experiment with parameters
4. **Create your own scenarios** - Explore quantum gravity effects

## Getting Help

- **Documentation**: See `README.md` and `TECHNICAL_DOCS.md`
- **Examples**: Check `example_simulation.py`
- **Tests**: Review `test_aethelgard.py` for usage patterns

## Performance Tips

### For Faster Simulations

```python
# Small grid
engine = AethelgardEngine(grid_size=16, domain_size=5.0)

# Fewer iterations
metric = engine.solve_field_equations(mass, entropy, iterations=30)
```

### For Higher Accuracy

```python
# Large grid
engine = AethelgardEngine(grid_size=64, domain_size=20.0)

# More iterations
metric = engine.solve_field_equations(mass, entropy, iterations=200)
```

### Memory Usage

| Grid Size | Approximate Memory |
| --------- | ------------------ |
| 16³       | ~10 MB             |
| 32³       | ~80 MB             |
| 64³       | ~640 MB            |
| 128³      | ~5 GB              |

---

**Happy exploring the quantum nature of spacetime!** 🌌
