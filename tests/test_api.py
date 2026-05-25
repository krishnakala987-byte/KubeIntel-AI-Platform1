
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'kubeops-api'))


def test_log_analyzer_healthy():
    from log_analyzer import parse_logs
    result = parse_logs("INFO: application started successfully")
    assert result["overall_status"] == "HEALTHY"
    assert result["error_count"] == 0


def test_log_analyzer_detects_crashloop():
    from log_analyzer import parse_logs
    result = parse_logs("CrashLoopBackOff detected in pod")
    assert result["error_count"] > 0


def test_log_analyzer_detects_oom():
    from log_analyzer import parse_logs
    result = parse_logs("OOMKilled: container exceeded memory limit")
    assert result["overall_status"] == "CRITICAL"


def test_parse_logs_counts_lines():
    from log_analyzer import parse_logs
    logs = "line one\nline two\nline three"
    result = parse_logs(logs)
    assert result["total_lines"] == 3


def test_health_endpoint():
    os.environ["GROQ_API_KEY"] = "test-key-placeholder"
    from app import app
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_analyze_endpoint_missing_query():
    os.environ["GROQ_API_KEY"] = "test-key-placeholder"
    from app import app
    client = app.test_client()
    response = client.post('/api/v1/analyze',
        json={"context": "some context"},
        content_type='application/json')
    assert response.status_code == 400
