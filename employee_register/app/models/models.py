from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, func,String
from sqlalchemy.orm import relationship
from app.config.database import Base

class EmployeeRegister(Base):
    __tablename__ = "employee_registers"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)  # Relación con Employee
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)  # Relación con Place
    entry_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    hours_worked = Column(Float, nullable=True)

    # Relaciones
    employee = relationship("Employee", back_populates="employee_registers")
    place = relationship("Place", back_populates="employee_registers")  # Relación con Place

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    nit = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación con UserPlace
    user_places = relationship("UserPlace", back_populates="place")
    employee_places = relationship("EmployeePlace", back_populates="place")

    # Relación con EmployeeRegister
    employee_registers = relationship("EmployeeRegister", back_populates="place")

class UserPlace(Base):
    __tablename__ = "user_places"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    access_level = Column(String(50), nullable=False)

    user = relationship("User", back_populates="user_places")
    place = relationship("Place", back_populates="user_places")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Contraseña encriptada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación con UserPlace
    user_places = relationship("UserPlace", back_populates="user")