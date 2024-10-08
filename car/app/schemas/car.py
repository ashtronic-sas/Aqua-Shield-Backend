from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CarCreate(BaseModel):
    license_plate: str
    brand: str
    model: str
    owner_id: int

class CarResponse(BaseModel):
    id: int
    license_plate: str
    brand: str
    model: str
    owner_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class CarUpdate(BaseModel):
    license_plate: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    owner_id: Optional[int]

    class Config:
        orm_mode = True