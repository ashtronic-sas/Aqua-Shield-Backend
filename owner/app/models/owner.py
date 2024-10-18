from sqlalchemy import Column, Integer, String, DateTime, func,ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    first_lastname = Column(String(100), nullable=False)
    second_lastname = Column(String(100), nullable=True)
    cedula = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car = relationship('Car', back_populates='owner' ,cascade="all, delete")

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship('Owner', back_populates='car' ,cascade="all, delete")


