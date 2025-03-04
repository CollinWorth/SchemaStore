from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PythonFiles.database import get_db
import PythonFiles.crud
import PythonFiles.schemas
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Corrected CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",# Only allow frontend origin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route
@app.post("/register/", response_model=PythonFiles.schemas.UserOut)
def register_user(user: PythonFiles.schemas.UserCreate, cursor=Depends(get_db)):
    db_user = PythonFiles.crud.get_user(cursor, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(cursor[0], cursor[1], user.username, user.password)
    return new_user

# Login route
@app.post("/login/")
def login(user: PythonFiles.schemas.UserCreate, cursor=Depends(get_db)):
    db_user = PythonFiles.crud.get_user(cursor, user.username)
    print("Found user:", db_user)  # This should print in FastAPI logs
    if db_user is None or db_user['password'] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# Handle CORS Preflight Requests
@app.options("/{full_path:path}")
async def preflight_check(full_path: str):
    response = JSONResponse(content={"message": "CORS preflight successful"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response