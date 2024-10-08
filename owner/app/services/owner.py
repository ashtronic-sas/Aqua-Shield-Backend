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
    return db.query(Owner).filter(Owner.id == owner_id).first()

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
