# To help with user authentication 
import psycopg2
from passlib.context import CryptContext
from PythonFiles.database import get_db
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(cursor, username: str):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

def create_user(cursor, conn, username: str, password: str):
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username", 
                   (username, password))  # Store password as plain text
    conn.commit()
    return cursor.fetchone()