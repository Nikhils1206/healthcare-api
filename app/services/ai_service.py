import json
import importlib
from fastapi import HTTPException
try:
    import requests  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - optional dependency at runtime
    requests = None

from sqlalchemy.orm import Session

if __package__:
    try:
        ai_analysis_module = importlib.import_module(
            ".schemas.ai_analysis",
            __package__,
        )
        claim_ai_analysis_module = importlib.import_module(
            ".models.claim_ai_analysis",
            __package__,
        )
    except ImportError:  # pragma: no cover - fallback for direct execution / package config
        ai_analysis_module = importlib.import_module("app.schemas.ai_analysis")
        claim_ai_analysis_module = importlib.import_module("app.models.claim_ai_analysis")
else:
    ai_analysis_module = importlib.import_module("app.schemas.ai_analysis")
    claim_ai_analysis_module = importlib.import_module("app.models.claim_ai_analysis")

AIClaimAnalysis = ai_analysis_module.AIClaimAnalysis
ClaimAIAnalysis = claim_ai_analysis_module.ClaimAIAnalysis


def save_claim_analysis(
    db: Session,
    claim_id,
    analysis: dict,
):
    ai_analysis = (
        db.query(ClaimAIAnalysis)
        .filter(ClaimAIAnalysis.claim_id == claim_id)
        .first()
    )

    if ai_analysis:
        ai_analysis.risk_score = analysis["risk_score"]
        ai_analysis.risk_level = analysis["risk_level"]
        ai_analysis.flags = analysis["flags"]
        ai_analysis.summary = analysis["summary"]
    else:
        ai_analysis = ClaimAIAnalysis(
            claim_id=claim_id,
            risk_score=analysis["risk_score"],
            risk_level=analysis["risk_level"],
            flags=analysis["flags"],
            summary=analysis["summary"],
        )
        db.add(ai_analysis)

    db.commit()
    db.refresh(ai_analysis)

    return ai_analysis

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

    try:
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

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is currently unavailable",
        ) from exc

    try:
        result = response.json()
        analysis = json.loads(result["response"])

        validated_analysis = AIClaimAnalysis.model_validate(
            analysis
        )

    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="AI service returned an invalid response",
        ) from exc

    return validated_analysis.model_dump()