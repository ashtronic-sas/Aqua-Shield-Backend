from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.owner import OwnerCreate, OwnerUpdate, OwnerResponse
from app.services.owner import create_owner, get_owners, get_owner_by_id, update_owner, delete_owner
from app.shared.utils import verify_token

router = APIRouter(prefix="/owner", tags=["Owner"])

# Crear un nuevo propietario
@router.post("/", response_model=OwnerResponse, dependencies=[Depends(verify_token)])
def create_new_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    return create_owner(db, owner)

# Obtener todos los propietarios
@router.get("/", response_model=list[OwnerResponse], dependencies=[Depends(verify_token)])
def get_all_owners(db: Session = Depends(get_db)):
    return get_owners(db)

# Obtener un propietario por ID
@router.get("/{id}", response_model=OwnerResponse, dependencies=[Depends(verify_token)])
def get_owner_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    owner = get_owner_by_id(db, id)
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return owner

# Actualizar un propietario existente
@router.put("/{id}", response_model=OwnerResponse, dependencies=[Depends(verify_token)])
def update_owner_endpoint(id: int, owner_update: OwnerUpdate, db: Session = Depends(get_db)):
    return update_owner(db, id, owner_update)

# Eliminar un propietario
@router.delete("/{id}", dependencies=[Depends(verify_token)])
def delete_owner_endpoint(id: int, db: Session = Depends(get_db)):
    delete_owner(db, id)
    return {"message": "Owner deleted successfully"}
