from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
import crud
import schemas
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
@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, cursor=Depends(get_db)):
    role = user.role if user.role else "customer"  # Default to "customer" if role is not provided
    new_user = crud.create_user(cursor[0], cursor[1], user.username, user.password, user.email, role)
    return {"message": "Register successful"}

# Login route
@app.post("/login/")
def login(user: schemas.UserLogin, cursor=Depends(get_db)):  # Use UserLogin instead of UserCreate
    db_user = crud.get_user(cursor, user.username)
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


# Get all products
@app.get("/products/", response_model=list[schemas.ProductOut])
def get_all_products(cursor=Depends(get_db)):
    products = crud.get_products(cursor[0])
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    return [
        schemas.ProductOut(
            sku=prod[0], 
            name=prod[1], 
            description=prod[2], 
            price=prod[3], 
            stock=prod[4], 
            category=prod[5], 
            img=prod[6]
        ) for prod in products
    ]

# Get a single product by SKU
@app.get("/products/{sku}", response_model=schemas.ProductOut)
def get_product(sku: str, cursor=Depends(get_db)):
    product = crud.get_product_by_sku(cursor[0], sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return schemas.ProductOut(
        sku=product[0], 
        name=product[1], 
        description=product[2], 
        price=product[3], 
        stock=product[4], 
        category=product[5], 
        img=product[6]
    )