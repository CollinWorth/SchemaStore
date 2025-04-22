from pydantic import BaseModel
from typing import Optional, List, Dict
import datetime


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

class OrderItem(BaseModel):
    product_sku: str
    amount: int

class OrderCreate(BaseModel):
    username: str
    products: List[OrderItem] # List of products with their amounts
    ship_address: str

class OrderUpdate(BaseModel):
    username: Optional[str] = None
    product_add: Optional[List[OrderItem]] = None
    product_remove: Optional[List[OrderItem]] = None
    ship_address: Optional[str] = None

class OrderOut(BaseModel):
    order_num: int
    username: str
    products: List[OrderItem]
    ship_address: str
    total: float
    create_at: datetime.datetime
