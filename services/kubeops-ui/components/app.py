import streamlit as st
import requests
import json
import os

API_URL = os.environ.get("API_URL", "http://kubeops-api-service:5000")

st.set_page_config(
    page_title="KubeIntel AI Platform",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main-header {font-size: 2.2rem; font-weight: 800; color: #00D4FF;}
.sub-header {color: #aaa; font-size: 1rem; margin-top: -10px;}
.metric-card {background: #1a1a2e; padding: 20px; border-radius: 12px; border-left: 4px solid #00D4FF;}
.critical {border-left-color: #FF4444 !important;}
.warning  {border-left-color: #FFA500 !important;}
.healthy  {border-left-color: #00FF88 !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚙️ KubeIntel AI Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Kubernetes Operations Intelligence</p>', unsafe_allow_html=True)

tabs = st.tabs([
    "🔍 Cluster Analysis",
    "🚨 Incident Triage",
    "📋 Log Analyzer",
    "📦 Deployment Scorer",
    "🔐 Security Audit",
    "📖 Runbook Generator",
])

# --- TAB 1: CLUSTER ANALYSIS ---
with tabs[0]:
    st.subheader("🔍 Cluster State Analysis")
    st.markdown("Paste `kubectl get pods -A`, events, or describe output for AI analysis.")
    col1, col2 = st.columns([2, 1])
    with col1:
        cluster_context = st.text_area(
            "Cluster State / kubectl output",
            height=250,
            placeholder="kubectl get pods -A\nkubectl get events -n production\nkubectl describe pod <name>",
        )
        query = st.text_input(
            "Question / What to analyze",
            placeholder="Why is my deployment not scaling? What pods are unhealthy?",
        )
    with col2:
        mode = st.selectbox("Analysis Mode", ["general", "deployment", "security"])
        st.markdown("**Quick prompts:**")
        if st.button("🔎 Why are pods crashing?"):
            query = "Why are pods crashing and what is the fix?"
        if st.button("📊 Resource analysis"):
            query = "Analyze resource usage and suggest optimizations"
        if st.button("🔄 Rollout health"):
            query = "Is this rollout healthy? Any issues?"

    if st.button("🤖 Analyze with AI", type="primary"):
        if not query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("KubeIntel AI analyzing..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/analyze",
                        json={"context": cluster_context, "query": query, "mode": mode},
                        timeout=60)
                    if r.status_code == 200:
                        st.markdown("### 🤖 AI Analysis")
                        st.markdown(r.json()["response"])
                    else:
                        st.error(f"API Error: {r.status_code} — {r.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# --- TAB 2: INCIDENT TRIAGE ---
with tabs[1]:
    st.subheader("🚨 Incident Triage")
    st.markdown("Describe the incident — AI will give you a prioritized action plan.")
    col1, col2 = st.columns(2)
    with col1:
        symptoms = st.text_area("Symptoms / What is broken", height=150,
            placeholder="API latency spiked to 8000ms, pods in CrashLoopBackOff, 50% error rate on /checkout endpoint")
    with col2:
        cluster_state = st.text_area("Cluster State (optional)", height=150,
            placeholder="Paste kubectl get pods, events output here")

    namespace = st.text_input("Namespace", value="production")

    if st.button("🚨 Triage Incident", type="primary"):
        if not symptoms:
            st.warning("Describe the symptoms first.")
        else:
            with st.spinner("Running AI triage..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/incident/triage",
                        json={"symptoms": symptoms, "cluster_state": cluster_state, "namespace": namespace},
                        timeout=60)
                    if r.status_code == 200:
                        st.markdown("### 🚨 Triage Report")
                        st.markdown(r.json()["triage_report"])
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 3: LOG ANALYZER ---
with tabs[2]:
    st.subheader("📋 Log Anomaly Detection")
    st.markdown("Paste Kubernetes pod logs — AI detects anomalies and gives root cause analysis.")
    logs_input = st.text_area("Paste Pod Logs", height=300,
        placeholder="kubectl logs -n production deploy/api-service --tail=200")

    if st.button("🔍 Analyze Logs", type="primary"):
        if not logs_input.strip():
            st.warning("Paste some logs first.")
        else:
            with st.spinner("Analyzing logs..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/analyze/logs",
                        json={"logs": logs_input}, timeout=60)
                    if r.status_code == 200:
                        data = r.json()
                        parsed = data["parsed_analysis"]
                        col1, col2, col3, col4 = st.columns(4)
                        status = parsed["overall_status"]
                        col1.metric("Status", status)
                        col2.metric("Total Lines", parsed["total_lines"])
                        col3.metric("Errors", parsed["error_count"])
                        col4.metric("Warnings", parsed["warning_count"])

                        if parsed["findings"]:
                            st.markdown("### Detected Anomalies")
                            for f in parsed["findings"]:
                                color = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(f["severity"], "⚪")
                                st.markdown(f"{color} **[{f['severity']}] Line {f['line_number']}** — {f['description']}")
                                st.code(f["line"], language="text")

                        st.markdown("### 🤖 AI Root Cause Analysis")
                        st.markdown(data["ai_diagnosis"])
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 4: DEPLOYMENT SCORER ---
with tabs[3]:
    st.subheader("📦 Deployment Production Readiness Score")
    st.markdown("Paste your Kubernetes Deployment YAML — get a scored health report.")
    yaml_input = st.text_area("Deployment YAML", height=300,
        placeholder="apiVersion: apps/v1\nkind: Deployment\n...")

    if st.button("📊 Score Deployment", type="primary"):
        if not yaml_input.strip():
            st.warning("Paste a deployment YAML first.")
        else:
            with st.spinner("Scoring deployment..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/deployment/score",
                        json={"yaml_content": yaml_input}, timeout=60)
                    if r.status_code == 200:
                        score_data = r.json()
                        if "overall_score" in score_data:
                            overall = score_data["overall_score"]
                            color = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
                            st.markdown(f"## {color} Overall Score: **{overall}/100**")

                            if "grades" in score_data:
                                cols = st.columns(5)
                                for i, (k, v) in enumerate(score_data["grades"].items()):
                                    cols[i].metric(k.replace("_", " ").title(), f"{v}/100")

                            if score_data.get("critical_issues"):
                                st.error("**Critical Issues:**\n" + "\n".join(f"• {i}" for i in score_data["critical_issues"]))
                            if score_data.get("warnings"):
                                st.warning("**Warnings:**\n" + "\n".join(f"• {w}" for w in score_data["warnings"]))
                            if score_data.get("recommendations"):
                                st.success("**Recommendations:**\n" + "\n".join(f"• {r}" for r in score_data["recommendations"]))
                        else:
                            st.json(score_data)
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 5: SECURITY AUDIT ---
with tabs[4]:
    st.subheader("🔐 Kubernetes Security Audit")
    st.markdown("Paste Kubernetes manifests — AI checks for security misconfigurations.")
    manifests = st.text_area("Kubernetes Manifests (YAML)", height=300,
        placeholder="Paste deployments, RBAC, network policies...")

    if st.button("🔐 Run Security Audit", type="primary"):
        if not manifests.strip():
            st.warning("Paste manifests to audit.")
        else:
            with st.spinner("Running security audit..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/security/audit",
                        json={"manifests": manifests}, timeout=60)
                    if r.status_code == 200:
                        st.markdown("### 🔐 Security Audit Report")
                        st.markdown(r.json()["audit_report"])
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 6: RUNBOOK GENERATOR ---
with tabs[5]:
    st.subheader("📖 Auto Runbook Generator")
    st.markdown("Describe any Kubernetes incident — get a production runbook instantly.")
    incident_desc = st.text_area("Incident Description", height=200,
        placeholder="Production pods in CrashLoopBackOff after deployment v2.4.1. Liveness probe failing. Memory usage spiked to 2GB before crash. Last change was new env variable injection.")

    if st.button("📖 Generate Runbook", type="primary"):
        if not incident_desc.strip():
            st.warning("Describe the incident first.")
        else:
            with st.spinner("Generating runbook..."):
                try:
                    r = requests.post(f"{API_URL}/api/v1/incident/runbook",
                        json={"incident": incident_desc}, timeout=60)
                    if r.status_code == 200:
                        st.markdown("### 📖 Generated Runbook")
                        st.markdown(r.json()["runbook"])
                        st.download_button("⬇️ Download Runbook",
                            data=r.json()["runbook"],
                            file_name="incident-runbook.md",
                            mime="text/markdown")
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.markdown("**KubeIntel AI Platform** — Built by Krishna Kala | AWS EKS + Kubernetes + Groq LLaMA 3.3 70B")