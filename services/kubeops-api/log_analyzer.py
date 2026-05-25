import re
from datetime import datetime


ERROR_PATTERNS = {
    "OOMKilled": {"severity": "CRITICAL", "desc": "Container killed due to memory limit exceeded"},
    "CrashLoopBackOff": {"severity": "CRITICAL", "desc": "Container repeatedly crashing"},
    "ImagePullBackOff": {"severity": "HIGH", "desc": "Cannot pull container image"},
    "Evicted": {"severity": "HIGH", "desc": "Pod evicted — likely node pressure"},
    "Pending": {"severity": "MEDIUM", "desc": "Pod stuck in Pending state"},
    "Error": {"severity": "MEDIUM", "desc": "Generic error condition"},
    "Failed": {"severity": "MEDIUM", "desc": "Operation failed"},
    "Unhealthy": {"severity": "HIGH", "desc": "Health probe failing"},
    "BackOff": {"severity": "HIGH", "desc": "Back-off restarting container"},
    "connection refused": {"severity": "HIGH", "desc": "Service connectivity failure"},
    "timeout": {"severity": "MEDIUM", "desc": "Operation timed out"},
    "permission denied": {"severity": "HIGH", "desc": "RBAC or filesystem permission issue"},
    "certificate": {"severity": "HIGH", "desc": "TLS/certificate issue"},
    "OutOfMemory": {"severity": "CRITICAL", "desc": "Memory exhaustion"},
    "Liveness probe failed": {"severity": "HIGH", "desc": "Liveness probe failing — pod will restart"},
    "Readiness probe failed": {"severity": "MEDIUM", "desc": "Readiness probe failing — pod removed from service"},
}


def parse_logs(raw_logs: str) -> dict:
    lines = raw_logs.strip().split("\n")
    findings = []
    error_count = 0
    warning_count = 0

    for i, line in enumerate(lines):
        for pattern, meta in ERROR_PATTERNS.items():
            if pattern.lower() in line.lower():
                findings.append({
                    "line_number": i + 1,
                    "line": line.strip(),
                    "pattern": pattern,
                    "severity": meta["severity"],
                    "description": meta["desc"],
                })
                if meta["severity"] == "CRITICAL":
                    error_count += 1
                elif meta["severity"] == "HIGH":
                    error_count += 1
                else:
                    warning_count += 1
                break

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda x: severity_order.get(x["severity"], 99))

    overall = "HEALTHY"
    if error_count > 0:
        overall = "CRITICAL" if any(f["severity"] == "CRITICAL" for f in findings) else "DEGRADED"
    elif warning_count > 0:
        overall = "WARNING"

    return {
        "total_lines": len(lines),
        "error_count": error_count,
        "warning_count": warning_count,
        "overall_status": overall,
        "findings": findings[:20],
        "summary": f"Analyzed {len(lines)} log lines. Found {error_count} errors, {warning_count} warnings.",
    }