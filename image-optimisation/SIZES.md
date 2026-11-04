| Version | Change | Disk usage | Compressed | Saved vs previous |
|---------|--------|-----------|------------|-------------------|
| v0 | Baseline: python:3.12 full image | 1.64 GB | 421 MB | - |
| v1 | Base image changed to python:3.12-slim | 210 MB | 52.1 MB | ~1.43 GB |
| v2 | --no-cache-dir, cached requirements layer, .dockerignore, copy only app.py | 205 MB | 49.9 MB | ~5 MB |
| v3 | Multi-stage build on slim (venv copied to runtime stage) | 209 MB | 50.4 MB | +4 MB (no gain: no build-only tools to drop) |
| v4 | Multi-stage build on python:3.12-alpine | 106 MB | 25.2 MB | ~103 MB |
| v5 | Same as v4, runs as non-root user (appuser) | 106 MB | 25.2 MB | none (security hardening) |
