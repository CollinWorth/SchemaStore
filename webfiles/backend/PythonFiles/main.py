from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_db
import crud
import schemas
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import base64
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/src/images")) # To insure that we are getting abs path for differet systems
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

# Corrected CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db=Depends(get_db)):  # Unpack db into cursor and conn
    cursor, conn = db  # Unpack the tuple into cursor and conn
    role_id = 3
    # Register the user in the database
    crud.register_user(cursor, user.username, user.password, user.email, role_id)
    return schemas.UserOut(username=user.username, password=user.password, email=user.email)

@app.post("/login/")
def login(user: schemas.UserLogin, db=Depends(get_db)):  # db is a tuple (cursor, conn)
    try:
        cursor, conn = db  # Unpack the tuple here

        # Retrieve the user from the database
        db_user = crud.get_user(cursor, user.username)

        # Check if user exists and passwords match
        if db_user is None or db_user[1] != user.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return success response
        return {"message": "Login successful"}

    except Exception as e:
        # Log the error (optional)
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get all products
@app.get("/products/", response_model=list[schemas.ProductOut])
def get_all_products(db=Depends(get_db)):
    cursor, conn = db
    products = crud.get_products(cursor)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    return [
        schemas.ProductOut(
            sku=prod[0], 
            name=prod[1], 
            description=prod[2], 
            price=prod[3], 
            stock=prod[4],
            img=prod[5]
        ) for prod in products
    ]

# Get a single product by SKU
@app.get("/products/{sku}", response_model=schemas.ProductOut)
def get_product(sku: str, db=Depends(get_db)):
    cursor, conn = db
    product = crud.get_product_by_sku(cursor, sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return schemas.ProductOut(
        sku=product[0], 
        name=product[1], 
        description=product[2], 
        price=product[3], 
        stock=product[4],
        img=product[5]
    )

@app.post("/products/", response_model=schemas.ProductOut)
def create_product(
    sku: str, 
    name: str, 
    description: str, 
    price: float, 
    stock: int, 
    file: UploadFile = File(...), 
    db=Depends(get_db)
):
    cursor, conn = db
    crud.register_product(cursor, sku, name, description, price, stock, file)
    return schemas.ProductOut(
        sku=sku, name=name, description=description, price=price, stock=stock, img=f"/images/{sku}.png"
    )


# Handle CORS Preflight Requests
@app.options("/{full_path:path}")
async def preflight_check(full_path: str):
    response = JSONResponse(content={"message": "CORS preflight successful"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
