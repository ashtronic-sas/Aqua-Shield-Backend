from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

# Crear un nuevo empleado
def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Obtener todos los empleados
def get_employees(db: Session):
    return db.query(Employee).all()

# Obtener empleado por ID
def get_employee_by_id_db(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

# Obtener empleado por documento
def get_employee_document(db: Session, employee_document: str):
    return db.query(Employee).filter(Employee.document == employee_document).first()

# Actualizar un empleado existente
def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = get_employee_by_id_db(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee_update.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

# Eliminar un empleado
def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id_db(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    try:
        db.delete(db_employee)
        db.commit()
    except Exception as e:
        db.rollback()
        if "foreign key constraint fails" in str(e):
            raise HTTPException(status_code=400, detail="Cannot delete employee due to existing foreign key constraints")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
