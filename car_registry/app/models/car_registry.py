from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Car_Register(Base):
    __tablename__ = "car_register"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False)
    even_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car = relationship("Car", back_populates="car_register")


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car_register = relationship("Car_Register", back_populates="car")

