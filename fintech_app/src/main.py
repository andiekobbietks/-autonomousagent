from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from .models import User, Wallet, Pool, UserCreate, UserLogin, Transaction, TransactionCreate
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT encoding")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory database (for prototyping purposes) with hashed passwords
db = {
    "users": {
        1: User(id=1, username="alexrivera", email="alex.rivera@example.com"),
        2: User(id=2, username="jules", email="jules@example.com"),
    },
    "hashed_passwords": {
        "alexrivera": pwd_context.hash("password123"),
        "jules": pwd_context.hash("password456"),
    },
    "wallets": {
        1: Wallet(id=1, user_id=1, balance=1240.50),
    },
    "pools": {
        1: Pool(id=1, name="Tech Founders", total_amount=5000.00, participants=[1]),
    },
    "transactions": []
}

oauth2_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = None
    for u in db["users"].values():
        if u.username == username:
            user = u
            break

    if user is None:
        raise credentials_exception
    return user

@app.get("/health")
def read_root():
    return {"status": "ok"}

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = db["users"].get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return user

@app.post("/users/register", response_model=User)
def register_user(user: UserCreate):
    for existing_user in db["users"].values():
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    new_user_id = max(db["users"].keys() or [0]) + 1
    new_user = User(id=new_user_id, username=user.username, email=user.email)
    db["users"][new_user_id] = new_user
    db["hashed_passwords"][user.username] = pwd_context.hash(user.password)
    return new_user

@app.post("/users/login")
def login_for_access_token(user_login: UserLogin):
    user = None
    for u in db["users"].values():
        if u.username == user_login.username:
            user = u
            break

    if not user or not pwd_context.verify(user_login.password, db["hashed_passwords"].get(user.username)):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/wallets/{wallet_id}", response_model=Wallet)
def get_wallet(wallet_id: int, current_user: User = Depends(get_current_user)):
    wallet = db["wallets"].get(wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return wallet

@app.post("/wallets/{wallet_id}/transactions", response_model=Transaction)
def create_transaction(wallet_id: int, transaction: TransactionCreate, current_user: User = Depends(get_current_user)):
    wallet = db["wallets"].get(wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    if transaction.type == "deposit":
        wallet.balance += transaction.amount
    elif transaction.type == "withdrawal":
        if wallet.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        wallet.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    new_transaction_id = len(db["transactions"]) + 1
    new_transaction = Transaction(
        id=new_transaction_id,
        wallet_id=wallet_id,
        amount=transaction.amount,
        type=transaction.type,
        timestamp=datetime.utcnow()
    )
    db["transactions"].append(new_transaction)
    return new_transaction

@app.get("/pools", response_model=List[Pool])
def get_pools(current_user: User = Depends(get_current_user)):
    return list(db["pools"].values())
