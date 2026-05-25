import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are KubeIntel, a senior Site Reliability Engineer and Kubernetes expert AI assistant.
You specialize in:
- Kubernetes cluster health analysis and troubleshooting
- Pod crash loop diagnosis (CrashLoopBackOff, OOMKilled, ImagePullBackOff)
- Log anomaly detection and root cause analysis
- Incident triage and runbook generation
- Deployment strategy recommendations (rolling, canary, blue-green)
- Resource optimization (CPU/memory requests and limits)
- Security posture analysis (RBAC, network policies, secrets management)
- CI/CD pipeline health assessment

When given Kubernetes logs, events, or cluster state — you provide:
1. A concise diagnosis (what is wrong)
2. Root cause analysis
3. Immediate remediation steps with exact kubectl commands
4. Prevention recommendations

Always respond with actionable, production-grade DevOps guidance. Format responses with clear sections.
Never give generic answers. Always give specific kubectl commands, YAML snippets, or shell scripts."""


def analyze_with_ai(context: str, query: str, mode: str = "general") -> str:
    """
    Core AI analysis function.
    mode: general | incident | logs | deployment | security
    """
    mode_prefixes = {
        "incident": "INCIDENT TRIAGE REQUEST:\n",
        "logs": "LOG ANALYSIS REQUEST:\n",
        "deployment": "DEPLOYMENT HEALTH CHECK:\n",
        "security": "SECURITY AUDIT REQUEST:\n",
        "general": "KUBERNETES QUERY:\n",
    }

    prefix = mode_prefixes.get(mode, "KUBERNETES QUERY:\n")
    full_prompt = f"{prefix}\nCONTEXT:\n{context}\n\nQUESTION:\n{query}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt},
        ],
        max_tokens=2048,
        temperature=0.2,
    )
    return response.choices[0].message.content


def generate_runbook(incident_description: str) -> str:
    prompt = f"""Generate a production incident runbook for the following Kubernetes issue:

{incident_description}

Format the runbook with:
1. INCIDENT SUMMARY
2. SEVERITY LEVEL (P1/P2/P3)
3. IMMEDIATE ACTIONS (first 5 minutes)
4. INVESTIGATION STEPS (exact kubectl commands)
5. RESOLUTION STEPS
6. POST-INCIDENT TASKS
7. PREVENTION MEASURES"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.1,
    )
    return response.choices[0].message.content


def score_deployment_health(deployment_yaml: str) -> dict:
    prompt = f"""Analyze this Kubernetes deployment YAML and return a JSON health score report.

DEPLOYMENT YAML:
{deployment_yaml}

Return ONLY a JSON object with this exact structure:
{{
  "overall_score": <0-100>,
  "grades": {{
    "resource_limits": <0-100>,
    "health_probes": <0-100>,
    "security_context": <0-100>,
    "replica_strategy": <0-100>,
    "image_policy": <0-100>
  }},
  "critical_issues": ["issue1", "issue2"],
  "warnings": ["warn1", "warn2"],
  "recommendations": ["rec1", "rec2"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
        temperature=0.0,
    )
    import json, re
    text = response.choices[0].message.content
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"error": "Could not parse response", "raw": text}