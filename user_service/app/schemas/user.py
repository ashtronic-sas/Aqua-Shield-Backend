from typing import Optional
from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    created_at : Optional[datetime.datetime]  = None
    updated_at : Optional[datetime.datetime]  = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at : Optional[datetime.datetime]  = None
    updated_at : Optional[datetime.datetime]  = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

from pydantic import BaseModel
from typing import Dict

class UserResponse(BaseModel):
    access_token: str
    token_type: str
    message: str
    user: Dict[str, str]
