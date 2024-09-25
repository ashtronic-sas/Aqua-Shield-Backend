from sqlalchemy import Column, Integer, String, DateTime,func
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())






