from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CarCreate(BaseModel):
    id: int
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
    create_at: datetime
    update_at: datetime

class CarUpdate(BaseModel):
    license_plate: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    owner_id: Optional[int]

    class Config:
        orm_mode = True