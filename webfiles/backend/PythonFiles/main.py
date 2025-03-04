from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PythonFiles.database import get_db
import PythonFiles.crud
import PythonFiles.schemas


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000"
    "http://localhost:3000/$%7BAPI_URL/login/"
    ],  # Adjust to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Register
@app.post("/register/", response_model=PythonFiles.schemas.UserOut)
def register_user(user: PythonFiles.schemas.UserCreate, cursor=Depends(get_db)):
    db_user = crud.get_user(cursor, user.username) # Will be set to NULL if the 
    if db_user:
        #
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(cursor[0], cursor[1], user.username, user.password)
    return new_user

# Login
@app.post("/login/")
def login(user: PythonFiles.schemas.UserCreate, cursor=Depends(get_db)):
    db_user = crud.get_user(cursor, user.username)
    print("Found user:", db_user) 
    if db_user is None or not pwd_context.verify(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}