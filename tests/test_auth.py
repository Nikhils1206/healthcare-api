def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "pytest_user@example.com",
            "password": "TestPassword123",
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "pytest_user@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_duplicate_email(client):
    user_data = {
        "full_name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "TestPassword123",
        "role": "MEMBER",
    }

    first_response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert second_response.status_code == 409


def test_login(client):
    user_data = {
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "TestPassword123",
        "role": "MEMBER",
    }

    register_response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    user_data = {
        "full_name": "Wrong Password User",
        "email": "wrongpassword@example.com",
        "password": "TestPassword123",
        "role": "MEMBER",
    }

    client.post(
        "/auth/register",
        json=user_data,
    )

    response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": "WrongPassword123",
        },
    )

    assert response.status_code in [401, 400]