<p align="center">
  <img src="https://img.shields.io/badge/Aethelgard--QGF-Quantum%20Gravity-blue?style=for-the-badge" alt="Aethelgard-QGF" />
</p>

<h1 align="center">Aethelgard-QGF</h1>
<p align="center">
  <strong>Quantum Gravitational Field Engine</strong> — Spacetime metrics where entanglement entropy creates repulsive geometry
</p>

<p align="center">
  <a href="https://github.com/Purmamarca/Aethelgard-QGF/actions"><img src="https://img.shields.io/github/actions/workflow/status/Purmamarca/Aethelgard-QGF/ci.yml?branch=main&style=flat-square" alt="CI" /></a>
  <a href="https://github.com/Purmamarca/Aethelgard-QGF/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue?style=flat-square" alt="Python" /></a>
  <a href="https://github.com/Purmamarca/Aethelgard-QGF/blob/main/docs/API_REFERENCE.md"><img src="https://img.shields.io/badge/API-Documented-orange?style=flat-square" alt="API" /></a>
</p>

---

## What is Aethelgard-QGF?

A **production-grade numerical engine** for exploring theoretical spacetime metrics where **quantum information density modifies gravity**. Entanglement entropy gradients create repulsive geometric pressure—a potential antigravity mechanism with applications in black holes, wormholes, and dark energy.

| Feature | Description |
|---------|-------------|
| **Modified Einstein equations** | G_μν + Λ(x)·g_μν = 8πG·T_μν with quantum corrections |
| **GPU acceleration** | 10–50× speedup with CuPy (optional) |
| **Time evolution** | 3+1 ADM formalism, gravitational waves, stellar collapse |
| **Scenarios** | Black hole with quantum core, wormhole stabilization, dark energy cosmology |
| **API spec** | [Full API reference](docs/API_REFERENCE.md) with types and contracts |

---

## Quick Start

```bash
# From PyPI (when published) or local install
pip install -e .

# Or minimal: pip install -r requirements.txt
```

```python
from aethelgard import AethelgardEngine
import numpy as np

engine = AethelgardEngine(grid_size=32, domain_size=10.0)
mass = np.zeros((32, 32, 32))
mass[15:17, 15:17, 15:17] = 1e10
entropy = np.random.rand(32, 32, 32)

metric = engine.solve_field_equations(mass, entropy, iterations=100)
g_00 = metric[..., 0, 0]
print(f"g_00 range: [{g_00.min():.4f}, {g_00.max():.4f}]")
```

### Optional Extras

```bash
pip install "aethelgard-qgf[gpu]"    # CuPy for 10–50× speedup
pip install "aethelgard-qgf[viz]"    # Plotly + Dash for web viz
pip install "aethelgard-qgf[dev]"    # pytest, ruff for development
```

### CLI

```bash
aethelgard-example      # Run example simulation
aethelgard-viz          # Launch interactive 3D viewer (port 8050)
aethelgard-benchmark    # CPU vs GPU benchmark
```

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Scenarios](#scenarios)
- [Theory](#theory)
- [API Reference](#api-reference)
- [Contributing](#contributing)

---

## Installation

```bash
git clone https://github.com/Purmamarca/Aethelgard-QGF.git
cd Aethelgard-QGF
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
python run_tests.py
```

---

## Usage

### CPU Engine

```python
from aethelgard import AethelgardEngine

engine = AethelgardEngine(grid_size=64, domain_size=20.0)
metric = engine.solve_field_equations(mass, entropy, iterations=200)
hazard = engine.calculate_paradox_hazard()  # 0–1 causality risk
```

### GPU Engine (optional)

```python
from aethelgard import AethelgardEngineGPU

engine = AethelgardEngineGPU(grid_size=128, use_gpu=True)
metric = engine.solve_field_equations(mass, entropy)
```

### Time Evolution

```python
from aethelgard import AethelgardEngineTimeEvolution

engine = AethelgardEngineTimeEvolution(grid_size=32, dt=0.01)
history = engine.evolve_metric(mass, entropy_wave, time_steps=100)
engine.visualize_evolution(output_dir="output")
```

---

## Architecture

```
aethelgard/
├── AethelgardEngine          # Core CPU solver
├── AethelgardEngineGPU       # GPU solver (CuPy fallback)
└── AethelgardEngineTimeEvolution  # 3+1 ADM time stepping

scenarios/                    # Physics scenarios
├── black_hole_quantum_core
├── wormhole_stabilization
└── dark_energy_cosmology
```

| Module | Purpose |
|--------|---------|
| `aethelgard_engine` | Core solver, quantum pressure, field equations |
| `aethelgard_engine_gpu` | GPU acceleration with automatic CPU fallback |
| `aethelgard_time_evolution` | Dynamic spacetime evolution |
| `antigravity_engine` | Flux anomaly calculations |
| `scenarios` | Pre-built physics scenarios |

---

## Scenarios

| Scenario | Run | Output |
|----------|-----|--------|
| Black hole + quantum core | `python -m scenarios.black_hole_quantum_core` | Radial profiles, 2D slices |
| Wormhole stabilization | `python -m scenarios.wormhole_stabilization` | Throat geometry |
| Dark energy cosmology | `python -m scenarios.dark_energy_cosmology` | Power spectrum, fields |

See [scenarios/README.md](scenarios/README.md) for details.

---

## Theory

The engine solves modified Einstein field equations:

```
G_μν + Λ(x)·g_μν = 8πG·T_μν
```

With quantum stress-energy:

```
T_total = T_classical - T_quantum = ρ·c² - (ℏc/dx⁴)·∇²S
```

The **negative quantum term** yields repulsive geometry (antigravity).

**Applications:** Dark energy, singularity prevention, wormhole stabilization, inflation seeds.

---

## API Reference

Full specification: **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)**

- Constructor and method signatures
- Parameter types and constraints
- Error handling
- Entry points and CLI

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:

- Numerical method improvements
- Physical model refinements
- Documentation and examples

---

## Citation

```bibtex
@software{aethelgard_qgf_2026,
  title = {Aethelgard-QGF: Quantum Gravitational Field Engine},
  author = {Aethelgard-QGF Project},
  year = {2026},
  url = {https://github.com/Purmamarca/Aethelgard-QGF},
  version = {1.0.0}
}
```

---

## License

MIT — free for academic and commercial use with attribution.

---

## References

- Jacobson (1995) — Thermodynamics of spacetime
- Verlinde (2011) — Emergent gravity
- Susskind (1995) — Holographic principle
- Ryu–Takayanagi (2006) — Holographic entanglement entropy
