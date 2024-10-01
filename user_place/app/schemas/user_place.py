from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserPlaceCreate(BaseModel):
    user_id: int
    place_id: int
    access_level: str

class UserPlaceResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    access_level: str
    assigned_at: datetime

    class Config:
        orm_mode = True