import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.database import Base
from src import models
from datetime import datetime, timedelta, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client():
    # Setup: create tables
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Teardown: drop tables
    Base.metadata.drop_all(bind=engine)


def test_register_and_login(client):
    # Register user
    reg_response = client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert reg_response.status_code == 200
    user_data = reg_response.json()
    assert user_data["username"] == "testuser"
    assert "referral_code" in user_data

    # Login
    login_response = client.post("/users/login", json={"username": "testuser", "password": "password"})
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data

def test_referral_system(client):
    # Register referrer
    referrer_res = client.post("/users/register", json={"username": "referrer", "email": "referrer@example.com", "password": "password123"})
    referrer_id = referrer_res.json()["id"]
    referral_code = referrer_res.json()["referral_code"]

    # Register referred user
    client.post("/users/register", json={"username": "referred", "email": "referred@example.com", "password": "password456", "referral_code": referral_code})

    # Login as referrer and check referrals
    login_res = client.post("/users/login", json={"username": "referrer", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    referrals_res = client.get("/referrals", headers=headers)
    assert referrals_res.status_code == 200
    referrals = referrals_res.json()
    assert len(referrals) == 1
    assert referrals[0]["referrer_id"] == referrer_id

def test_full_flow(client):
    # 1. Register and Login
    client.post("/users/register", json={"username": "mainuser", "email": "main@example.com", "password": "password"})
    login_res = client.post("/users/login", json={"username": "mainuser", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Deposit funds
    user_res = client.get("/users/1", headers=headers)
    wallet_id = user_res.json()["wallet"]["id"]
    client.post(f"/wallets/{wallet_id}/transactions", json={"amount": 500, "type": "deposit"}, headers=headers)

    # 3. Create and join a pool
    pool_res = client.post("/pools", json={"name": "Test Pool", "total_amount": 1000}, headers=headers)
    pool_id = pool_res.json()["id"]
    client.post(f"/pools/{pool_id}/join", headers=headers)

    # 4. Create and contribute to a sprint
    start_time = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    end_time = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    sprint_res = client.post("/sprints", json={"name": "Test Sprint", "goal_amount": 500, "start_time": start_time, "end_time": end_time}, headers=headers)
    sprint_id = sprint_res.json()["id"]

    contrib_res = client.post(f"/sprints/{sprint_id}/contribute", json={"amount": 100}, headers=headers)
    assert contrib_res.status_code == 200

    # 5. Check notifications
    notif_res = client.get("/notifications", headers=headers)
    assert notif_res.status_code == 200
    notifications = notif_res.json()
    assert len(notifications) > 2 # Deposit, Join, Contribution, etc.

    # Mark one as read
    notif_id = notifications[0]["id"]
    read_res = client.post(f"/notifications/{notif_id}/read", headers=headers)
    assert read_res.status_code == 200
    assert read_res.json()["read"] is True
