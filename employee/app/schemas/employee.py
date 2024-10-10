from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeCreate(BaseModel):

    first_name: str
    second_name: Optional[str]
    last_name: str
    second_last_name: Optional[str]
    document: str
    photo   : Optional[str]
    document: str
    phone: str


class EmployeeUpdate(BaseModel):

    first_name:  Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    second_last_name: Optional[str]
    document:  Optional[str]
    photo   : Optional[str]
    document:  Optional[str]
    phone:  Optional[str]
    document: Optional[str]
    phone: Optional[str]

class EmployeeResponse(BaseModel):

    id: int
    first_name: str
    second_name: Optional[str]
    last_name: str
    second_last_name: Optional[str]
    document: str
    photo   : Optional[str]
    document: str
    phone: str
    document: Optional[str]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
