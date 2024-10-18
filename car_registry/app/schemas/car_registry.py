from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CarRegistryCreate(BaseModel):

    car_id: int
    datetime: datetime
    even_type: str
    created_at  = datetime
    updated_at = datetime

class CarRegistryResponse(BaseModel):
    
    id: int
    car_id: int
    datetime: datetime
    even_type: str
    created_at  = datetime
    updated_at = datetime

    class Config:
        orm_mode = True

class CarRegistryUpdate(BaseModel):

    car_id: Optional[int]
    datetime: Optional[datetime]
    even_type: Optional[str]
