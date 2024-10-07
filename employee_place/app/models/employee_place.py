from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint,ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación inversa
    employee_places = relationship("EmployeePlace", back_populates="employee")

class EmployeePlace(Base):
    __tablename__ = "employee_places"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    employee = relationship("Employee", back_populates="employee_places")
    place = relationship("Place", back_populates="employee_places")

    # Validación de duplicados
    __table_args__ = (UniqueConstraint('employee_id', 'place_id', name='_employee_place_uc'),)


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    nit = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación inversa
    employee_places = relationship("EmployeePlace", back_populates="place")