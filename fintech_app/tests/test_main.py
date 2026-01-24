from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def get_auth_token():
    response = client.post(
        "/users/login",
        json={"username": "alexrivera", "password": "password123"}
    )
    return response.json()["access_token"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_user():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "alexrivera", "email": "alex.rivera@example.com"}

def test_get_user_not_found():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/99", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_user_unauthorized():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/2", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Operation not permitted"}

def test_get_wallet():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/wallets/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "user_id": 1, "balance": 1240.50}

def test_get_wallet_not_found():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/wallets/99", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}

def test_create_transaction():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Get initial balance
    response = client.get("/wallets/1", headers=headers)
    initial_balance = response.json()["balance"]

    # Deposit
    deposit_amount = 100.0
    response = client.post(
        "/wallets/1/transactions",
        json={"amount": deposit_amount, "type": "deposit"},
        headers=headers
    )
    assert response.status_code == 200
    transaction = response.json()
    assert transaction["amount"] == deposit_amount
    assert transaction["type"] == "deposit"

    # Check updated balance
    response = client.get("/wallets/1", headers=headers)
    assert response.json()["balance"] == initial_balance + deposit_amount

    # Withdrawal
    withdrawal_amount = 50.0
    response = client.post(
        "/wallets/1/transactions",
        json={"amount": withdrawal_amount, "type": "withdrawal"},
        headers=headers
    )
    assert response.status_code == 200
    transaction = response.json()
    assert transaction["amount"] == withdrawal_amount
    assert transaction["type"] == "withdrawal"

    # Check updated balance
    response = client.get("/wallets/1", headers=headers)
    assert response.json()["balance"] == initial_balance + deposit_amount - withdrawal_amount

def test_create_transaction_insufficient_funds():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/wallets/1/transactions",
        json={"amount": 999999.0, "type": "withdrawal"},
        headers=headers
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}

def test_get_pools():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/pools", headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Tech Founders", "total_amount": 5000.0, "participants": [1]}
    ]

def test_register_user():
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_login_for_access_token():
    response = client.post(
        "/users/login",
        json={"username": "alexrivera", "password": "password123"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_login_for_access_token_wrong_password():
    response = client.post(
        "/users/login",
        json={"username": "alexrivera", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
