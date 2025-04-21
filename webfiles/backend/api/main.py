from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import os
import logging

from .routes import cart, products, user
from .database import get_db
from .schemas import *

logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",  # Also valid sometimes depending on browser
]


# Used for Image Upload
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/images")) # To insure that we are getting abs path for differet systems
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")
# Include the routes
app.include_router(cart.router)
app.include_router(products.router)
app.include_router(user.router)

# Corrected CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db=Depends(get_db)):  # Unpack db into cursor and conn
    cursor, conn = db  # Unpack the tuple into cursor and conn
    # Register the user in the database
    cursor.execute(f"INSERT INTO users (username, password, email, role_id) VALUES ('{user.username}', '{user.password}', '{user.email}', {user.role_id})")
    cursor.connection.commit()  # Commit the transaction
    # Get role name
    statement = f"""SELECT roles.user_role
                    FROM roles JOIN users ON roles.id = users.role_id
                    WHERE users.username = '{user.username}'"""
    cursor.execute(statement)
    role = cursor.fetchone()[0]
    # Return User
    return UserOut(username=user.username, email=user.email, role=role)

@app.post("/login/", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db=Depends(get_db)):
    try:
        cursor, conn = db

        # Use parameterized query to prevent SQL injection
        cursor.execute(
            """SELECT username FROM users WHERE username = %s AND password = %s""",
            (user.username, user.password)
        )
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return the username so frontend can store it
        return {"username": result[0], "message": "Login successful"}

    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Handle CORS Preflight Requests
@app.options("/{full_path:path}")
async def preflight_check(full_path: str):
    response = JSONResponse(content={"message": "CORS preflight successful"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

