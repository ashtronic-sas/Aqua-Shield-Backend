from typing import Optional
from pydantic import BaseModel,EmailStr
from typing import Dict
import datetime
from pydantic import validator, ValidationError


class UserUpdate(BaseModel):

    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "string",
                "email": "string",
                "password": "string",
            }
        }

    @validator('password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    

class UserCreate(BaseModel):

    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "string",
                "email": "string",
                "password": "string",
            }
    }
    

    @validator('password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserOut(BaseModel):
    id: int
    username: str
    created_at : Optional[datetime.datetime]  = None
    updated_at : Optional[datetime.datetime]  = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    message: str
    user: Dict[str, str]
