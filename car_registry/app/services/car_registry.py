from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.car_registry import Car_Register
from app.schemas.car_registry import CarRegistryCreate, CarRegistryResponse

def create_car_registry_db(db: Session, car: CarRegistryCreate):
    db_car = Car_Register(
        car_id=car.car_id,
        datetime=car.datetime,
        even_type=car.even_type
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car.__dict__  # Convertir el objeto a un diccionario

def update_car_registry_db(db: Session, car_id: int, car: CarRegistryCreate):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    if car.car_id is not None:
        db_car.car_id = car.car_id
    if car.even_type is not None:
        db_car.even_type = car.even_type
    if car.datetime is not None:
        db_car.datetime = car.datetime
    
    db.commit()
    db.refresh(db_car)
    return db_car.__dict__

def get_car_registry_by_id_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car.__dict__

def get_car_registry_by_car_id_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.car_id == car_id).all()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return [car.__dict__ for car in db_car]

def delete_car_registry_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}

def get_all_car_registry(db: Session):
    return db.query(Car_Register).all()