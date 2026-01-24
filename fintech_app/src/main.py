from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

from .config import settings

# JWT settings
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = HTTPBearer()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def generate_referral_code(db: Session):
    while True:
        code = secrets.token_urlsafe(6).upper()
        if not db.query(models.User).filter(models.User.referral_code == code).first():
            return code

def create_notification(db: Session, user_id: int, title: str, message: str, type: str):
    db_notification = models.Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@app.get("/health")
def read_root():
    return {"status": "ok"}

@app.post("/users/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    referred_by_user = None
    if user.referral_code:
        referred_by_user = db.query(models.User).filter(models.User.referral_code == user.referral_code).first()
        if not referred_by_user:
            raise HTTPException(status_code=400, detail="Invalid referral code")

    hashed_password = pwd_context.hash(user.password)
    referral_code = generate_referral_code(db)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        referral_code=referral_code,
        referred_by=referred_by_user.id if referred_by_user else None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if referred_by_user:
        referral = models.Referral(
            referrer_id=referred_by_user.id,
            referred_id=db_user.id
        )
        db.add(referral)
        db.commit()
    # Also create a wallet for the new user
    wallet = models.Wallet(user_id=db_user.id, balance=0.0)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return db_user

@app.post("/users/login")
def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_login.username).first()
    if not user or not pwd_context.verify(user_login.password, user.hashed_password):
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

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/wallets/{wallet_id}", response_model=schemas.Wallet)
def get_wallet(wallet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return wallet

@app.post("/wallets/{wallet_id}/transactions", response_model=schemas.Transaction)
def create_transaction(wallet_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
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

    db_transaction = models.Transaction(**transaction.model_dump(), wallet_id=wallet_id, timestamp=datetime.now(timezone.utc))
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Create notification
    create_notification(
        db=db,
        user_id=current_user.id,
        title=f"{transaction.type.capitalize()} Successful",
        message=f"Your {transaction.type} of ${transaction.amount} was successful.",
        type="success"
    )

    return db_transaction

@app.post("/pools", response_model=schemas.Pool)
def create_pool(pool: schemas.PoolCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_pool = models.Pool(**pool.model_dump())
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    return db_pool

@app.get("/pools", response_model=List[schemas.Pool])
def get_pools(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Pool).all()

@app.get("/pools/{pool_id}", response_model=schemas.Pool)
def get_pool(pool_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pool = db.query(models.Pool).filter(models.Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return pool

@app.post("/pools/{pool_id}/join", response_model=schemas.Pool)
def join_pool(pool_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pool = db.query(models.Pool).filter(models.Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")

    if current_user in pool.participants:
        raise HTTPException(status_code=400, detail="User already in pool")

    pool.participants.append(current_user)
    db.commit()
    db.refresh(pool)

    # Create notification
    create_notification(
        db=db,
        user_id=current_user.id,
        title="Joined Pool",
        message=f"You have successfully joined the pool '{pool.name}'.",
        type="info"
    )

    return pool

@app.post("/pools/{pool_id}/leave", response_model=schemas.Pool)
def leave_pool(pool_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pool = db.query(models.Pool).filter(models.Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")

    if current_user not in pool.participants:
        raise HTTPException(status_code=400, detail="User not in pool")

    pool.participants.remove(current_user)
    db.commit()
    db.refresh(pool)
    return pool

@app.post("/sprints", response_model=schemas.Sprint)
def create_sprint(sprint: schemas.SprintCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_sprint = models.Sprint(**sprint.model_dump(), current_amount=0.0)
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint

@app.get("/sprints", response_model=List[schemas.Sprint])
def get_sprints(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Sprint).all()

@app.get("/sprints/{sprint_id}", response_model=schemas.Sprint)
def get_sprint(sprint_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@app.post("/sprints/{sprint_id}/contribute", response_model=schemas.Contribution)
def contribute_to_sprint(sprint_id: int, contribution: schemas.ContributionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")

    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < contribution.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= contribution.amount
    sprint.current_amount += contribution.amount

    db_contribution = models.Contribution(**contribution.model_dump(), sprint_id=sprint_id, user_id=current_user.id, timestamp=datetime.now(timezone.utc))
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)

    # Create notification
    create_notification(
        db=db,
        user_id=current_user.id,
        title="Contribution Successful",
        message=f"Your contribution of ${contribution.amount} to the sprint '{sprint.name}' was successful.",
        type="success"
    )

    return db_contribution

@app.get("/notifications", response_model=List[schemas.Notification])
def get_notifications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()

@app.get("/referrals", response_model=List[schemas.Referral])
def get_referrals(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Referral).filter(models.Referral.referrer_id == current_user.id).all()

@app.post("/notifications/{notification_id}/read", response_model=schemas.Notification)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    notification.read = True
    db.commit()
    db.refresh(notification)
    return notification
