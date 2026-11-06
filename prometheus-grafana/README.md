# Task 7: App Metrics with Prometheus and Grafana

A Flask app exposes a `/metrics` endpoint. Prometheus scrapes it every 5 seconds, and a Grafana dashboard shows request rate, p95 latency and error rate. Everything runs with Docker Compose.

## Structure

- `app/`: Flask app (`app.py`), `requirements.txt`, `Dockerfile`
- `prometheus/prometheus.yml`: scrape config (target `app:5000`)
- `grafana/dashboard.json`: dashboard exported as JSON
- `docker-compose.yml`: app, Prometheus and Grafana

## App routes

| Route    | Behaviour                               |
|----------|-----------------------------------------|
| /        | fast response                           |
| /slow    | sleeps 0.1 to 1.5 seconds               |
| /error   | returns HTTP 500 about half of the time |
| /metrics | Prometheus metrics                      |

## Custom metrics

- `http_requests_total{method, endpoint, status}`: counter
- `http_request_duration_seconds{endpoint}`: histogram

## Run

    docker compose up -d --build

| Service    | Port | URL                   |
|------------|------|-----------------------|
| Flask app  | 5000 | http://localhost:5000 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana    | 3001 | http://localhost:3001 |

In Grafana, add a Prometheus data source with URL `http://prometheus:9090`, then import `grafana/dashboard.json`.

## Dashboard queries

Request rate:

    sum(rate(http_requests_total[1m])) by (endpoint)

Latency p95:

    histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))

Error rate (share of 5xx responses):

    sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))

## Results

With steady traffic the dashboard showed about 0.55 req/s per route, a p95 latency of about 1.8 s (driven by /slow), and an error rate of 15 to 20 percent (driven by /error).

## Cleanup

    docker compose down -v
