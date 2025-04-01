from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import os
import logging

from .routes import cart, products
from .database import get_db
from .schemas import *

logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# Used for Image Upload
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/images")) # To insure that we are getting abs path for differet systems
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")
# Include the routes
app.include_router(cart.router)
app.include_router(products.router)

# Corrected CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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

@app.post("/login/", status_code=status.HTTP_200_OK, response_model=None)
def login(user: UserLogin, db=Depends(get_db)):  # db is a tuple (cursor, conn)
    try:
        cursor, conn = db  # Unpack the tuple here

        # Retrieve the user from the database
        cursor.execute(f"""SELECT *
                           FROM users
                           WHERE username = '{user.username}' AND password = '{user.password}'""")
        user = cursor.fetchone()  # Get the user as a tuple
        if user:
            print(user)

        # Check if user exists and passwords match
        if user is None:
            return HTTPException(status_code=401, detail="Invalid credentials")

        # Return success response
        return {"message": "Login successful"}

    except Exception as e:
        # Log the error (optional)
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
