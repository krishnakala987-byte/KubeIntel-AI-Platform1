# KubeIntel AI Platform — Full Project Documentation

---

# Detailed Architecture

## Service Architecture

### kubeops-ui

* Streamlit frontend
* Port 8501
* Provides operator dashboard
* Includes:

  * Cluster Analysis
  * Incident Triage
  * Log Analyzer
  * Deployment Scorer
  * Security Audit
  * Runbook Generator

---

### kubeops-api

* Flask REST API
* Gunicorn with 4 workers
* Port 5000
* Handles:

  * AI inference
  * Log pattern analysis
  * Deployment scoring
  * Security auditing
  * Metrics export

---

### Groq AI Integration

Model:

```text
llama-3.3-70b-versatile
```

Used for:

* Cluster analysis
* Incident triage
* Deployment reviews
* Security auditing
* Runbook generation

---

# AWS Infrastructure

## AWS EKS

Cluster:

```text
kubeintel-cluster
```

Region:

```text
us-east-1
```

Node configuration:

```text
2x t3.medium EC2 instances
```

---

## AWS ECR

Stores:

* kubeops-api Docker image
* kubeops-ui Docker image

---

# Local Development

## Prerequisites

* Python 3.10+
* Docker
* AWS CLI v2
* kubectl
* eksctl

---

## Run Locally

```bash
docker-compose up --build
```

---

## Health Check

```bash
curl http://localhost:5000/health
```

---

# AWS EKS Deployment

## Configure AWS CLI

```bash
aws configure
```

---

## Create ECR Repositories

```bash
aws ecr create-repository \
  --repository-name kubeops-api \
  --region us-east-1

aws ecr create-repository \
  --repository-name kubeops-ui \
  --region us-east-1
```

---

## Create EKS Cluster

```bash
eksctl create cluster \
  --name kubeintel-cluster \
  --region us-east-1 \
  --nodegroup-name kubeintel-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --managed
```

---

## Update kubeconfig

```bash
aws eks update-kubeconfig \
  --name kubeintel-cluster \
  --region us-east-1
```

---

## Build Docker Images

```bash
docker build -t kubeops-api:latest services/kubeops-api

docker build -t kubeops-ui:latest services/kubeops-ui
```

---

## Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/namespaces/

kubectl apply -f kubernetes/deployments/

kubectl apply -f kubernetes/services/

kubectl apply -f kubernetes/hpa/

kubectl apply -f kubernetes/monitoring/
```

---

# CI/CD Pipeline

## Pipeline Stages

### Job 1 — Run Tests

* pytest
* Python 3.11
* Dependency validation

---

### Job 2 — Build and Push

* Docker image build
* AWS ECR push
* Git commit SHA tagging

---

### Job 3 — Deploy to EKS

* kubectl rollout
* Deployment update
* Rollout health verification

---

# Kubernetes Production Features

## Horizontal Pod Autoscaler

Scaling:

```text
Min Pods: 2
Max Pods: 10
```

Thresholds:

```text
CPU: 70%
Memory: 80%
```

---

## Liveness Probes

Automatically restart unhealthy containers.

---

## Readiness Probes

Prevent traffic routing until pods are healthy.

---

## Pod Anti-Affinity

Distributes pods across nodes for high availability.

---

## Rolling Updates

Ensures zero downtime deployments.

---

## Kubernetes Secrets

Groq API keys stored using Kubernetes Secrets.

---

# Observability Stack

## Prometheus

Scrapes:

* Flask metrics
* Kubernetes metrics
* Node Exporter metrics

---

## Node Exporter

Collects:

* CPU usage
* RAM usage
* Filesystem usage
* Network I/O

---

## Grafana

Visualizes:

* Cluster health
* CPU metrics
* Memory metrics
* Network metrics

Dashboard:

```text
Node Exporter Full Dashboard (ID: 1860)
```

---

# API Reference

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| GET    | /health                  | Health check       |
| GET    | /ready                   | Readiness check    |
| GET    | /metrics                 | Prometheus metrics |
| POST   | /api/v1/analyze          | Cluster analysis   |
| POST   | /api/v1/analyze/logs     | Log analysis       |
| POST   | /api/v1/incident/triage  | Incident triage    |
| POST   | /api/v1/incident/runbook | Runbook generation |
| POST   | /api/v1/deployment/score | Deployment scoring |
| POST   | /api/v1/security/audit   | Security audit     |

---

# Example API Calls

## Analyze Cluster State

```bash
curl -X POST http://EXTERNAL_IP:30081/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query":"Why are my pods crashing?","mode":"general"}'
```

---

## Analyze Logs

```bash
curl -X POST http://EXTERNAL_IP:30081/api/v1/analyze/logs \
  -H "Content-Type: application/json" \
  -d '{"logs":"ERROR CrashLoopBackOff detected"}'
```

---

# Operational Commands

## View Pods

```bash
kubectl get pods -n kubeintel
```

---

## View Logs

```bash
kubectl logs -n kubeintel -l app=kubeops-api -f
```

---

## Restart Deployment

```bash
kubectl rollout restart deployment/kubeops-api -n kubeintel
```

---

## Rollback Deployment

```bash
kubectl rollout undo deployment/kubeops-api -n kubeintel
```

---

## Scale Deployment

```bash
kubectl scale deployment kubeops-api --replicas=5 -n kubeintel
```

---

# Troubleshooting

## Container Crash Issues

Common causes:

* Dependency conflicts
* Missing Python packages
* Invalid environment variables

Fix:

```bash
docker build --no-cache -t kubeops-api:latest .
```

---

## GitHub Secret Scanning

If GitHub blocks a push:

* Regenerate exposed keys
* Remove secrets from git history
* Force push cleaned history

---

## Grafana Shows No Data

Verify:

* Prometheus targets are UP
* Node Exporter is running
* Correct Prometheus datasource configured

---

## Pods Stuck Pending

Check:

```bash
kubectl describe pod POD_NAME -n kubeintel
```

Common causes:

* Insufficient node resources
* Invalid image URI
* ECR authentication failures

---

# What I Learned

## Docker Dependency Management

Pinned:

```text
groq==0.13.0
httpx==0.28.1
```

to prevent compatibility issues.

---

## Kubernetes Secrets Management

Secrets should never be committed to source control.

Use:

```bash
kubectl create secret generic
```

instead of storing credentials in files.

---

## CI/CD Pipeline Design

Three-stage pipeline:

* Test
* Build
* Deploy

prevents broken code from reaching production.

---

## Kubernetes Observability

Prometheus targets page is the first place to debug missing Grafana metrics.

---

## Git History Rewriting

Used:

```bash
git filter-repo
```

to permanently remove exposed secrets from repository history.

---

# Resume Bullets

* Built AI-powered Kubernetes operations platform on AWS EKS using Groq LLaMA 3.3 70B
* Designed Flask + Streamlit microservices architecture
* Implemented GitHub Actions CI/CD pipeline with EKS deployment
* Configured Prometheus, Grafana, and Node Exporter monitoring stack
* Implemented Kubernetes HPA, rolling updates, and production security standards

