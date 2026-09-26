import json

try:
    import requests  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - optional dependency at runtime
    requests = None


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def analyze_claim(claim):
    prompt = f"""
You are an insurance claim analysis assistant.

Analyze the following healthcare claim and identify potential risk indicators.

Claim:
Claim Number: {claim.claim_number}
Service Date: {claim.service_date}
Description: {claim.description}
Diagnosis: {claim.diagnosis}
Billed Amount: {claim.billed_amount}

Return ONLY valid JSON in this format:

{{
    "risk_score": 0.0,
    "risk_level": "LOW",
    "flags": [],
    "summary": ""
}}

Rules:
- risk_score must be between 0 and 1.
- risk_level must be LOW, MEDIUM, or HIGH.
- flags must contain specific reasons for potential risk.
- Do not approve or reject the claim.
- This is only an advisory analysis.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(result["response"])