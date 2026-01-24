from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    username: str
    email: str

class Wallet(BaseModel):
    id: int
    user_id: int
    balance: float

class Pool(BaseModel):
    id: int
    name: str
    total_amount: float
    participants: List[int]
