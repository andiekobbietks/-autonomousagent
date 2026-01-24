from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "alexrivera", "email": "alex.rivera@example.com"}

def test_get_user_not_found():
    response = client.get("/users/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_wallet():
    response = client.get("/wallets/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "user_id": 1, "balance": 1240.50}

def test_get_wallet_not_found():
    response = client.get("/wallets/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}

def test_get_pools():
    response = client.get("/pools")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Tech Founders", "total_amount": 5000.0, "participants": [1, 2]},
        {"id": 2, "name": "Family Savings", "total_amount": 10000.0, "participants": [1]}
    ]
