from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    item_name: str
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    item_name: str
    quantity: int

    class Config:
        orm_mode = True



