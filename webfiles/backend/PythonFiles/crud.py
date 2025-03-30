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
        return {
            "username": user[0],
            "password": user[1],
            "email": user[2],
            "role": user[3]
        }
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
    return [
        {
            "sku": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "stock": product[4],
            "category": product[5],
            "img": product[6]
        }
        for product in products
    ]

def get_product_by_sku(cursor, sku: str):
    cursor.execute("SELECT sku, name, description, price, stock, category, img FROM products WHERE sku = %s", (sku,))
    product = cursor.fetchone()  # Get the product as a tuple
    if product:
        return {
            "sku": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "stock": product[4],
            "category": product[5],
            "img": product[6]
        }
    return None