from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeRegisterCreate(BaseModel):
    employee_id: int
    place_id: int
    entry_time: datetime

class EmployeeRegisterUpdate(BaseModel):
    exit_time: Optional[datetime]

class EmployeeRegisterResponse(BaseModel):
    id: int
    employee_id: int
    place_id: int
    entry_time: datetime
    exit_time: Optional[datetime]
    hours_worked: Optional[float]

    class Config:
        orm_mode = True
