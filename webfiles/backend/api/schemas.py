from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None

class UserOut(BaseModel):
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: float
    stock: int
    img: str | None = None 

class ProductOut(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: float
    stock: int
    img: str | None = None 

    class Config:
        orm_mode = True

class ReservedItemCreate(BaseModel):
    username: str
    product_sku: str
    amount: int

class ReservedItemOut(BaseModel):
    username: str
    product_sku: str
    amount: int

    class Config:
        orm_mode = True

