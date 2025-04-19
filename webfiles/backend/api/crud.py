from passlib.context import CryptContext
from fastapi import UploadFile
import logging
import os

UPLOAD_DIR = "../../frontend/src/images"  # Directory where images are stored //realitive to Python files (fast api root)

logging.basicConfig(level=logging.DEBUG)  # Set log level to debug

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


def search_products_by_query(query: str, db):
    cursor, conn = db

    # Execute the query with the search string
    cursor.execute("""
        SELECT sku, name, description, price, stock, img
        FROM products
        WHERE name ILIKE %s OR description ILIKE %s
        LIMIT 50;
    """, (f"%{query}%", f"%{query}%"))

    results = cursor.fetchall()
    

    return results