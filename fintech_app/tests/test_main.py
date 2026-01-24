import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.database import Base
from datetime import datetime, timedelta, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

def get_auth_token(client):
    client.post(
        "/users/register",
        json={"username": "alexrivera", "email": "alex.rivera@example.com", "password": "password123"}
    )
    response = client.post(
        "/users/login",
        json={"username": "alexrivera", "password": "password123"}
    )
    return response.json()["access_token"]

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_user(client):
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_login_for_access_token(client):
    client.post(
        "/users/register",
        json={"username": "alexrivera", "email": "alex.rivera@example.com", "password": "password123"}
    )
    response = client.post(
        "/users/login",
        json={"username": "alexrivera", "password": "password123"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_get_user(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "alexrivera", "email": "alex.rivera@example.com", "wallet": {'balance': 0.0, 'id': 1, 'transactions': [], 'user_id': 1}, "contributions": []}

def test_create_sprint_and_contribute(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create Sprint
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(hours=6)
    sprint_response = client.post(
        "/sprints",
        json={
            "name": "Test Sprint",
            "goal_amount": 1000.0,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        },
        headers=headers,
    )
    assert sprint_response.status_code == 200
    sprint = sprint_response.json()
    sprint_id = sprint["id"]

    # Contribute to Sprint
    contribution_amount = 100.0
    contribution_response = client.post(
        f"/sprints/{sprint_id}/contribute",
        json={"amount": contribution_amount},
        headers=headers,
    )
    # This will fail because the user has no money. Let's first deposit.

    # Deposit money
    deposit_response = client.post(
        "/wallets/1/transactions",
        json={"amount": 500.0, "type": "deposit"},
        headers=headers,
    )
    assert deposit_response.status_code == 200

    # Retry contribution
    contribution_response = client.post(
        f"/sprints/{sprint_id}/contribute",
        json={"amount": contribution_amount},
        headers=headers,
    )
    assert contribution_response.status_code == 200
    contribution = contribution_response.json()
    assert contribution["amount"] == contribution_amount

    # Check sprint's current amount
    sprint_response = client.get(f"/sprints/{sprint_id}", headers=headers)
    assert sprint_response.json()["current_amount"] == contribution_amount

def test_create_and_manage_pool(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a pool
    pool_response = client.post(
        "/pools",
        json={"name": "Test Pool", "total_amount": 1000.0},
        headers=headers,
    )
    assert pool_response.status_code == 200
    pool = pool_response.json()
    pool_id = pool["id"]
    assert pool["name"] == "Test Pool"

    # Get all pools
    pools_response = client.get("/pools", headers=headers)
    assert pools_response.status_code == 200
    assert len(pools_response.json()) > 0

    # Get single pool
    single_pool_response = client.get(f"/pools/{pool_id}", headers=headers)
    assert single_pool_response.status_code == 200
    assert single_pool_response.json()["id"] == pool_id

    # Join pool
    join_response = client.post(f"/pools/{pool_id}/join", headers=headers)
    assert join_response.status_code == 200
    assert len(join_response.json()["participants"]) == 1

    # Leave pool
    leave_response = client.post(f"/pools/{pool_id}/leave", headers=headers)
    assert leave_response.status_code == 200
    assert len(leave_response.json()["participants"]) == 0

def test_notifications(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Initial notifications check
    response = client.get("/notifications", headers=headers)
    assert response.status_code == 200
    initial_notification_count = len(response.json())

    # Trigger a notification by joining a pool
    pool_response = client.post(
        "/pools",
        json={"name": "Notification Test Pool", "total_amount": 100.0},
        headers=headers,
    )
    pool_id = pool_response.json()["id"]
    client.post(f"/pools/{pool_id}/join", headers=headers)

    # Verify new notification
    response = client.get("/notifications", headers=headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == initial_notification_count + 1
    assert notifications[-1]["title"] == "Joined Pool"

    # Mark notification as read
    notification_id = notifications[-1]["id"]
    response = client.post(f"/notifications/{notification_id}/read", headers=headers)
    assert response.status_code == 200
    assert response.json()["read"] is True
