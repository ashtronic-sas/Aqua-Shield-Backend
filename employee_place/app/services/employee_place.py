from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import ValidationError
from app.models.employee_place import EmployeePlace, Employee, Place
from app.schemas.employee_place import EmployeePlaceCreate,EmployeePlaceResponse
from typing import List


def create_employee_place(db: Session, employee_place: EmployeePlaceCreate):
    # Verificar si el employee_id existe en la tabla employee
    employee = db.query(Employee).filter(Employee.id == employee_place.employee_id).first()
    if employee is None:
        raise HTTPException(status_code=400, detail="Employee ID does not exist")

    # Verificar si el place_id existe en la tabla place
    place = db.query(Place).filter(Place.id == employee_place.place_id).first()

    # Verificar si la combinación de employee_id y place_id ya existe en la tabla employee_place
    existing_employee_place = db.query(EmployeePlace).filter(
        EmployeePlace.employee_id == employee_place.employee_id,
        EmployeePlace.place_id == employee_place.place_id
    ).first()
    if existing_employee_place:
        raise HTTPException(status_code=400, detail="The combination of Employee ID and Place ID already exists")
    if place is None:
        raise HTTPException(status_code=400, detail="Place ID does not exist")

    db_employee_place = EmployeePlace(
        employee_id=employee_place.employee_id,
        place_id=employee_place.place_id
    )
    db.add(db_employee_place)
    db.commit()
    db.refresh(db_employee_place)
    return db_employee_place

def get_employee_place_all(db: Session) :

    db_employee_place = db.query(EmployeePlace).all()

    if db_employee_place is None:
        raise HTTPException(status_code=404, detail="EmployeePlace not found")  
    
    return db_employee_place


def get_employee_place_all_by_id_db(db: Session, employee_id: int):
    db_employee_place = db.query(EmployeePlace).filter(EmployeePlace.employee_id == employee_id).all()
    if db_employee_place is None:
        raise HTTPException(status_code=404, detail="EmployeePlace not found")
    return db_employee_place

def delete_employee_place_db(db: Session, employee_id: int, place_id: int):
    db_employee_place = db.query(EmployeePlace).filter(EmployeePlace.employee_id == employee_id, EmployeePlace.place_id == place_id).first()
    if db_employee_place is None:
        raise HTTPException(status_code=404, detail="EmployeePlace not found")
    db.delete(db_employee_place)
    db.commit()
    return {"message": "EmployeePlace deleted"}
