# Multi-Service App (Docker Compose)

A containerized three-tier app: React frontend, Node.js API, and PostgreSQL,
orchestrated with Docker Compose and deployed on an AWS EC2 instance.

## Architecture

Browser -> nginx (frontend container, port 3000) -> Node.js API (port 5000) -> PostgreSQL (port 5432)

- **frontend**: React (Vite) built in a multi-stage Dockerfile and served by nginx.
  nginx also reverse-proxies `/api/` requests to the API container.
- **api**: Node.js + Express. `/api/health` checks the service, `/api/time` queries PostgreSQL.
- **db**: PostgreSQL 16 with a named volume for persistent data and a healthcheck.

Only the frontend is published (port 3000). The API and database are reachable
only inside the Compose network.

## Run it

```bash
# 1. Create a .env file
POSTGRES_USER=appuser
POSTGRES_PASSWORD=<your-password>
POSTGRES_DB=appdb

# 2. Start everything
docker compose up -d --build

# 3. Open http://<host>:3000
```

## Key design decisions

- **Multi-stage build** for the frontend: Node is used only to build; the final image is nginx plus static files.
- **Layer caching**: `package.json` is copied and dependencies installed before the source code, so rebuilds are fast.
- **Healthcheck + `depends_on: service_healthy`**: the API starts only after PostgreSQL accepts connections.
- **Named volume (`pgdata`)**: data survives container removal (verified with `docker compose down` / `up`).
- **Secrets in `.env`**, excluded from Git via `.gitignore`.
- **Least exposure**: SSH and port 3000 restricted to my IP in the EC2 security group.

## Verify

```bash
curl http://localhost:3000/api/health   # {"status":"ok"}
curl http://localhost:3000/api/time     # current time from PostgreSQL
```
