from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Wallet(BaseModel):
    id: int
    user_id: int
    balance: float

from datetime import datetime

class Pool(BaseModel):
    id: int
    name: str
    total_amount: float
    participants: List[int]

class Transaction(BaseModel):
    id: int
    wallet_id: int
    amount: float
    type: str
    timestamp: datetime

class TransactionCreate(BaseModel):
    amount: float
    type: str # "deposit" or "withdrawal"
