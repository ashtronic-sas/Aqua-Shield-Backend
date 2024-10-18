from sqlalchemy import Column, Integer, String, DateTime, func, Float, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config.database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    second_last_name = Column(String(255), nullable=True)
    cedula = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    photo = Column(Text, nullable=True)

    # Relación con EmployeeRegister
    employee_registers = relationship("EmployeeRegister", back_populates="employee", cascade="all, delete")

class EmployeeRegister(Base):
    __tablename__ = "employee_registers"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)  # Relación con Employee
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)  # Relación con Place

    cedula_employee = Column(String(50), nullable=False)
    photo_employee = Column(Text, nullable=False)
    date_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    event_type = Column(String(10), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    employee = relationship("Employee", back_populates="employee_registers", cascade="all, delete")
    place = relationship("Place", back_populates="employee_registers", cascade="all, delete")  

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    nit = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación con EmployeeRegister
    employee_registers = relationship("EmployeeRegister", back_populates="place", cascade="all, delete")
