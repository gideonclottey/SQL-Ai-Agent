from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class AppUser(Base):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Sample dataset for querying (what the agent will SELECT from)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    age = Column(Integer)
    location = Column(String)
    signup_date = Column(Date)
    last_login = Column(DateTime)
    job_industry = Column(String)
    activities = relationship("UserActivity", back_populates="user")

class UserActivity(Base):
    __tablename__ = "user_activity"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_date = Column(Date, nullable=False)
    activity_type = Column(String, nullable=False)

    user = relationship("User", back_populates="activities")