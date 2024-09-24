from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):  
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    admin_user = relationship("AdminUser", back_populates="user") 

class AdminUser(Base):  
    __tablename__ = "admin_user"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(String(100), unique=True, index=True)
    first_name  = Column(String(50))
    second_name = Column(String(50))
    first_last_name = Column(String(50))
    second_last_name = Column(String(50))
    documento = Column(String(50), unique=True)
    phote =  Column(Text)
    
    user = relationship("User", back_populates="admin_user")  



