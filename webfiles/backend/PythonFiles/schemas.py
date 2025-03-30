from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role: str | None = None

class UserOut(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: float
    stock: int
    category: str | None = None

class ProductOut(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: float
    stock: int
    category: str | None = None
    img: bytes | None = None

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

class ProductOrderCreate(BaseModel):
    username: str
    product_sku: str
    amount: int
    ship_addr: str
    total: float

class ProductOrderOut(BaseModel):
    username: str
    product_sku: str
    amount: int
    ship_addr: str
    total: float

    class Config:
        orm_mode = True
