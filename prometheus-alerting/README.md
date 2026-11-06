# Task 8: Alerting Rules for CPU and Memory

Prometheus alerting rules that fire when CPU usage stays above 80% for 5 minutes or memory usage goes above 90%. Alerts are routed to Alertmanager, which sends them to a webhook receiver. Everything runs with Docker Compose.

## Structure

- `prometheus/prometheus.yml`: scrape config, rule file, Alertmanager address
- `prometheus/alert_rules.yml`: the two alert rules
- `alertmanager/alertmanager.yml`: routing and webhook receiver
- `webhook/webhook.py`: small receiver that prints every alert it gets
- `docker-compose.yml`: Prometheus, Alertmanager, node-exporter, webhook

## Alert rules

| Alert           | Condition                    | For   | Severity |
|-----------------|------------------------------|-------|----------|
| HighCpuUsage    | CPU usage above 80%          | 5 min | warning  |
| HighMemoryUsage | Memory usage above 90%       | 2 min | critical |

## Expressions

CPU usage (percent):

    100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)

Memory usage (percent):

    (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

## Run

    docker compose up -d

Prometheus is on port 9090 and Alertmanager on port 9093. The webhook output can be read with:

    docker compose logs webhook

## Test

The CPU alert was triggered by running two busy loops on the 2-vCPU server:

    timeout 720 yes > /dev/null &
    timeout 720 yes > /dev/null &

After about 7 minutes the alert went from pending to firing, and the webhook printed:

    ALERT firing HighCpuUsage - High CPU usage on node-exporter:9100

After the load was stopped, the alert cleared and the webhook printed:

    ALERT resolved HighCpuUsage - High CPU usage on node-exporter:9100

## Cleanup

    docker compose down
