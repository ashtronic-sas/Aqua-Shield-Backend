from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.car_registry import Car_Register, Place, Car
from app.schemas.car_registry import CarRegistryCreate, CarRegistryResponseCar_id

def create_car_registry_db(db: Session, car: CarRegistryCreate):
    db_car = Car_Register(
        car_id=car.car_id,
        date_time=car.date_time,  # Corrected attribute name
        place_id=car.place_id,
        event_type=car.event_type
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
    if car.event_type is not None:
        db_car.event_type = car.even_type
    if car.date_time is not None:
        db_car.date_time = car.date_time
    
    db.commit()
    db.refresh(db_car)
    return db_car.__dict__

def get_car_registry_by_id_db(db: Session, id: int):
    # Obtenemos el registro del car_register
    car_register = db.query(Car_Register).filter(Car_Register.id == id).first()

    if car_register is None:
        raise HTTPException(status_code=404, detail="Car registry not found")
    
    # Obtenemos el registro de Car utilizando la relación definida en Car_Register
    car = db.query(Car).filter(Car.id == car_register.car_id).first()
    
    # Obtenemos el registro de Place utilizando la relación definida en Car_Register
    place = db.query(Place).filter(Place.id == car_register.place_id).first()
    print(place.__dict__)
    # Verificamos si los registros de car y place existen
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")

    # Retornamos la respuesta con el carro y el lugar anidados
    print(place.__dict__)
    return {
        "id": car_register.id,
        "date_time": car_register.date_time,
        "event_type": car_register.event_type,
        "created_at": car_register.created_at,
        "updated_at": car_register.updated_at,
        "car": car.__dict__,  # Anidamos el registro completo del carro
        "place": place.__dict__  # Anidamos el registro completo del lugar
    }

def get_car_registry_by_car_id_db(db: Session, car_id: int):
    db_car_registers = db.query(Car_Register).filter(Car_Register.car_id == car_id).options(joinedload(Car_Register.place)).all()
    if not db_car_registers:
        raise HTTPException(status_code=404, detail="No car register found for this car_id")
    

    # Mapeamos los registros para incluir el lugar (Place) en lugar de solo el place_id
    return [
            {
                "id": car_register.id,
                "car_id": car_register.car_id,
                "date_time": car_register.date_time,
                "event_type": car_register.event_type,
                "created_at": car_register.created_at,
                "updated_at": car_register.updated_at,
                "place": {
                    "id": car_register.place.id,
                    "name": car_register.place.name,
                    "address": car_register.place.address,
                    "nit": car_register.place.nit,
                    "created_at": car_register.place.created_at,
                    "updated_at": car_register.place.updated_at,
                }
            }
            for car_register in db_car_registers
        ]

def get_car_registry_by_place_id_db(db: Session, place_id: int):
    # Realizamos la consulta cargando también la información del carro (Car) asociado
    db_car_registers = (
        db.query(Car_Register)
        .filter(Car_Register.place_id == place_id)
        .options(joinedload(Car_Register.car))  # Carga la relación con Car
        .all()
    )

    if not db_car_registers:
        raise HTTPException(status_code=404, detail="No car register found for this place_id")

    # Mapeamos los registros para incluir el carro (Car) en lugar de solo el car_id
    return [
        {
            "id": car_register.id,
            "place_id": car_register.place_id,
            "date_time": car_register.date_time,
            "event_type": car_register.event_type,
            "created_at": car_register.created_at,
            "updated_at": car_register.updated_at,
            "car": {
                "id": car_register.car.id,
                "license_plate": car_register.car.license_plate,
                "brand": car_register.car.brand,
                "model": car_register.car.model,
                "owner_id": car_register.car.owner_id,
                "created_at": car_register.car.created_at,
                "updated_at": car_register.car.updated_at
            }
        }
        for car_register in db_car_registers
    ]


def delete_car_registry_db(db: Session, car_id: int):
    db_car = db.query(Car_Register).filter(Car_Register.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}

def get_car_all_registry_db(db: Session):

    
    db_car_registers = db.query(Car_Register).options(joinedload(Car_Register.car), joinedload(Car_Register.place)).all()

    if not db_car_registers:
        raise HTTPException(status_code=404, detail="No car register found")
    
    return [
        {
            "id": car_register.id,
            "car_id": car_register.car_id,
            "place_id": car_register.place_id,
            "date_time": car_register.date_time,
            "event_type": car_register.event_type,
            "created_at": car_register.created_at,
            "updated_at": car_register.updated_at,
            "car": {
                "id": car_register.car.id,
                "license_plate": car_register.car.license_plate,
                "brand": car_register.car.brand,
                "model": car_register.car.model,
                "owner_id": car_register.car.owner_id,
                "created_at": car_register.car.created_at,
                "updated_at": car_register.car.updated_at
            },
            "place": {
                "id": car_register.place.id,
                "name": car_register.place.name,
                "address": car_register.place.address,
                "nit": car_register.place.nit,
                "created_at": car_register.place.created_at,
                "updated_at": car_register.place.updated_at
            }
        }
        for car_register in db_car_registers
    ]
