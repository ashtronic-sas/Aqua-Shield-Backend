from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.employee_register import EmployeeRegister
from app.schemas.employee_register import EmployeeRegisterCreate, EmployeeRegisterUpdate
from app.shared.utils import calculate_hours_worked
from datetime import datetime

# Registrar una nueva entrada
def create_employee_register(db: Session, employee_register: EmployeeRegisterCreate):
    db_employee_register = EmployeeRegister(**employee_register.dict())
    db.add(db_employee_register)
    db.commit()
    db.refresh(db_employee_register)
    return db_employee_register

# Actualizar el registro con la salida y calcular horas trabajadas
def update_employee_register(db: Session, register_id: int, update_data: EmployeeRegisterUpdate):
    db_register = db.query(EmployeeRegister).filter(EmployeeRegister.id == register_id).first()
    if not db_register:
        raise HTTPException(status_code=404, detail="EmployeeRegister not found")

    if update_data.exit_time:
        db_register.exit_time = update_data.exit_time
        db_register.hours_worked = calculate_hours_worked(db_register.entry_time, db_register.exit_time)

    db.commit()
    db.refresh(db_register)
    return db_register

# Obtener registros por empleado
def get_registers_by_employee(db: Session, employee_id: int):
    print("se entro aquí")
    return db.query(EmployeeRegister).filter(EmployeeRegister.employee_id == employee_id).all()

# Obtener registros por sede
def get_registers_by_place(db: Session, place_id: int):
    return db.query(EmployeeRegister).filter(EmployeeRegister.place_id == place_id).all()

# Obtener registros por cedula
def get_registers_by_cedula(db: Session, cedula_employee: str):
    return db.query(EmployeeRegister).filter(EmployeeRegister.cedula_employee == cedula_employee).all()

# Eliminar un registro
def delete_employee_register(db: Session, register_id: int):
    db_register = db.query(EmployeeRegister).filter(EmployeeRegister.id == register_id).first()
    if not db_register:
        raise HTTPException(status_code=404, detail="EmployeeRegister not found")
    
    db.delete(db_register)
    db.commit()
