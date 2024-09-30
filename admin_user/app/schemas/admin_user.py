from typing import Optional
from pydantic import BaseModel,EmailStr,validator, ValidationError
from typing import Dict
import datetime

class UserCreate(BaseModel):

    username: str
    password: str
    created_at : Optional[datetime.datetime]  = None
    updated_at : Optional[datetime.datetime]  = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "string",
                "email": "string",
                "password": "string",
            }
    }

class AdminUserUpdate(BaseModel):

    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    first_last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    documento: Optional[str] = None
    photo: Optional[str] = None
    

class AdminUserCreate(BaseModel):

    username: str
    password: str
    email: EmailStr
    first_name: str
    second_name: Optional[str]| None
    first_last_name: str
    second_last_name: Optional[str]| None
    documento: str
    photo: Optional[str]| None

class AdminUserOut(BaseModel):
    id: int
    user_id: int
    email: str
    first_name: str
    second_name: str
    first_last_name: str
    second_last_name: str
    documento: str
    photo: str

    class Config:
        orm_mode = True



