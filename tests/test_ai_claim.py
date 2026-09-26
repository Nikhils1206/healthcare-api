from unittest.mock import patch

from app.models.claim import ClaimStatus
from app.models.claim_ai_analysis import ClaimAIAnalysis

def test_analyze_claim(client, db):
    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "AI Test User",
            "email": "ai_test@example.com",
            "password": "password123",
            "role": "MEMBER",
        },
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "ai_test@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create member profile
    member_response = client.post(
        "/members",
        headers=headers,
        json={
            "date_of_birth": "2000-01-01",
            "gender": "Male",
            "phone": "9876543210",
            "blood_group": "O+",
            "address": "Test Address",
            "emergency_contact": "9876543211",
        },
    )

    assert member_response.status_code == 201

    # Create claim
    claim_response = client.post(
        "/claims",
        headers=headers,
        json={
            "service_date": "2026-09-20",
            "description": "Hospital treatment",
            "diagnosis": "Fever",
            "billed_amount": "50000.00",
        },
    )

    assert claim_response.status_code == 201

    claim_id = claim_response.json()["id"]

    # Mock Ollama response
    mock_analysis = {
        "risk_score": 0.82,
        "risk_level": "HIGH",
        "flags": [
            "Unusually high billed amount"
        ],
        "summary": "Claim requires additional review.",
    }

    with patch(
        "app.routers.claim.analyze_claim",
        return_value=mock_analysis,
    ):
        response = client.post(
            f"/claims/{claim_id}/analyze",
            headers=headers,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == claim_id
    assert "claim_number" in data
    assert data["analysis"]["risk_score"] == 0.82
    assert data["analysis"]["risk_level"] == "HIGH"
    assert len(data["analysis"]["flags"]) > 0
    assert "summary" in data["analysis"]

    db_analysis = (
        db.query(ClaimAIAnalysis)
        .filter(ClaimAIAnalysis.claim_id == claim_id)
        .first()
    )

    assert db_analysis is not None
    assert float(db_analysis.risk_score) == 0.82
    assert db_analysis.risk_level == "HIGH"
    assert db_analysis.flags == [
        "Unusually high billed amount"
    ]
    assert db_analysis.summary == "Claim requires additional review."