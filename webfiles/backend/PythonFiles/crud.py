# crud.py
import psycopg2
from passlib.context import CryptContext
from database import get_db
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)  # Set log level to debug

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(cursor, username: str):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()  # Get the user as a tuple
    if user:
        return user  # Return the user as a tuple
    return None

def register_user(cursor, username: str, password: str, email: str, role: str):
    # Here, insert the user and commit the transaction
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)", 
                   (username, password, email, role))
    cursor.connection.commit()  # Commit the transaction
    return None  # Return None instead of the inserted user

def get_products(cursor):
    cursor.execute("SELECT sku, name, description, price, stock, category, img FROM products")
    products = cursor.fetchall()  # Get all products as tuples
    return products  # Return as a list of tuples, not dictionaries
   

def get_product_by_sku(cursor, sku: str):
    cursor.execute("SELECT sku, name, description, price, stock, category, img FROM products WHERE sku = %s", (sku,))
    product = cursor.fetchone()  # Get the product as a tuple
    if product:
        return product  # Return the product as a tuple
    return None