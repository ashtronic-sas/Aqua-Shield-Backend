from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.employee_register import EmployeeRegisterCreate, EmployeeRegisterUpdate, EmployeeRegisterResponse
from app.services.employee_register import create_employee_register, update_employee_register, get_registers_by_employee, get_registers_by_place, get_registers_by_cedula, delete_employee_register
from app.shared.utils import verify_token

router = APIRouter(prefix="/employee_register", tags=["employee_register"])


# Registrar una nueva entrada de un empleado
@router.post("/", response_model=EmployeeRegisterResponse,dependencies=[Depends(verify_token)])
def register_employee_entry(employee_register: EmployeeRegisterCreate, db: Session = Depends(get_db)):
    return create_employee_register(db, employee_register)

# Actualizar el registro con la salida del empleado y calcular horas trabajadas
@router.put("/{id}", response_model=EmployeeRegisterResponse,dependencies=[Depends(verify_token)])
def update_employee(id: int, employee_register_update: EmployeeRegisterUpdate, db: Session = Depends(get_db)):
    return update_employee_register(db, id, employee_register_update)

# Obtener historial de asistencia de un empleado
@router.get("/{employee_id}", response_model=list[EmployeeRegisterResponse],dependencies=[Depends(verify_token)])
def get_employee_registers(employee_id: int, db: Session = Depends(get_db)):
    return get_registers_by_employee(db, employee_id)

# Obtener registros de asistencia en una sede
@router.get("/place/{place_id}", response_model=list[EmployeeRegisterResponse],dependencies=[Depends(verify_token)])
def get_place_registers(place_id: int, db: Session = Depends(get_db)):
    return get_registers_by_place(db, place_id)

# Obtener registros de asistencia de un empleado por cedula
@router.get("/cedula/{cedula_employee}", response_model=list[EmployeeRegisterResponse],dependencies=[Depends(verify_token)])
def get_cedula_registers(cedula_employee: str, db: Session = Depends(get_db)):
    return get_registers_by_cedula(db, cedula_employee)

# Eliminar un registro de asistencia
@router.delete("/{id}",dependencies=[Depends(verify_token)])
def delete_register(id: int, db: Session = Depends(get_db)):
    delete_employee_register(db, id)
    return {"message": "EmployeeRegister deleted successfully"}
