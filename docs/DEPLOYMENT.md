
# KubeIntel AI Platform — Deployment Guide

## Prerequisites
- AWS CLI configured
- kubectl installed
- eksctl installed
- Docker running

## Local Development
```bash
docker-compose up --build
```
Open http://localhost:8501

## AWS EKS Deployment

### 1. Create EKS Cluster
```bash
eksctl create cluster --name kubeintel-cluster --region us-east-1 --nodegroup-name kubeintel-nodes --node-type t3.medium --nodes 2 --managed
```

### 2. Create Namespace and Secret
```bash
kubectl apply -f kubernetes/namespaces/kubeintel-namespace.yaml
kubectl create secret generic groq-secret --from-literal=api_key="YOUR_KEY" -n kubeintel
```

### 3. Deploy Services
```bash
kubectl apply -f kubernetes/deployments/
kubectl apply -f kubernetes/services/
kubectl apply -f kubernetes/hpa/
```

### 4. Access Platform
```bash
kubectl get nodes -o wide  # get EXTERNAL-IP
# UI: http://EXTERNAL-IP:30082
# API: http://EXTERNAL-IP:30081
```
EOF

cat > docs/RUNBOOK.md << 'EOF'
# KubeIntel Platform — Operations Runbook

## Health Checks
```bash
kubectl get pods -n kubeintel
kubectl get hpa -n kubeintel
kubectl top pods -n kubeintel
```

## Restart a Service
```bash
kubectl rollout restart deployment/kubeops-api -n kubeintel
kubectl rollout status deployment/kubeops-api -n kubeintel
```

## View Live Logs
```bash
kubectl logs -n kubeintel -l app=kubeops-api -f
```

## Scale Manually
```bash
kubectl scale deployment kubeops-api --replicas=4 -n kubeintel
```

## Rollback a Bad Deployment
```bash
kubectl rollout undo deployment/kubeops-api -n kubeintel
```
EOF

cat > docs/ARCHITECTURE.md << 'EOF'
# KubeIntel AI Platform — Architecture

## Overview
Two-service microservices architecture deployed on AWS EKS.

## Services
- **kubeops-api** (Flask, port 5000) — AI engine, REST API, Prometheus metrics
- **kubeops-ui** (Streamlit, port 8501) — Operator dashboard

## AI Features
1. Cluster State Analysis
2. Incident Triage
3. Log Anomaly Detection
4. Deployment Health Scoring
5. Security Audit
6. Runbook Generation

## Infrastructure
- AWS EKS — managed Kubernetes
- AWS ECR — private container registry
- HPA — auto-scales API pods 2-10 replicas
- GitHub Actions — CI/CD pipeline

## AI Stack
- Groq API — LLaMA 3.3 70B inference
- Custom prompt engineering for DevOps context
