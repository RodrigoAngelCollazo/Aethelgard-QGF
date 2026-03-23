# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-01-14

### Added

- Core `AethelgardEngine` for modified Einstein field equations
- `AethelgardEngineGPU` with CuPy acceleration (10–50× speedup) and CPU fallback
- `AethelgardEngineTimeEvolution` with 3+1 ADM formalism
- Scenarios: black hole quantum core, wormhole stabilization, dark energy cosmology
- Interactive 3D web visualizer (Plotly/Dash)
- CLI entry points: `aethelgard-example`, `aethelgard-viz`, `aethelgard-benchmark`
- Full API reference in `docs/API_REFERENCE.md`
- `pyproject.toml` for installable package and optional extras
- Unit test suite (32 tests) covering core, GPU, security, visualizer

### Security

- Input validation on grid_size, domain_size, iterations, time_steps
- Path traversal prevention in `visualize_evolution`
- Resource exhaustion limits (grid ≤ 256³, iterations ≤ 10000)

### Fixed

- Unicode console crash on Windows when CuPy is missing
- Dependency cleanup: core vs optional vs dev
- Scenario imports via `python -m scenarios.<module>`
