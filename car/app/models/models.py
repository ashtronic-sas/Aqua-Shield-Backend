from sqlalchemy import Column, Integer, ForeignKey, String,DateTime, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(50), unique=True, nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car_register = relationship("Car_Register", back_populates="car")
    owner = relationship("Owner", back_populates="cars")


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

    cars = relationship("Car", back_populates="owner")

class Car_Register(Base):
    __tablename__ = "car_register"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    even_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car = relationship("Car", back_populates="car_register")