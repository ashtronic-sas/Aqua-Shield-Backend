from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate

# Crear un nuevo propietario
def create_owner(db: Session, owner: OwnerCreate):
    # Verificar que la cédula sea única
    existing_owner = db.query(Owner).filter(Owner.cedula == owner.cedula).first()
    if existing_owner:
        raise HTTPException(status_code=400, detail="Owner with this cedula already exists")
    
    db_owner = Owner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

# Obtener todos los propietarios
def get_owners(db: Session):
    return db.query(Owner).all()

# Obtener propietario por ID
def get_owner_by_id(db: Session, owner_id: int):
    owner= db.query(Owner).filter(Owner.id == owner_id).options(joinedload(Owner.car)).first()
    return {
        "id": owner.id,
        "first_name": owner.first_name,
        "second_name": owner.second_name,
        "first_lastname": owner.first_lastname,
        "second_lastname": owner.second_lastname,
        "cedula": owner.cedula,
        "created_at": owner.created_at,
        "updated_at": owner.updated_at,
        # Construir la lista de carros asociados
        "cars": [
            {
                "id": car.id,
                "license_plate": car.license_plate,
                "brand": car.brand,
                "model": car.model,
                "owner_id": car.owner_id,
                "created_at": car.created_at,
                "updated_at": car.updated_at
            }
            for car in owner.car  # Recorre la relación de carros
        ]
    }

# Obtener propietario por document
def get_owner_by_cedula(db: Session, owner_cedula: int):
    owner = (
        db.query(Owner)
        .filter(Owner.cedula == owner_cedula)
        .options(joinedload(Owner.car))  # Cargar los carros relacionados
        .first()
    )
    return {
        "id": owner.id,
        "first_name": owner.first_name,
        "second_name": owner.second_name,
        "first_lastname": owner.first_lastname,
        "second_lastname": owner.second_lastname,
        "cedula": owner.cedula,
        "created_at": owner.created_at,
        "updated_at": owner.updated_at,
        # Construir la lista de carros asociados
        "cars": [
            {
                "id": car.id,
                "license_plate": car.license_plate,
                "brand": car.brand,
                "model": car.model,
                "owner_id": car.owner_id,
                "created_at": car.created_at,
                "updated_at": car.updated_at
            }
            for car in owner.car  # Recorre la relación de carros
        ]
    }

# Actualizar un propietario existente
def update_owner(db: Session, owner_id: int, owner_update: OwnerUpdate):
    db_owner = get_owner_by_id(db, owner_id)
    if not db_owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    for key, value in owner_update.dict(exclude_unset=True).items():
        setattr(db_owner, key, value)

    db.commit()
    db.refresh(db_owner)
    return db_owner

# Eliminar un propietario
def delete_owner(db: Session, owner_id: int):
    db_owner = get_owner_by_id(db, owner_id)
    if not db_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    db.delete(db_owner)
    db.commit()
