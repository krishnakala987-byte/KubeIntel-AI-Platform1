# KubeIntel AI Platform — Architecture

## Request Flow

```text
User Browser
    |
    v
kubeops-ui (Streamlit :8501)
    |
    | HTTP POST
    v
kubeops-api (Flask :5000)
    |
    |-- /api/v1/analyze ---------> Groq LLaMA 3.3 70B
    |
    |-- /api/v1/analyze/logs ---> log_analyzer + Groq
    |
    |-- /api/v1/incident -------> Incident AI Engine
    |
    |-- /api/v1/cluster --------> k8s_analyzer.py
    |
    v
Amazon EKS Cluster
    |
    |-- Kubernetes API
    |-- Deployments
    |-- Services
    |-- HPA
    |-- Monitoring
    |
    v
Prometheus + Grafana
```

---

## Components

### Frontend
- Streamlit dashboard
- Incident triage UI
- Cluster health visualization

### Backend
- Flask REST API
- Groq LLM integration
- Kubernetes analysis engine
- Log anomaly detection

### Infrastructure
- Docker containers
- AWS ECR
- Amazon EKS
- Kubernetes manifests
- Horizontal Pod Autoscaler

### Observability
- Prometheus metrics
- Grafana dashboards
- Kubernetes probes

---

## Deployment Flow

```text
Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions CI/CD
   |
   v
Docker Build
   |
   v
AWS ECR
   |
   v
Amazon EKS
```