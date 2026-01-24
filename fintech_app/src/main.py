from fastapi import FastAPI, HTTPException
from typing import List
from .models import User, Wallet, Pool

app = FastAPI()

# In-memory database
db = {
    "users": {
        1: User(id=1, username="alexrivera", email="alex.rivera@example.com"),
        2: User(id=2, username="jules", email="jules@example.com"),
    },
    "wallets": {
        1: Wallet(id=1, user_id=1, balance=1240.50),
    },
    "pools": {
        1: Pool(id=1, name="Tech Founders", total_amount=5000.00, participants=[1, 2]),
        2: Pool(id=2, name="Family Savings", total_amount=10000.00, participants=[1]),
    }
}

@app.get("/health")
def read_root():
    return {"status": "ok"}

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = db["users"].get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/wallets/{wallet_id}", response_model=Wallet)
def get_wallet(wallet_id: int):
    wallet = db["wallets"].get(wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.get("/pools", response_model=List[Pool])
def get_pools():
    return list(db["pools"].values())
