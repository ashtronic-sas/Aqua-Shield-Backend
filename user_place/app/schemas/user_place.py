from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserPlaceCreate(BaseModel):
    user_id: int
    place_id: int

class UserPlaceResponse(BaseModel):
    id: int
    user_id: int
    place_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True