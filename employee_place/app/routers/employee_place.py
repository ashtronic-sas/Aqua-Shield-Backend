from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.employee_place import EmployeePlaceCreate, EmployeePlaceResponse
from app.services.employee_place import create_employee_place, get_employee_place_all, get_employee_place_by_id_db, delete_employee_place_db
from app.shared.utils import verify_token

router = APIRouter( prefix="/employee_place", tags=["Employee Place"] )


@router.get("/", response_model=list[EmployeePlaceResponse], dependencies=[Depends(verify_token)])
def get_employee_place(db: Session = Depends(get_db)):
    return get_employee_place_all(db)

@router.post("/", response_model=EmployeePlaceResponse, dependencies=[Depends(verify_token)])
def assign_employee_to_place(employee_place: EmployeePlaceCreate, db: Session = Depends(get_db)):
    return create_employee_place(db, employee_place)

@router.get("/{employee_id}", response_model=EmployeePlaceResponse, dependencies=[Depends(verify_token)])
def get_employee_place_by_id(employee_id: int, db: Session = Depends(get_db)):
    return get_employee_place_by_id_db(db, employee_id)

@router.delete("/{employee_id}/{place_id}", dependencies=[Depends(verify_token)])
def delete_employee_place(employee_id: int, place_id: int, db: Session = Depends(get_db)):
    return delete_employee_place_db(db, employee_id, place_id)




