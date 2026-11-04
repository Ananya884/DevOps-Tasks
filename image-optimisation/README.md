# Docker Image Optimisation (Python / Flask)

Reduced a Flask app image from 1.64 GB to 106 MB (about 94% smaller) without
changing the application. Each change was built and measured separately.

See SIZES.md for the full table. Dockerfile.v0 to Dockerfile.v5 are kept so
every step can be reproduced:

    docker build -f Dockerfile.v4 -t py-app:v4 .
    docker images py-app

## What each step showed

- **Base image (v0 to v1):** python:3.12 includes compilers and many system packages. Switching to slim saved about 1.4 GB, the biggest single win.
- **Layer hygiene (v1 to v2):** --no-cache-dir, copying requirements.txt before the code, and a .dockerignore saved little space but make rebuilds faster.
- **Multi-stage on slim (v3):** no size gain, because this app has no build-only tools to leave behind. Multi-stage helps when dependencies need compilers or headers.
- **Alpine (v4):** saved about 100 MB more by using a smaller base.
- **Non-root user (v5):** same size, safer runtime.

## Trade-offs

Alpine uses musl instead of glibc. Packages with C extensions may need to be
compiled or may lack prebuilt wheels, which can erase the size advantage and
slow builds. For this app (Flask, requests, gunicorn) it works cleanly.
