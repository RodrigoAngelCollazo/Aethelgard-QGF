# Contributing to Aethelgard-QGF

Thank you for your interest in contributing. This document outlines how to get started.

## Development Setup

```bash
git clone https://github.com/Purmamarca/Aethelgard-QGF.git
cd Aethelgard-QGF
pip install -e ".[dev]"
```

## Running Tests

```bash
python run_tests.py
# or
pytest tests/ -v
```

## Code Style

- Use [Ruff](https://docs.astral.sh/ruff/) for linting: `ruff check .`
- Follow existing patterns in the codebase
- Add docstrings for new public functions and classes

## Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes with tests
3. Ensure `python run_tests.py` passes
4. Run `ruff check .` (or equivalent lint)
5. Open a PR with a clear description of the change

## Areas of Interest

- **Numerical methods**: Improved solvers, stability, convergence
- **Physics**: Model refinements, additional scenarios
- **Performance**: GPU optimizations, memory efficiency
- **Documentation**: Examples, API docs, tutorials
- **Testing**: Edge cases, property-based tests

## Questions

Open an [Issue](https://github.com/Purmamarca/Aethelgard-QGF/issues) or start a [Discussion](https://github.com/Purmamarca/Aethelgard-QGF/discussions).
