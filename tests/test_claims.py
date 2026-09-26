from datetime import date


def get_auth_token(client, email):
    client.post(
        "/auth/register",
        json={
            "full_name": "Claims Test User",
            "email": email,
            "password": "TestPassword123",
            "role": "MEMBER",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_member(client, token):
    response = client.post(
        "/members",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date_of_birth": "2000-01-15",
            "gender": "Male",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201


def test_create_claim(client):
    token = get_auth_token(
        client,
        "claim_create@example.com",
    )

    create_member(client, token)

    response = client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_date": "2026-09-25",
            "description": "Hospital consultation",
            "diagnosis": "Acute infection",
            "billed_amount": 5000.00,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "claim_number" in data
    assert data["status"] == "PENDING"
    assert data["approved_amount"] is None
    assert float(data["billed_amount"]) == 5000.00


def test_get_claims(client):
    token = get_auth_token(
        client,
        "claim_get@example.com",
    )

    create_member(client, token)

    client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_date": "2026-09-25",
            "description": "Medical treatment",
            "diagnosis": "Infection",
            "billed_amount": 3000.00,
        },
    )

    response = client.get(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "PENDING"


def test_get_single_claim(client):
    token = get_auth_token(
        client,
        "claim_single@example.com",
    )

    create_member(client, token)

    create_response = client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_date": "2026-09-25",
            "description": "Doctor consultation",
            "diagnosis": "Fever",
            "billed_amount": 1500.00,
        },
    )

    claim_id = create_response.json()["id"]

    response = client.get(
        f"/claims/{claim_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == claim_id


def test_claim_pagination(client):
    token = get_auth_token(
        client,
        "claim_pagination@example.com",
    )

    create_member(client, token)

    for amount in [1000, 2000, 3000]:
        response = client.post(
            "/claims",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "service_date": "2026-09-25",
                "description": "Medical service",
                "diagnosis": "Treatment",
                "billed_amount": amount,
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/claims?page=1&limit=2",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_claim_status_filter(client):
    token = get_auth_token(
        client,
        "claim_filter@example.com",
    )

    create_member(client, token)

    response = client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_date": "2026-09-25",
            "description": "Medical service",
            "diagnosis": "Treatment",
            "billed_amount": 2000,
        },
    )

    assert response.status_code == 201

    response = client.get(
        "/claims?status=PENDING",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "PENDING"


def test_claim_requires_authentication(client):
    response = client.get("/claims")

    assert response.status_code in [401, 403]

def get_user_token(client, email, role):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Role Test User",
            "email": email,
            "password": "TestPassword123",
            "role": role,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_test_claim(client, token):
    create_member(client, token)

    response = client.post(
        "/claims",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "service_date": "2026-09-25",
            "description": "Hospital treatment",
            "diagnosis": "Acute infection",
            "billed_amount": 5000,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_member_cannot_approve_claim(client):
    token = get_user_token(
        client,
        "member_approve@example.com",
        "MEMBER",
    )

    claim_id = create_test_claim(client, token)

    response = client.patch(
        f"/claims/{claim_id}/approve",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "approved_amount": 4000
        },
    )

    assert response.status_code == 403


def test_member_cannot_reject_claim(client):
    token = get_user_token(
        client,
        "member_reject@example.com",
        "MEMBER",
    )

    claim_id = create_test_claim(client, token)

    response = client.patch(
        f"/claims/{claim_id}/reject",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_provider_can_approve_claim(client):
    member_token = get_user_token(
        client,
        "provider_member@example.com",
        "MEMBER",
    )

    claim_id = create_test_claim(
        client,
        member_token,
    )

    provider_token = get_user_token(
        client,
        "provider_reviewer@example.com",
        "PROVIDER",
    )

    response = client.patch(
        f"/claims/{claim_id}/approve",
        headers={
            "Authorization": f"Bearer {provider_token}"
        },
        json={
            "approved_amount": 4000
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "APPROVED"
    assert float(data["approved_amount"]) == 4000


def test_cannot_approve_more_than_billed(client):
    member_token = get_user_token(
        client,
        "amount_member@example.com",
        "MEMBER",
    )

    claim_id = create_test_claim(
        client,
        member_token,
    )

    provider_token = get_user_token(
        client,
        "amount_provider@example.com",
        "PROVIDER",
    )

    response = client.patch(
        f"/claims/{claim_id}/approve",
        headers={
            "Authorization": f"Bearer {provider_token}"
        },
        json={
            "approved_amount": 6000
        },
    )

    assert response.status_code == 400
    