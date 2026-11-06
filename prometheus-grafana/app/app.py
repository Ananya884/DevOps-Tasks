import random
import time
from flask import Flask, Response, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["endpoint"]
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.path).observe(latency)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route("/")
def home():
    return "Hello from the metrics demo app!\n"

@app.route("/slow")
def slow():
    time.sleep(random.uniform(0.1, 1.5))
    return "That was slow.\n"

@app.route("/error")
def error():
    if random.random() < 0.5:
        return "Something broke\n", 500
    return "Lucky, no error\n"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
