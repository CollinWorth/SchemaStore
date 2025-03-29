# To help with user authentication 
import psycopg2
from passlib.context import CryptContext
from database import get_db
from passlib.context import CryptContext
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)  # Set log level to debug

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(cursor, username: str):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

def create_user(cursor, conn, username: str, password: str, email: str, role: str):
    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)", 
                   (username, password, email, role))  
    conn.commit()
    return cursor.fetchone()