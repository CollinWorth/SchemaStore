from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True