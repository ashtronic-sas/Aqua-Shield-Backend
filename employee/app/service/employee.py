from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.employee import Employee, EmployeePlace, Place
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

# Crear un nuevo empleado
def create_employee(db: Session, employee: EmployeeCreate):
    #crete employee
    place_id= employee.place_id
    employee_dict= employee.dict()
    employee_dict.pop("place_id",None)
    db_employee = Employee(**employee_dict)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # create employee_place asociado

    # Verificar si el place_id existe en la tabla place
    place = db.query(Place).filter(Place.id == place_id).first()
    # Verificar si la combinación de employee_id y place_id ya existe en la tabla employee_place
    existing_employee_place = db.query(EmployeePlace).filter(
        EmployeePlace.employee_id == db_employee.id,
        EmployeePlace.place_id == place_id
    ).first()

    if place is None:
        raise HTTPException(status_code=400, detail="Place ID does not exist")
    db_employee_place = EmployeePlace(
        employee_id=db_employee.id,
        place_id=place_id
    )
    db.add(db_employee_place)
    db.commit()
    db.refresh(db_employee_place)
    return {"employee":db_employee , "employee_place": db_employee_place}

# Obtener todos los empleados
def get_employees(db: Session):
    return db.query(Employee).all()

# Obtener empleado por ID
def get_employee_by_id_db(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

# Obtener empleado por cedulao
def get_employee_cedula(db: Session, employee_cedula: str):
    return db.query(Employee).filter(Employee.cedula == employee_cedula).first()

# Obtener empleados por place
def get_employee_place(db: Session, place_id: int):
    # Obtener los employee_id asociados al place_id en EmployeePlace
    return db.query(Employee).join(EmployeePlace, Employee.id == EmployeePlace.employee_id).filter(EmployeePlace.place_id == place_id).all()

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
