from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeCreate(BaseModel):

    first_name: str
    second_name: Optional[str]
    last_name: str
    second_last_name: Optional[str]
    cedula: str
    photo   : Optional[str]
    phone: str
    place_id: int





class EmployeeUpdate(BaseModel):

    first_name:  Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    second_last_name: Optional[str]
    cedula:  Optional[str]
    photo   : Optional[str]
    cedula:  Optional[str]
    phone:  Optional[str]
    cedula: Optional[str]
    phone: Optional[str]

class EmployeeResponse(BaseModel):

    id: Optional[int]
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    second_last_name: Optional[str]
    photo   : Optional[str]
    cedula: Optional[str]
    phone: Optional[str]
    cedula: Optional[str]
    phone: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

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
class EmployeeResponse_with_EmployeePlace(BaseModel):
    employee: EmployeeResponse
    employee_place: EmployeePlaceResponse