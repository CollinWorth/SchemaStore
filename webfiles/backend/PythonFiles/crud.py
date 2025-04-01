# crud.py
import psycopg2
from passlib.context import CryptContext
from database import get_db
from fastapi import HTTPException, UploadFile
import logging
import os

UPLOAD_DIR = "../../frontend/src/images"  # Directory where images are stored //realitive to Python files (fast api root)

logging.basicConfig(level=logging.DEBUG)  # Set log level to debug

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(cursor, username: str):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()  # Get the user as a tuple
    if user:
        return user  # Return the user as a tuple
    return None

def register_user(cursor, username: str, password: str, email: str, role_id: int):
    # Here, insert the user and commit the transaction
    cursor.execute("INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)", 
                   (username, password, email, role_id))
    cursor.connection.commit()  # Commit the transaction
    return None  # Return None instead of the inserted user

def get_products(cursor):
    cursor.execute("SELECT sku, name, description, price, stock, img FROM products")
    products = cursor.fetchall()  # Get all products as tuples
    return products  # Return as a list of tuples, not dictionaries
   

def get_product_by_sku(cursor, sku: str):
    cursor.execute("SELECT sku, name, description, price, stock, img FROM products WHERE sku = %s", (sku,))
    product = cursor.fetchone()  # Get the product as a tuple
    if product:
        return product  # Return the product as a tuple
    return None

################################## Images ################################
def save_image(file: UploadFile, sku: str) -> str:
    """Save the uploaded image file and return its path."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure directory exists
    file_path = os.path.join(UPLOAD_DIR, f"{sku}.png")  # Save as SKU.png
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())  # Save the file
    
    return file_path  # Return path to store in database
##########################################################################

def register_product(cursor, sku: str, name: str, description: str, price: float, stock: int, file: UploadFile):
    """Register a new product and save its image as a file."""
    img_path = save_image(file, sku)  # Save image and get path
    cursor.execute(
        "INSERT INTO products (sku, name, description, price, stock, img) VALUES (%s, %s, %s, %s, %s, %s)",
        (sku, name, description, price, stock, img_path)
    )
    cursor.connection.commit()