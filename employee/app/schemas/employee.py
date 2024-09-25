from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeCreate(BaseModel):
    name: str
    document: str
    phone: str

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    document: Optional[str]
    phone: Optional[str]

class EmployeeResponse(BaseModel):
    id: int
    name: str
    document: str
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
