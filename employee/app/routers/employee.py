from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.service.employee import create_employee, get_employees, get_employee_by_id_db, get_employee_cedula, get_employee_place, update_employee, delete_employee
from app.shared.utils import verify_token

router = APIRouter(prefix="/employee", tags=["employee"])


# Crear un nuevo empleado
@router.post("/", response_model=EmployeeResponse,dependencies=[Depends(verify_token)])
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)

# Obtener todos los empleados
@router.get("/", response_model=list[EmployeeResponse],dependencies=[Depends(verify_token)])
def get_all_employees(db: Session = Depends(get_db)):
    return get_employees(db)

# Obtener un empleado por ID
@router.get("/{id}", response_model=EmployeeResponse,dependencies=[Depends(verify_token)])
def get_employee_by_id(id: int, db: Session = Depends(get_db)):
    employee = get_employee_by_id_db(db, id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

# Obtener un empleado por cedulao
@router.get("/cedula/{cedula}", response_model=EmployeeResponse,dependencies=[Depends(verify_token)])
def get_employee_by_cedula(cedula: str, db: Session = Depends(get_db)):
    employee = get_employee_cedula(db, cedula)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found by cedula")
    return employee

# Obtener empleados por place
@router.get("/place/{place_id}", response_model=list[EmployeeResponse],dependencies=[Depends(verify_token)])
def get_employee_by_place(place_id: int, db: Session = Depends(get_db)):
    employee = get_employee_place(db, place_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found by place")
    return employee

# Actualizar un empleado existente
@router.put("/{id}", response_model=EmployeeResponse,dependencies=[Depends(verify_token)])
def update_employee_by_id(id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    return update_employee(db, id, employee_update)

# Eliminar un empleado
@router.delete("/{id}",dependencies=[Depends(verify_token)])
def delete_employee_by_id(id: int, db: Session = Depends(get_db)):
    delete_employee(db, id)
    return {"message": "Employee deleted successfully"}
