# KubeIntel AI Platform

AI-powered Kubernetes operations platform built on AWS EKS using Groq LLaMA 3.3 70B for real-time cluster intelligence, incident triage, deployment health scoring, log anomaly detection, security auditing, and automated runbook generation.

---

# Overview

KubeIntel is a production-grade AI-powered DevOps intelligence platform designed to simplify Kubernetes operations.

Instead of manually debugging clusters, reading logs, and investigating incidents, operators can submit cluster state, logs, incidents, or Kubernetes manifests and instantly receive:

* Root cause analysis
* Incident triage
* Deployment health scoring
* Security recommendations
* AI-generated remediation guidance
* Automated operational runbooks

The platform is built using a microservices architecture with:

* Flask REST API
* Streamlit dashboard
* AWS EKS
* Docker
* GitHub Actions CI/CD
* Prometheus
* Grafana
* Kubernetes Horizontal Pod Autoscaler

---

# Architecture Overview

```text
Developer / SRE
       |
       v
+----------------------+
|  Streamlit Frontend  |
|      kubeops-ui      |
+----------------------+
       |
       v
+----------------------+
|     Flask API        |
|     kubeops-api      |
+----------------------+
       |
       v
+----------------------+
|  Groq LLaMA 3.3 70B |
+----------------------+

Infrastructure:
----------------
GitHub Actions CI/CD
        |
        v
AWS EKS Cluster
        |
        |-- kubeops-api
        |-- kubeops-ui
        |-- Prometheus
        |-- Grafana
        |-- Node Exporter
        |
        v
AWS ECR
```

---

# Features

## Cluster State Analysis

* Detects Kubernetes failures
* Diagnoses CrashLoopBackOff and OOMKilled issues
* Suggests kubectl remediation commands
* Provides root cause analysis

---

## Incident Triage

* AI-assisted production incident analysis
* Severity classification
* Prioritized remediation workflow
* Step-by-step investigation guidance

---

## Log Anomaly Detection

Detects:

* CrashLoopBackOff
* OOMKilled
* ImagePullBackOff
* Liveness probe failures
* Readiness probe failures
* Certificate issues
* Permission denied
* BackOff failures

---

## Deployment Health Scoring

Scores Kubernetes deployments based on:

* Resource limits
* Health probes
* Security context
* Replica strategy
* Image policies

---

## Security Audit

Audits manifests for:

* Privileged containers
* Missing RBAC
* Hardcoded secrets
* Missing resource limits
* Pod Security Standards violations

---

## Runbook Generator

Automatically generates:

* Incident runbooks
* Resolution workflows
* Investigation commands
* Prevention recommendations

---

# Tech Stack

| Category         | Technology         |
| ---------------- | ------------------ |
| Backend          | Flask + Gunicorn   |
| Frontend         | Streamlit          |
| AI Model         | Groq LLaMA 3.3 70B |
| Kubernetes       | AWS EKS            |
| Registry         | AWS ECR            |
| CI/CD            | GitHub Actions     |
| Monitoring       | Prometheus         |
| Visualization    | Grafana            |
| Containerization | Docker             |
| Language         | Python 3.11        |

---

# Project Structure

```text
KubeIntel-AI-Platform/
│
├── .github/
├── docs/
├── kubernetes/
├── monitoring/
├── services/
├── tests/
├── docker-compose.yml
├── Makefile
└── README.md
```

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/krishnakala987-byte/KubeIntel-AI-Platform1.git

cd KubeIntel-AI-Platform1
```

---

## Configure Environment

```bash
cp .env.example .env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
AWS_ACCOUNT_ID=your_aws_account_id
```

---

## Run Locally

```bash
docker-compose up --build
```

Access:

```text
UI  : http://localhost:8501
API : http://localhost:5000
```

---

# AWS EKS Deployment

```bash
eksctl create cluster \
  --name kubeintel-cluster \
  --region us-east-1 \
  --nodegroup-name kubeintel-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --managed
```

Deploy:

```bash
kubectl apply -f kubernetes/
```

---

# CI/CD Pipeline

The GitHub Actions pipeline automatically:

1. Runs pytest unit tests
2. Builds Docker images
3. Pushes images to AWS ECR
4. Deploys to AWS EKS
5. Verifies rollout health

---

# Kubernetes Production Features

* Horizontal Pod Autoscaler
* Liveness probes
* Readiness probes
* Rolling updates
* Pod anti-affinity
* Kubernetes Secrets
* Non-root containers

---

# Observability Stack

## Prometheus

Collects:

* Flask metrics
* Kubernetes metrics
* Node metrics

---

## Grafana

Visualizes:

* CPU usage
* Memory usage
* Cluster health
* Pod metrics

---

# API Endpoints

| Method | Endpoint                 |
| ------ | ------------------------ |
| GET    | /health                  |
| GET    | /ready                   |
| GET    | /metrics                 |
| POST   | /api/v1/analyze          |
| POST   | /api/v1/analyze/logs     |
| POST   | /api/v1/incident/triage  |
| POST   | /api/v1/incident/runbook |
| POST   | /api/v1/deployment/score |
| POST   | /api/v1/security/audit   |

---

# Full Documentation

Complete architecture, deployment, observability, troubleshooting, API reference, operational commands, and production workflows are available in:

```text
docs/PROJECT_DOCUMENTATION.md
```

---

# Resume Highlights

* Built AI-powered Kubernetes operations platform on AWS EKS using Groq LLaMA 3.3 70B
* Implemented Flask microservices architecture with Streamlit frontend
* Designed GitHub Actions CI/CD pipeline with automated EKS deployment
* Configured Prometheus, Grafana, and Kubernetes observability stack
* Implemented Kubernetes HPA, rolling deployments, and production security practices

---

# Author

Krishna Kala

GitHub:
https://github.com/krishnakala987-byte/KubeIntel-AI-Platform1

