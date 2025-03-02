from fastapi import FastAPI, Depends, HTTPException
from database import get_db
import crud, schemas
from passlib.context import CryptContext

app = FastAPI()

# Register
@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, cursor=Depends(get_db)):
    db_user = crud.get_user(cursor, user.username)
    if db_user:
        #
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(cursor[0], cursor[1], user.username, user.password)
    return new_user

# Login
@app.post("/login/")
def login(user: schemas.UserCreate, cursor=Depends(get_db)):
    db_user = crud.get_user(cursor, user.username)
    if db_user is None or not pwd_context.verify(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}