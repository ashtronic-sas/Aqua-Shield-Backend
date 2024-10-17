from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeRegisterCreate(BaseModel):
    employee_id: int
    place_id: int
    cedula_employee: str
    event_type: str
    photo_employee: Optional[str]

class EmployeeRegisterUpdate(BaseModel):
    exit_time: Optional[datetime]

class EmployeeRegisterResponse(BaseModel):
    id: int
    employee_id: int
    cedula_employee: str
    place_id: int
    date_time: Optional[datetime]
    photo_employee: Optional[str]
    event_type: str
    updapte_at: Optional[datetime]
    create_at: Optional[datetime]

    class Config:
        orm_mode = True
