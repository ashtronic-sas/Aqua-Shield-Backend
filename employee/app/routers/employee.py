from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.service.employee import create_employee, get_employees, get_employee_by_id, update_employee, delete_employee
from app.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/employee", tags=["employee"])

# Define the OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

# Crear un nuevo empleado
@router.post("/", response_model=EmployeeResponse)
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return create_employee(db, employee)

# Obtener todos los empleados
@router.get("/employee", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return get_employees(db)

# Obtener un empleado por ID
@router.get("/{id}", response_model=EmployeeResponse)
def get_employee_by_id(id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    employee = get_employee_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

# Actualizar un empleado existente
@router.put("/{id}", response_model=EmployeeResponse)
def update_employee_by_id(id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return update_employee(db, id, employee_update)

# Eliminar un empleado
@router.delete("/{id}")
def delete_employee_by_id(id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    delete_employee(db, id)
    return {"message": "Employee deleted successfully"}
