# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security issues privately by opening a GitHub Security Advisory:

1. Go to [Security Advisories](https://github.com/Purmamarca/Aethelgard-QGF/security/advisories)
2. Click "Report a vulnerability"
3. Describe the issue and steps to reproduce

We will respond as soon as possible and coordinate disclosure.

## Known Mitigations

- Input validation enforces limits on grid size (≤ 256) and iterations (≤ 10000) to prevent resource exhaustion
- Path traversal is blocked in file output (e.g. `visualize_evolution`)
- Array shapes are validated before computation
