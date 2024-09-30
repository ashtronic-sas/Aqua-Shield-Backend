from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OwnerCreate(BaseModel):
    first_name: str
    second_name: Optional[str] = None
    first_lastname: str
    second_lastname: Optional[str] = None
    cedula: str

class OwnerUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    first_lastname: Optional[str] = None
    second_lastname: Optional[str] = None
    cedula: Optional[str] = None

class OwnerResponse(BaseModel):
    id: int
    first_name: str
    second_name: Optional[str]
    first_lastname: str
    second_lastname: Optional[str]
    cedula: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
