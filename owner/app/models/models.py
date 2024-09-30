from sqlalchemy import Column, Integer, String, DateTime, func
from app.config.database import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    first_lastname = Column(String(100), nullable=False)
    second_lastname = Column(String(100), nullable=True)
    cedula = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())