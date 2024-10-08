from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Car
from app.schemas.car import CarCreate,CarUpdate

# Función para crear un carro
def create_car_db(db: Session, car: CarCreate):
    # Check if the license plate already exists
    existing_car = db.query(Car).filter(Car.license_plate == car.license_plate).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="License plate already exists")

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
    cars = db.query(Car).all()
    if not cars:
        raise HTTPException(status_code=404, detail="No cars found")
    return cars

# Función para obtener un carro por su id
def get__car_by_id_db(db: Session, id: int):
    car = db.query(Car).filter(Car.id == id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# Función para actualizar un carro por su id
def update_car_by_id_db(db: Session, id: int, car: CarUpdate):

    db_car = db.query(Car).filter(Car.id == id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    for key, value in car.dict(exclude_unset=True).items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)

    return db_car


# Función para eliminar un carro por su id
def delete_car_by_id_db(db: Session, id: int):

    car = db.query(Car).filter(Car.id == id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}
