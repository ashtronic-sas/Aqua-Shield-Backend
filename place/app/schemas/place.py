from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema para crear una nueva Place
class PlaceCreate(BaseModel):
    name: str
    address: str
    nit: Optional[str] = None

# Esquema para actualizar una Place existente
class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    nit: Optional[str] = None

# Esquema para la respuesta de Place
class PlaceResponse(BaseModel):
    id: int
    name: str
    address: str
    nit: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True