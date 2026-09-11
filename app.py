from flask import Flask, jsonify
import os
import random

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "v1")
# Simulates a bad deploy: set via env var, this version fails health checks intermittently
FAILURE_RATE = float(os.environ.get("FAILURE_RATE", "0"))

@app.route("/")
def index():
    return jsonify(message=f"Hello from capstone-app {VERSION}")

@app.route("/health")
def health():
    if random.random() < FAILURE_RATE:
        return jsonify(status="unhealthy", version=VERSION), 500
    return jsonify(status="healthy", version=VERSION), 200

@app.route("/metrics")
def metrics():
    # Minimal Prometheus-compatible metrics for the analysis-gate step
    healthy = 0 if random.random() < FAILURE_RATE else 1
    body = (
        f'# HELP app_health_status 1 if healthy, 0 if not\n'
        f'# TYPE app_health_status gauge\n'
        f'app_health_status{{version="{VERSION}"}} {healthy}\n'
    )
    return body, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
