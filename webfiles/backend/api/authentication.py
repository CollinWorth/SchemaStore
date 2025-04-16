from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

from .database import get_db

SECRET_KEY = "aad5deb677ebcbacc797c1482be159f6b8cecfaec52c553b9667c48784baa3cd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(
   status_code=status.HTTP_401_UNAUTHORIZED,
   detail="Could not validate credentials",
   headers={"WWW-Authenticate": "Bearer"},
)

class User(BaseModel):
   username: str
   email: Optional[str] = None
   role: str
   active: bool

class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   username: str

def authenticate_user(username: str, password: str, db=Depends(get_db)):
   hashed_password = pwd_context.hash(password)
   cursor, conn = db
   cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
   user = cursor.fetchone()
   if user:
      return User(username=user[0], email=user[2], role=user[3])
   return None

def create_access_token(data: dict, expires_delta: int = None):
   to_encode = data.copy()
   if expires_delta:
      expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
   else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt

async def get_current_active_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("sub")
      if username is None:
         raise credentials_exception
      token_data = TokenData(username=username)
   except InvalidTokenError:
      raise credentials_exception
   user = authenticate_user(token_data.username, db)
   if user is None:
      raise credentials_exception
   if not user.active:
      raise HTTPException(status_code=403, detail="Inactive user")
   return user
