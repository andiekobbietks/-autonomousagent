from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class WalletBase(BaseModel):
    balance: float

class TransactionBase(BaseModel):
    amount: float
    type: str

class TransactionCreate(TransactionBase):
    pass

class ContributionBase(BaseModel):
    amount: float

class ContributionCreate(ContributionBase):
    pass

class SprintBase(BaseModel):
    name: str
    goal_amount: float
    start_time: datetime
    end_time: datetime

class SprintCreate(SprintBase):
    pass

class PoolBase(BaseModel):
    name: str
    total_amount: float

class PoolCreate(PoolBase):
    pass


# Schemas with Relationships for Reading Data

from pydantic import ConfigDict

class Transaction(TransactionBase):
    id: int
    wallet_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class Wallet(WalletBase):
    id: int
    user_id: int
    transactions: List[Transaction] = []

    model_config = ConfigDict(from_attributes=True)

class Contribution(ContributionBase):
    id: int
    sprint_id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class Sprint(SprintBase):
    id: int
    current_amount: float
    contributions: List[Contribution] = []

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    wallet: Optional[Wallet] = None
    contributions: List[Contribution] = []

    model_config = ConfigDict(from_attributes=True)

class Pool(PoolBase):
    id: int
    participants: List[User] = []

    model_config = ConfigDict(from_attributes=True)
