from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeePlaceCreate(BaseModel):
    employee_id: int
    place_id: int

    class Config:
        orm_mode = True  

class EmployeePlaceResponse(BaseModel):
    
    id: int
    employee_id: int
    place_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True