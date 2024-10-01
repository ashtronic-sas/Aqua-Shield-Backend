from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Car
from app.schemas.car import CarCreate, CarResponse, CarUpdate

# Función para crear un carro
def create_car_db(db: Session, car: CarCreate):

    db_car = Car(
        license_plate=car.license_plate,
        brand=car.brand,
        model=car.model,
        owner_id=car.owner_id
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car   

# Función para obtener todos los carros
def get_all_car_db(db: Session):
    return db.query(Car).all()

# Función para obtener un carro por su id
def get__car_by_id_db(db: Session, id: int):
    car = db.query(Car).filter(Car.id == id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# Función para actualizar un carro por su id
def update_car_by_id_db(db: Session, id: int, car_update: CarCreate):

    car = db.query(Car).filter(Car.id == id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    # Update only the fields that are provided
    if car_update.license_plate is not None:
        car.license_plate = car_update.license_plate
    if car_update.brand is not None:
        car.brand = car_update.brand
    if car_update.model is not None:
        car.model = car_update.model
    if car_update.owner_id is not None:
        car.owner_id = car_update.owner_id

    db.commit()
    db.refresh(car)

    return car

# Función para eliminar un carro por su id
def delete_car_by_id_db(db: Session, id: int):

    car = db.query(Car).filter(Car.id == id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}
