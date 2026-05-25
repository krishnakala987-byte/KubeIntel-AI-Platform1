````markdown
# KubeIntel AI Platform

> AI-powered Kubernetes operations platform — real-time cluster intelligence, log anomaly detection, incident triage, deployment health scoring, and auto-generated runbooks on AWS EKS using Groq LLaMA 3.3 70B.

---

## Table of Contents

- [What This Project Does](#what-this-project-does)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [How to Run Locally](#how-to-run-locally)
- [How to Deploy to AWS EKS](#how-to-deploy-to-aws-eks)
- [CI/CD Pipeline](#cicd-pipeline)
- [Kubernetes Production Features](#kubernetes-production-features)
- [Observability Stack](#observability-stack)
- [API Endpoints](#api-endpoints)
- [Key Commands Reference](#key-commands-reference)
- [Troubleshooting](#troubleshooting)
- [What I Learned](#what-i-learned)
- [Resume Bullets](#resume-bullets)

---

## What This Project Does

KubeIntel is a production-grade AI-powered DevOps intelligence platform that acts like a senior SRE available 24/7. Instead of manually reading kubectl output and digging through thousands of lines of logs, you paste your cluster state or logs into KubeIntel and the AI instantly gives you:

- Root cause diagnosis of what is broken and why
- Exact kubectl commands to fix the issue
- Deployment health scores with specific improvements
- Security misconfigurations in your YAML manifests
- Auto-generated production runbooks you can download

The platform is built with two microservices — a Flask REST API that contains all the AI logic, and a Streamlit dashboard that operators use. Both run on AWS EKS with horizontal pod autoscaling, zero-downtime deployments, and a full Prometheus + Grafana observability stack.

---

## Architecture

````
Developer / SRE opens browser
           |
           v
   kubeops-ui (Streamlit)
   Port 8501 — what the user sees
   6 tabs: Cluster Analysis, Incident Triage,
   Log Analyzer, Deployment Scorer,
   Security Audit, Runbook Generator
           |
           | HTTP POST requests
           v
   kubeops-api (Flask + Gunicorn)
   Port 5000 — the AI brain
           |
           |-- POST /api/v1/analyze         --> Groq LLaMA 3.3 70B
           |-- POST /api/v1/analyze/logs    --> Pattern detection + Groq
           |-- POST /api/v1/incident/triage --> Incident AI triage
           |-- POST /api/v1/incident/runbook --> Runbook generation
           |-- POST /api/v1/deployment/score --> YAML health scoring
           |-- POST /api/v1/security/audit  --> Security posture check
           |-- GET  /metrics               --> Prometheus scraping
           |-- GET  /health                --> Liveness probe
           |-- GET  /ready                 --> Readiness probe
           |
           v
   Groq API (external)
   Model: llama-3.3-70b-versatile
   Fastest LLM inference available

AWS Infrastructure:
   GitHub push to main
           |
           v
   GitHub Actions CI/CD Pipeline
           |
           |-- Job 1: Run Tests (pytest) ........... 11 seconds
           |-- Job 2: Build and Push to ECR ........ 1 minute 6 seconds
           |-- Job 3: Deploy to EKS ................ 52 seconds
           |
           v
   AWS EKS Cluster (kubeintel-cluster)
   Region: us-east-1
   Nodes: 2x t3.medium EC2 instances
           |
           |-- Namespace: kubeintel
           |-- kubeops-api   Deployment (2-10 pods, HPA)
           |-- kubeops-ui    Deployment (2 pods)
           |-- prometheus    Deployment (1 pod)
           |-- grafana       Deployment (1 pod)
           |-- node-exporter DaemonSet (1 pod per node)
           |
           v
   AWS ECR (private Docker image registry)
   Stores: kubeops-api:latest
   Stores: kubeops-ui:latest
````

---

## Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| AI Model | Groq LLaMA 3.3 70B | LLM inference for all AI features |
| Backend | Python Flask 3.0 + Gunicorn | REST API with 4 workers |
| Frontend | Streamlit | Operator dashboard |
| Containerisation | Docker | Package each service |
| Registry | AWS ECR | Private Docker image storage |
| Kubernetes | AWS EKS | Managed Kubernetes cluster |
| Auto-scaling | Kubernetes HPA | Scale API pods 2 to 10 |
| CI/CD | GitHub Actions | Automated test, build, deploy |
| Metrics | Prometheus | Scrape Flask and node metrics |
| Visualisation | Grafana | Live cluster dashboards |
| Node Metrics | Node Exporter | CPU, memory, disk per node |
| Language | Python 3.11 | All application code |

---

## Features

### Feature 1 — Cluster State Analysis

What it does: You paste the output of kubectl get pods, kubectl get events, or kubectl describe pod into the text box. The AI reads it and tells you exactly what is wrong, why it happened, and gives you the exact kubectl commands to fix it.

Example input:
````
production    payment-service-7d9f8b-xkp2q    0/1    CrashLoopBackOff    14    23m
production    auth-service-6c8d9f-mnb4r        0/1    OOMKilled            3    45m
````

Example output from AI: Diagnosis of CrashLoopBackOff cause, memory limit recommendations, exact kubectl commands to increase resource limits and restart deployments.

### Feature 2 — Incident Triage

What it does: You describe a production incident in plain English. The AI acts as an on-call SRE and gives you a prioritised action plan with severity level and step-by-step resolution.

Example input:
````
API latency spiked to 8000ms. payment-service in CrashLoopBackOff with 14 restarts.
50% error rate on /checkout. Customers cannot complete purchases.
````

### Feature 3 — Log Anomaly Detection

What it does: You paste raw pod logs. The platform first runs pattern matching against 15 known Kubernetes failure signatures including CrashLoopBackOff, OOMKilled, ImagePullBackOff, Liveness probe failed, Readiness probe failed, BackOff, connection refused, permission denied, and certificate errors. It shows you which lines triggered which patterns with severity levels (CRITICAL, HIGH, MEDIUM), then feeds the full analysis to the AI for root cause explanation.

### Feature 4 — Deployment Health Scoring

What it does: You paste a Kubernetes Deployment YAML. The AI scores it from 0 to 100 across five categories and tells you exactly what to fix.

Scoring categories:
- Resource limits (are CPU and memory requests and limits defined)
- Health probes (are liveness and readiness probes configured)
- Security context (is runAsNonRoot set, is allowPrivilegeEscalation false)
- Replica strategy (is replica count greater than 1, is rolling update configured)
- Image policy (is imagePullPolicy set to Always, is a specific tag used instead of latest)

### Feature 5 — Security Audit

What it does: You paste any Kubernetes manifests. The AI checks for security misconfigurations including missing RBAC roles, privileged containers, hostNetwork usage, secrets hardcoded in environment variables, missing NetworkPolicies, missing resource limits, and Pod Security Standards compliance issues.

### Feature 6 — Runbook Generator

What it does: You describe any Kubernetes incident. The AI generates a complete production runbook in markdown format that you can download. The runbook includes incident summary, severity level (P1/P2/P3), immediate actions for the first 5 minutes, investigation steps with exact kubectl commands, resolution steps, post-incident tasks, and prevention measures.

---

## Project Structure

````
KubeIntel-AI-Platform/
│
├── .github/
│   └── workflows/
│       └── deploy.yml                    # GitHub Actions pipeline
│                                         # Runs on every push to main
│                                         # 3 jobs: test, build, deploy
│
├── architecture/
│   └── kubeintel-architecture.md         # Architecture documentation
│
├── docs/
│   ├── DEPLOYMENT.md                     # Step by step deployment guide
│   └── RUNBOOK.md                        # Operations runbook
│
├── kubernetes/
│   ├── namespaces/
│   │   └── kubeintel-namespace.yaml      # Creates kubeintel namespace
│   │
│   ├── deployments/
│   │   ├── kubeops-api-deployment.yaml   # Flask API deployment
│   │   │                                 # 2 replicas, HPA enabled
│   │   │                                 # liveness + readiness probes
│   │   │                                 # non-root security context
│   │   │                                 # pod anti-affinity
│   │   └── kubeops-ui-deployment.yaml    # Streamlit UI deployment
│   │
│   ├── services/
│   │   ├── kubeops-api-service.yaml      # NodePort 30081
│   │   └── kubeops-ui-service.yaml       # NodePort 30082
│   │
│   ├── secrets/
│   │   └── groq-secret.yaml             # Template only — NEVER commit real keys
│   │                                    # Real secret created with kubectl create secret
│   │
│   ├── hpa/
│   │   └── kubeops-hpa.yaml             # Scales API 2 to 10 pods
│   │                                    # CPU threshold: 70%
│   │                                    # Memory threshold: 80%
│   │
│   ├── ingress/
│   │   └── kubeintel-ingress.yaml        # Nginx ingress configuration
│   │
│   └── monitoring/
│       ├── prometheus-configmap.yaml     # Prometheus scrape config
│       ├── prometheus-deployment.yaml    # Prometheus pod + NodePort 30090
│       ├── grafana-deployment.yaml       # Grafana pod + NodePort 30083
│       └── node-exporter.yaml           # DaemonSet on every node
│
├── monitoring/
│   ├── prometheus.yml                    # Prometheus config for local dev
│   └── grafana/
│       └── dashboards/
│           └── kubeintel-dashboard.json  # Custom Grafana dashboard
│
├── services/
│   ├── kubeops-api/
│   │   ├── app.py                        # Flask app — all 9 API endpoints
│   │   ├── ai_engine.py                  # Groq client — prompt engineering
│   │   │                                 # 3 functions: analyze, runbook, score
│   │   ├── log_analyzer.py               # Pattern matching — 15 failure patterns
│   │   │                                 # Returns severity, line number, description
│   │   ├── Dockerfile                    # Multi-stage, non-root user, healthcheck
│   │   └── requirements.txt              # flask, groq==0.13.0, httpx==0.28.1
│   │                                     # prometheus-flask-exporter, gunicorn
│   └── kubeops-ui/
│       ├── app.py                        # Streamlit — 6 tabs, quick prompts
│       ├── Dockerfile                    # Non-root, healthcheck
│       └── requirements.txt             # streamlit, requests
│
├── tests/
│   ├── __init__.py
│   └── test_api.py                       # 6 pytest unit tests
│                                         # tests log_analyzer and Flask endpoints
│
├── .env.example                          # Shows required variables, no real values
├── .gitignore                            # Excludes .env, __pycache__, etc
├── docker-compose.yml                    # Local dev — both services + networking
├── Makefile                              # make dev, make build, make deploy
└── README.md
````

---

## How to Run Locally

### Prerequisites

Install these tools before starting:

```bash
# Check Python (need 3.10 or higher)
python3 --version

# Check Docker (must be running)
docker --version

# Check AWS CLI (need v2)
aws --version

# Check kubectl
kubectl version --client

# Check eksctl
eksctl version
```

Install anything missing:
- AWS CLI v2: https://aws.amazon.com/cli/
- kubectl: https://kubernetes.io/docs/tasks/tools/
- eksctl: https://eksctl.io/installation/
- Docker Desktop: https://www.docker.com/products/docker-desktop/

### Get a Groq API Key

1. Go to console.groq.com
2. Sign up or log in
3. Click API Keys in the left sidebar
4. Click Create API Key
5. Copy the key immediately — it is shown only once

### Clone and Configure

```bash
git clone https://github.com/krishnakala987-byte/KubeIntel-AI-Platform1.git
cd KubeIntel-AI-Platform1

# Create your local environment file
cp .env.example .env

# Open .env and add your real values
# GROQ_API_KEY=gsk_your_actual_key_here
# AWS_ACCOUNT_ID=your_12_digit_account_id
```

### Run with Docker Compose

```bash
# Build and start both services
docker-compose up --build

# You will see both containers start
# Access UI at:  http://localhost:8501
# Access API at: http://localhost:5000

# Test the API is healthy
curl http://localhost:5000/health
# Expected: {"service":"kubeops-api","status":"healthy","version":"2.0.0"}

# Stop when done
docker-compose down
```

### Run Tests

```bash
pip install pytest flask flask-cors prometheus-flask-exporter groq==0.13.0 httpx==0.28.1
pytest tests/ -v
```

---

## How to Deploy to AWS EKS

### Step 1 — Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json

# Verify it worked
aws sts get-caller-identity
# Shows your account ID, user ARN, and account number
```

### Step 2 — Create ECR Repositories

ECR is AWS's private Docker registry. You need one repository per service.

```bash
# Create repository for the Flask API
aws ecr create-repository \
  --repository-name kubeops-api \
  --region us-east-1

# Create repository for the Streamlit UI
aws ecr create-repository \
  --repository-name kubeops-ui \
  --region us-east-1

# Get your account ID (you will need this)
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo $ACCOUNT_ID

# See your repository URIs
aws ecr describe-repositories \
  --query 'repositories[*].repositoryUri' \
  --output table
```

### Step 3 — Create EKS Cluster

This command creates the full cluster including VPC, subnets, IAM roles, and EC2 nodes. Takes 15-20 minutes.

```bash
eksctl create cluster \
  --name kubeintel-cluster \
  --region us-east-1 \
  --nodegroup-name kubeintel-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 4 \
  --managed

# After creation, configure kubectl to talk to your cluster
aws eks update-kubeconfig \
  --name kubeintel-cluster \
  --region us-east-1

# Verify kubectl is connected
kubectl cluster-info
kubectl get nodes
# You should see 2 nodes with STATUS = Ready
```

### Step 4 — Build and Push Docker Images

```bash
# Authenticate Docker with ECR (do this once per terminal session)
aws ecr get-login-password --region us-east-1 | \
  docker login \
  --username AWS \
  --password-stdin \
  $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

export ECR="$ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com"

# Build API image
cd services/kubeops-api
docker build -t kubeops-api:latest .

# Build UI image
cd ../kubeops-ui
docker build -t kubeops-ui:latest .
cd ../..

# Tag images with ECR URI
docker tag kubeops-api:latest $ECR/kubeops-api:v1.0
docker tag kubeops-ui:latest $ECR/kubeops-ui:v1.0

# Push images to ECR
docker push $ECR/kubeops-api:v1.0
docker push $ECR/kubeops-ui:v1.0

# Verify images are in ECR
aws ecr list-images --repository-name kubeops-api
aws ecr list-images --repository-name kubeops-ui
```

### Step 5 — Update Deployment YAMLs

Open kubernetes/deployments/kubeops-api-deployment.yaml and find this line:

````
image: YOUR_ECR_URI/kubeops-api:latest
````

Replace with your actual ECR URI:

````
image: 123456789.dkr.ecr.us-east-1.amazonaws.com/kubeops-api:v1.0
````

Do the same in kubeops-ui-deployment.yaml.

### Step 6 — Deploy to Kubernetes

Always deploy in this order: namespace first, then secrets, then deployments, then services, then HPA.

```bash
# Create the namespace
kubectl apply -f kubernetes/namespaces/kubeintel-namespace.yaml

# Verify namespace exists
kubectl get namespaces | grep kubeintel

# Create the Groq API key secret
# Replace YOUR_GROQ_KEY with your actual key
kubectl create secret generic groq-secret \
  --from-literal=api_key="YOUR_GROQ_KEY" \
  -n kubeintel

# Verify secret was created (values are hidden)
kubectl get secrets -n kubeintel

# Deploy the applications
kubectl apply -f kubernetes/deployments/kubeops-api-deployment.yaml
kubectl apply -f kubernetes/deployments/kubeops-ui-deployment.yaml

# Deploy the services (expose pods via NodePort)
kubectl apply -f kubernetes/services/kubeops-api-service.yaml
kubectl apply -f kubernetes/services/kubeops-ui-service.yaml

# Deploy HPA (autoscaling)
kubectl apply -f kubernetes/hpa/kubeops-hpa.yaml

# Deploy monitoring stack
kubectl apply -f kubernetes/monitoring/prometheus-configmap.yaml
kubectl apply -f kubernetes/monitoring/prometheus-deployment.yaml
kubectl apply -f kubernetes/monitoring/grafana-deployment.yaml
kubectl apply -f kubernetes/monitoring/node-exporter.yaml
```

### Step 7 — Watch Pods Come Up

```bash
# Watch pods start (takes 60-90 seconds)
kubectl get pods -n kubeintel -w

# You will see:
# Pending → ContainerCreating → Running
# Press Ctrl+C when all pods show Running

# Expected output:
# kubeops-api-xxxxx   1/1   Running   0   2m
# kubeops-api-xxxxx   1/1   Running   0   2m
# kubeops-ui-xxxxx    1/1   Running   0   2m
# kubeops-ui-xxxxx    1/1   Running   0   2m
# prometheus-xxxxx    1/1   Running   0   1m
# grafana-xxxxx       1/1   Running   0   1m
# node-exporter-xxxx  1/1   Running   0   1m
```

### Step 8 — Access Your Platform

```bash
# Get the external IP of your nodes
kubectl get nodes -o wide
# Look at the EXTERNAL-IP column

# Your platform is now live at:
# KubeIntel UI:    http://EXTERNAL_IP:30082
# API Health:      http://EXTERNAL_IP:30081/health
# Prometheus:      http://EXTERNAL_IP:30090
# Grafana:         http://EXTERNAL_IP:30083  (login: admin / kubeintel123)

# Test the API
curl http://EXTERNAL_IP:30081/health
# Expected: {"service":"kubeops-api","status":"healthy","version":"2.0.0"}
```

---

## CI/CD Pipeline

The GitHub Actions pipeline in .github/workflows/deploy.yml runs automatically on every push to main.

### Pipeline Flow

````
git push origin main
       |
       v
Job 1: Run Tests (11 seconds)
       |-- actions/checkout@v4
       |-- actions/setup-python@v5 (Python 3.11)
       |-- pip install all dependencies including groq==0.13.0 httpx==0.28.1
       |-- pytest tests/ -v
       |-- 6 tests must pass before proceeding
       |
       v (only if tests pass)
Job 2: Build and Push to ECR (1 minute 6 seconds)
       |-- Configure AWS credentials from GitHub Secrets
       |-- docker build kubeops-api image
       |-- docker push to ECR with git commit SHA as tag
       |-- docker build kubeops-ui image
       |-- docker push to ECR
       |
       v (only if build succeeds)
Job 3: Deploy to EKS (52 seconds)
       |-- aws eks update-kubeconfig
       |-- kubectl set image (updates deployment to new image tag)
       |-- kubectl rollout status (waits until all pods are healthy)
       |-- If rollout fails, deployment stops and old version keeps running
````

### Setting Up CI/CD

Add these secrets to your GitHub repository under Settings → Secrets and variables → Actions:

````
AWS_ACCESS_KEY_ID      your IAM user access key
AWS_SECRET_ACCESS_KEY  your IAM user secret key
AWS_ACCOUNT_ID         your 12-digit AWS account ID
````

---

## Kubernetes Production Features

### Horizontal Pod Autoscaler

The HPA watches CPU and memory usage of the kubeops-api pods. When CPU goes above 70% or memory above 80%, it adds more pods automatically. Maximum 10 pods, minimum 2 pods.

```bash
# Check HPA status
kubectl get hpa -n kubeintel

# Example output:
# NAME             REFERENCE              TARGETS                    MINPODS   MAXPODS   REPLICAS
# kubeops-api-hpa  Deployment/kubeops-api cpu: 0%/70%, mem: 59%/80%  2         10        3
```

### Liveness and Readiness Probes

Liveness probe: Kubernetes sends GET /health every 20 seconds. If it fails 3 times in a row, the pod is restarted automatically.

Readiness probe: Kubernetes sends GET /ready every 10 seconds. Until this passes, the pod does not receive any traffic. This prevents broken pods from serving requests.

### Pod Anti-Affinity

The deployment is configured so that no two kubeops-api pods can be scheduled on the same node. This means if one EC2 node goes down, at least one API pod survives on the other node.

### Security Context

```yaml
securityContext:
  runAsNonRoot: true       # never runs as root
  runAsUser: 1001          # runs as specific non-root user
  allowPrivilegeEscalation: false  # cannot gain more permissions
```

### Zero-Downtime Rolling Updates

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1          # adds 1 new pod before removing old ones
    maxUnavailable: 0    # never reduces below desired replica count
```

This means during a deployment update, new pods start before old ones stop. Users experience zero downtime.

### Kubernetes Secrets

The Groq API key is never in source code. It lives only in a Kubernetes Secret:

```bash
kubectl create secret generic groq-secret \
  --from-literal=api_key="YOUR_KEY" \
  -n kubeintel
```

The deployment references it as an environment variable:

```yaml
env:
  - name: GROQ_API_KEY
    valueFrom:
      secretKeyRef:
        name: groq-secret
        key: api_key
```

---

## Observability Stack

### Prometheus

Prometheus scrapes metrics from two targets every 15 seconds:

1. kubeops-api at http://kubeops-api-service:5000/metrics — Flask request counts, response times, error rates
2. node-exporter at the node IP port 9100 — CPU, memory, disk, network per EC2 node

Check targets are UP:
```bash
# Open in browser
http://EXTERNAL_IP:30090/targets
# Both should show green UP status
```

### Node Exporter

A DaemonSet runs one node-exporter pod on every EC2 node in the cluster. It exposes hardware-level metrics including CPU busy percentage, RAM usage, SWAP usage, filesystem usage, system load, and network I/O.

### Grafana

Access Grafana at http://EXTERNAL_IP:30083 with username admin and password kubeintel123.

Import the Node Exporter Full dashboard:
1. Click + in top right
2. Click Import dashboard
3. Enter dashboard ID 1860
4. Click Load
5. Select prometheus as the data source
6. Click Import
7. Select node-exporter from the Job dropdown
8. Select your node from the Instance dropdown

You will see live CPU busy percentage, RAM usage, system load, filesystem usage, and network graphs.

---

## API Endpoints

| Method | Endpoint | Request Body | Response |
|---|---|---|---|
| GET | /health | none | status, service name, version |
| GET | /ready | none | ready status, error if key missing |
| GET | /metrics | none | Prometheus format metrics |
| POST | /api/v1/analyze | context, query, mode | AI analysis text |
| POST | /api/v1/analyze/logs | logs | parsed findings + AI diagnosis |
| POST | /api/v1/incident/triage | symptoms, cluster_state, namespace | triage report |
| POST | /api/v1/incident/runbook | incident | full runbook markdown |
| POST | /api/v1/deployment/score | yaml_content | score 0-100 + grades + issues |
| POST | /api/v1/deployment/review | yaml_content | full review text |
| POST | /api/v1/security/audit | manifests | audit report |

### Example API Calls

```bash
# Health check
curl http://EXTERNAL_IP:30081/health

# Analyze cluster state
curl -X POST http://EXTERNAL_IP:30081/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query":"Why are my pods in CrashLoopBackOff?","mode":"general"}'

# Analyze logs
curl -X POST http://EXTERNAL_IP:30081/api/v1/analyze/logs \
  -H "Content-Type: application/json" \
  -d '{"logs":"ERROR CrashLoopBackOff detected\nERROR OOMKilled: memory limit exceeded"}'

# Generate runbook
curl -X POST http://EXTERNAL_IP:30081/api/v1/incident/runbook \
  -H "Content-Type: application/json" \
  -d '{"incident":"payment-service CrashLoopBackOff with OOMKilled, 14 restarts"}'

# Score a deployment
curl -X POST http://EXTERNAL_IP:30081/api/v1/deployment/score \
  -H "Content-Type: application/json" \
  -d '{"yaml_content":"apiVersion: apps/v1\nkind: Deployment..."}'
```

---

## Key Commands Reference

```bash
# See all pods and their status
kubectl get pods -n kubeintel

# See pods with node assignment
kubectl get pods -n kubeintel -o wide

# See HPA scaling status
kubectl get hpa -n kubeintel

# See all services and ports
kubectl get svc -n kubeintel

# See resource usage per pod
kubectl top pods -n kubeintel

# Follow live logs from all API pods
kubectl logs -n kubeintel -l app=kubeops-api -f

# See recent events (great for debugging)
kubectl get events -n kubeintel --sort-by='.lastTimestamp'

# Describe a pod for detailed info including events
kubectl describe pod POD_NAME -n kubeintel

# Shell into a running pod
kubectl exec -it POD_NAME -n kubeintel -- /bin/sh

# Restart a deployment (picks up new secret values)
kubectl rollout restart deployment/kubeops-api -n kubeintel

# Check rollout progress
kubectl rollout status deployment/kubeops-api -n kubeintel

# Rollback to previous version
kubectl rollout undo deployment/kubeops-api -n kubeintel

# Scale manually
kubectl scale deployment kubeops-api --replicas=5 -n kubeintel

# Update secret with new API key
kubectl delete secret groq-secret -n kubeintel
kubectl create secret generic groq-secret \
  --from-literal=api_key="YOUR_NEW_KEY" \
  -n kubeintel
kubectl rollout restart deployment/kubeops-api -n kubeintel

# Delete cluster when not using it (saves AWS costs)
eksctl delete cluster --name kubeintel-cluster --region us-east-1

# Recreate cluster when needed
eksctl create cluster --name kubeintel-cluster --region us-east-1 \
  --nodegroup-name kubeintel-nodes --node-type t3.medium --nodes 2 --managed
```

---

## Troubleshooting

### Container crashes immediately after docker run

```bash
# Step 1: Check if container is running or crashed
docker ps -a | grep kubeops-api-test

# Step 2: Read the crash logs
docker logs kubeops-api-test

# Common error 1: TypeError proxies argument
# Cause: groq and httpx version conflict
# Fix: update requirements.txt to use groq==0.13.0 and httpx==0.28.1
# then rebuild: docker build --no-cache -t kubeops-api:latest .

# Common error 2: ModuleNotFoundError
# Cause: Docker used cached layer without new package
# Fix: docker build --no-cache -t kubeops-api:latest .

# Common error 3: connection refused on curl
# Cause: container crashed before Flask could start
# Always read docker logs before assuming port issue
```

### GitHub push rejected with secret scanning error

```bash
# Error: GH013: Repository rule violations found
# Cause: real API key was committed to a file

# Step 1: Regenerate your Groq API key at console.groq.com immediately
# Step 2: Remove the secret from git history
pip install git-filter-repo --break-system-packages
git filter-repo --path .env.example --invert-paths --force

# Step 3: Re-add remote (filter-repo removes it)
git remote add origin https://github.com/USERNAME/REPO.git

# Step 4: Fix the file with placeholder only
echo "GROQ_API_KEY=your_groq_api_key_here" > .env.example

# Step 5: Force push clean history
git add .env.example
git commit -m "fix: remove exposed secret"
git push origin main --force

# Golden rule: .env.example contains ONLY placeholder text
# Real keys live in .env (gitignored) and Kubernetes Secrets
```

### Grafana shows N/A or No data

```bash
# Cause 1: Prometheus data source URL is wrong
# Fix: go to Connections → Data sources → prometheus
# Set URL to the Prometheus cluster IP not localhost
kubectl get svc -n kubeintel | grep prometheus
# Use the CLUSTER-IP shown, format: http://CLUSTER_IP:9090

# Cause 2: Node exporter not running
kubectl get pods -n kubeintel | grep node-exporter
kubectl get daemonset -n kubeintel

# Cause 3: Prometheus not scraping node-exporter
# Open http://EXTERNAL_IP:30090/targets
# Both kubeops-api and node-exporter should show UP green

# Cause 4: Dashboard needs Job and Instance selected
# In Grafana dashboard, click Job dropdown → select node-exporter
# Click Instance dropdown → select your node
```

### Pods stuck in Pending state

```bash
kubectl describe pod POD_NAME -n kubeintel
# Look at Events section at the bottom

# Common cause: not enough CPU/memory on nodes
# Fix: check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Common cause: image pull error
kubectl describe pod POD_NAME -n kubeintel | grep -A 10 Events
# If ImagePullBackOff: check ECR URI in deployment YAML is correct
# Check ECR authentication: aws ecr get-login-password | docker login
```

### API returns 500 Internal Server Error

```bash
# Cause: Groq API key is wrong or expired
# Check what key is in the secret
kubectl get secret groq-secret -n kubeintel -o jsonpath='{.data.api_key}' | base64 -d

# If wrong, update it
kubectl delete secret groq-secret -n kubeintel
kubectl create secret generic groq-secret \
  --from-literal=api_key="YOUR_NEW_KEY" \
  -n kubeintel
kubectl rollout restart deployment/kubeops-api -n kubeintel
kubectl rollout status deployment/kubeops-api -n kubeintel
```

### GitHub Actions test job fails with exit code 4

```bash
# Cause: pytest found no test files
# Error: ERROR: file or directory not found: tests/

# Check if test file exists and is committed
git ls-files tests/
# Must show tests/__init__.py and tests/test_api.py

# If missing, create and commit
touch tests/__init__.py
# Create tests/test_api.py with your test functions
git add tests/
git commit -m "test: add test files"
git push origin main
```

---

## What I Learned

**Docker and dependency management**
Version conflicts between Python packages are one of the most common real-world problems. The groq==0.9.0 library passed a proxies argument to httpx that newer httpx versions removed. The fix was pinning compatible versions: groq==0.13.0 and httpx==0.28.1. Always pin exact versions in requirements.txt for production. Never use latest.

**Kubernetes secrets management**
Secrets must never appear in source code or committed files. GitHub's secret scanning will block your push and your key will be compromised. The correct pattern is: store real values in kubectl create secret commands only, use placeholder text in all committed files, and reference secrets via environment variables in deployment YAMLs.

**CI/CD pipeline design**
The three-job pipeline (test, build, deploy) follows the principle that each stage gates the next. If tests fail, nothing gets built or deployed. If the build fails, nothing gets deployed. If the deployment rollout fails, the old version keeps running. This prevents broken code from reaching production.

**Kubernetes HPA and observability**
HPA requires metrics-server to be running to read CPU and memory values. The targets page in Prometheus shows you exactly what is being scraped and whether it is healthy. When Grafana shows N/A, the first thing to check is the Prometheus targets page, not the dashboard configuration.

**Git history rewriting**
Once a secret is committed, just deleting the file is not enough because the secret exists in git history. git filter-repo rewrites all commits to remove the file entirely. Combined with force push, it erases the secret from the remote repository as if it never existed.

**AWS EKS networking**
EKS nodes do not expose node-level metrics by default. Node Exporter must be deployed as a DaemonSet with hostNetwork: true and privileged: true to access the host proc and sys filesystems. Prometheus then scrapes the node IP directly at port 9100.

---

## Resume Bullets

- Built AI-powered Kubernetes operations platform on AWS EKS using Groq LLaMA 3.3 70B — 6 intelligence features including real-time incident triage, log anomaly detection across 15 failure patterns, deployment health scoring out of 100, and auto-generated P1/P2/P3 runbooks
- Designed two-microservice architecture with Flask REST API and Streamlit dashboard, containerised with Docker, stored in AWS ECR, deployed on AWS EKS with Horizontal Pod Autoscaler scaling from 2 to 10 replicas based on CPU and memory thresholds
- Implemented GitHub Actions CI/CD pipeline with three automated jobs: pytest unit tests, Docker build and ECR push, zero-downtime EKS rolling deployment with kubectl rollout status health gate — total pipeline duration under 2 minutes
- Configured complete observability stack with Prometheus scraping Flask metrics endpoint every 15 seconds, Node Exporter DaemonSet exposing CPU, memory, disk, and network metrics from all EKS nodes, and Grafana Node Exporter Full dashboard with live cluster visualisation
- Enforced production Kubernetes security standards: non-root containers (UID 1001), no privilege escalation, pod anti-affinity preventing co-location on same node, Kubernetes Secrets for API key management, liveness and readiness probes for automatic pod recovery

---

## Author

Krishna Kala

GitHub: https://github.com/krishnakala987-byte/KubeIntel-AI-Platform1
````
