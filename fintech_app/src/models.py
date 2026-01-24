from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

user_pool_association = Table('user_pool_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('pool_id', Integer, ForeignKey('pools.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    wallet = relationship("Wallet", back_populates="owner", uselist=False)
    contributions = relationship("Contribution", back_populates="user")
    pools = relationship("Pool", secondary=user_pool_association, back_populates="participants")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)
    timestamp = Column(DateTime)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    wallet = relationship("Wallet", back_populates="transactions")

class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    goal_amount = Column(Float)
    current_amount = Column(Float, default=0.0)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    contributions = relationship("Contribution", back_populates="sprint")


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime)
    sprint_id = Column(Integer, ForeignKey("sprints.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    sprint = relationship("Sprint", back_populates="contributions")
    user = relationship("User", back_populates="contributions")

class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_amount = Column(Float)
    participants = relationship("User", secondary=user_pool_association, back_populates="pools")
