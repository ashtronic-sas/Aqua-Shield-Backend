from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.car_registry import Car_Register
from app.schemas.car_registry import CarRegistryCreate, CarRegistryResponse

def create_car_registry_db(db: Session, car: CarRegistryCreate):
    db_car = Car_Register(
        car_id=car.car_id,
        even_type=car.even_type
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def update_car_registry_db(db: Session, car_id: int, car: CarRegistryCreate):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_car.car_id = car.car_id
    db_car.even_type = car.even_type
    db.commit()
    db.refresh(db_car)
    return db_car

def get_car_registry_by_id_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

def get_car_registry_by_car_id_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.car_id == car_id).all()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

def delete_car_registry_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}


