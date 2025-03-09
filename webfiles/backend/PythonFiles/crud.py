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

def create_user(cursor, conn, username: str, password: str, email: str):
    debug.log("inserting into db");
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s), username", 
                   (username, password, email))  # Store password as plain text
    conn.commit()
    return cursor.fetchone()