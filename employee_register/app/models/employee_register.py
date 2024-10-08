from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, func,String,Text
from sqlalchemy.orm import relationship
from app.config.database import Base

class EmployeeRegister(Base):
    __tablename__ = "employee_registers"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)  # Relación con Employee
    cedula_employee = Column(String(50), nullable=False)
    photo_employee = Column(Text, nullable=False)
    entry_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    hours_worked = Column(Float, nullable=True)

    # Relaciones
    employee = relationship("Employee", back_populates="employee_registers")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    second_last_name = Column(String(255), nullable=True)
    document = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    photo = Column(Text, nullable=True)

    # Relación con EmployeeRegister
    employee_places = relationship("EmployeePlace", back_populates="employee")
    employee_registers = relationship("EmployeeRegister", back_populates="employee")
