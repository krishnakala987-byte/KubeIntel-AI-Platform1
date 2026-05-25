import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from ai_engine import analyze_with_ai, generate_runbook, score_deployment_health
from log_analyzer import parse_logs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

metrics.info("kubeintel_api_info", "KubeIntel API", version="2.0.0")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "kubeops-api", "version": "2.0.0"})


@app.route("/ready", methods=["GET"])
def ready():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"status": "not ready", "reason": "GROQ_API_KEY missing"}), 503
    return jsonify({"status": "ready"})


@app.route("/api/v1/analyze", methods=["POST"])
def analyze():
    """General Kubernetes AI analysis endpoint."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    context = data.get("context", "")
    query = data.get("query", "")
    mode = data.get("mode", "general")

    if not query:
        return jsonify({"error": "query field is required"}), 400

    logger.info(f"Analysis request | mode={mode} | query_len={len(query)}")
    result = analyze_with_ai(context, query, mode)
    return jsonify({"response": result, "mode": mode})


@app.route("/api/v1/analyze/logs", methods=["POST"])
def analyze_logs():
    """Log ingestion + anomaly detection + AI triage."""
    data = request.get_json()
    if not data or "logs" not in data:
        return jsonify({"error": "logs field required"}), 400

    raw_logs = data["logs"]
    parsed = parse_logs(raw_logs)

    ai_context = f"Log analysis results:\n{json.dumps(parsed, indent=2)}\n\nRaw logs sample:\n{raw_logs[:3000]}"
    ai_query = "Analyze these Kubernetes logs. What are the root causes and what exact steps should I take to fix each issue?"

    ai_response = analyze_with_ai(ai_context, ai_query, mode="logs")

    return jsonify({
        "parsed_analysis": parsed,
        "ai_diagnosis": ai_response,
    })


@app.route("/api/v1/incident/triage", methods=["POST"])
def triage_incident():
    """Incident triage: takes cluster state + symptoms, returns AI diagnosis."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    symptoms = data.get("symptoms", "")
    cluster_state = data.get("cluster_state", "")
    namespace = data.get("namespace", "default")

    context = f"Namespace: {namespace}\n\nCluster State:\n{cluster_state}\n\nSymptoms:\n{symptoms}"
    result = analyze_with_ai(context, symptoms, mode="incident")

    return jsonify({"triage_report": result, "namespace": namespace})


@app.route("/api/v1/incident/runbook", methods=["POST"])
def generate_incident_runbook():
    """Auto-generate a production runbook for an incident."""
    data = request.get_json()
    if not data or "incident" not in data:
        return jsonify({"error": "incident field required"}), 400

    runbook = generate_runbook(data["incident"])
    return jsonify({"runbook": runbook})


@app.route("/api/v1/deployment/score", methods=["POST"])
def score_deployment():
    """Score a Kubernetes deployment YAML for production readiness."""
    data = request.get_json()
    if not data or "yaml_content" not in data:
        return jsonify({"error": "yaml_content field required"}), 400

    score = score_deployment_health(data["yaml_content"])
    return jsonify(score)


@app.route("/api/v1/deployment/review", methods=["POST"])
def review_deployment():
    """Full deployment YAML review with AI recommendations."""
    data = request.get_json()
    if not data or "yaml_content" not in data:
        return jsonify({"error": "yaml_content field required"}), 400

    context = f"Kubernetes Deployment YAML:\n{data['yaml_content']}"
    query = "Review this deployment for production readiness. Check resource limits, health probes, security context, image pull policy, and anti-affinity rules. Provide specific fixes."
    result = analyze_with_ai(context, query, mode="deployment")

    return jsonify({"review": result})


@app.route("/api/v1/security/audit", methods=["POST"])
def security_audit():
    """AI-powered Kubernetes security posture audit."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    manifests = data.get("manifests", "")
    query = "Perform a security audit. Check for: missing RBAC, privileged containers, hostNetwork usage, missing NetworkPolicies, secrets in env vars, missing resource limits, and pod security standards compliance."
    result = analyze_with_ai(manifests, query, mode="security")

    return jsonify({"audit_report": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)