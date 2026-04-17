from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from database import Base


# SQLAlchemy ORM model
class GoalDB(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(Date, nullable=True)
    plan = Column(Text, nullable=True)


# Pydantic schemas
class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    plan: Optional[str] = None

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    plan: Optional[str] = None

class GoalResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    due_date: Optional[date]
    plan: Optional[str]

    class Config:
        from_attributes = True
