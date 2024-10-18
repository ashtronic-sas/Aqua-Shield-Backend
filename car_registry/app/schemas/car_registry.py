from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CarRegistryCreate(BaseModel):

    car_id: int
    date_time: datetime
    place_id: int
    event_type: str

class CarRegistryResponse(BaseModel):
    
    id: int
    car_id: int
    date_time: datetime
    place_id: int
    event_type: str
    created_at  = datetime
    updated_at = datetime

class CarRegistryUpdate(BaseModel):

    car_id: Optional[int]
    date_time: Optional[datetime]
    place_id: int
    event_type: Optional[str]

class PlaceResponse(BaseModel):
    id: int
    name: str
    address: str
    nit: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CarRegistryResponseCar_id(BaseModel):
    
    id: int
    car_id: int
    date_time: datetime
    place: PlaceResponse
    event_type: str
    created_at  = datetime
    updated_at = datetime
    class Config:
        orm_mode = True


class CarResponse(BaseModel):
    id: int
    license_plate: str
    brand: str
    model: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
class CarRegistryResponsePlace_id(BaseModel):
    
    id: int
    car: CarResponse
    date_time: datetime
    place_id: int 
    event_type: str
    created_at  = datetime
    updated_at = datetime
    class Config:
        orm_mode = True
class CarRegistryResponse_id(BaseModel):
    id: int
    date_time: datetime
    event_type: str
    created_at: datetime
    updated_at: datetime
    car: CarResponse  # Anidamos el esquema CarResponse completo
    place: PlaceResponse  # Anidamos el esquema PlaceResponse completo

    class Config:
        orm_mode = True