def get_auth_token(client, email="member_test@example.com"):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Member Test User",
            "email": email,
            "password": "TestPassword123",
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_create_member(client):
    token = get_auth_token(client)

    response = client.post(
        "/members",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date_of_birth": "2000-01-15",
            "gender": "Male",
            "phone": "9876543210",
            "blood_group": "O+",
            "address": "Indore, India",
            "emergency_contact": "9876500000",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "user_id" in data
    assert data["phone"] == "9876543210"


def test_get_member(client):
    token = get_auth_token(
        client,
        "get_member@example.com",
    )

    create_response = client.post(
        "/members",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date_of_birth": "2000-01-15",
            "gender": "Male",
            "phone": "9876543211",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/members/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["phone"] == "9876543211"


def test_update_member(client):
    token = get_auth_token(
        client,
        "update_member@example.com",
    )

    create_response = client.post(
        "/members",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date_of_birth": "2000-01-15",
            "gender": "Male",
            "phone": "9876543212",
        },
    )

    assert create_response.status_code == 201

    response = client.patch(
        "/members/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "phone": "9999999999",
            "address": "Mumbai, India",
        },
    )
    print(response.json())


    assert response.status_code == 200

    data = response.json()

    assert data["phone"] == "9999999999"
    assert data["address"] == "Mumbai, India"


def test_delete_member(client):
    token = get_auth_token(
        client,
        "delete_member@example.com",
    )

    create_response = client.post(
        "/members",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date_of_birth": "2000-01-15",
            "gender": "Male",
            "phone": "9876543213",
        },
    )

    assert create_response.status_code == 201

    response = client.delete(
        "/members/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Member deleted successfully"


def test_member_requires_authentication(client):
    response = client.get("/members/me")

    assert response.status_code in [401, 403]