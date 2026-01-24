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
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    wallet = relationship("Wallet", back_populates="owner", uselist=False)
    contributions = relationship("Contribution", back_populates="user")
    pools = relationship("Pool", secondary=user_pool_association, back_populates="participants")
    notifications = relationship("Notification", back_populates="user")
    referrals = relationship("Referral", foreign_keys="[Referral.referrer_id]", back_populates="referrer")

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

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    type = Column(String)
    read = Column(Boolean, default=False)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="notifications")

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending") # pending, complete
    reward = Column(Float, default=10.0)

    referrer = relationship("User", back_populates="referrals", foreign_keys=[referrer_id])
