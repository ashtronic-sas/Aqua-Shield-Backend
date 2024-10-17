from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Car_Register(Base):
    __tablename__ = "car_register"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)  # Relación con Place
    #datetime = Column(DateTime(timezone=True), nullable=False)
    event_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car = relationship("Car", back_populates="car_register")
    place = relationship("Place", back_populates="car_register")


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    car_register = relationship("Car_Register", back_populates="car")
    owner = relationship("Owner", back_populates="car")

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

    car = relationship('Car', back_populates='owner')
    

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    nit = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación inversa
    car_register = relationship("Car_Register", back_populates="place")
