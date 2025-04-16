from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..database import get_db
from ..crud import register_user, login_user
from ..schemas import UserCreate, UserOut, UserLogin
from ..authentication import oauth2_scheme, User, Token, TokenData, create_access_token, authenticate_user, credentials_exception, get_current_active_user

router = APIRouter(
   prefix="/user",
   tags=["user"]
)

@router.get("/auth/", status_code=status.HTTP_200_OK, response_model=Token)
async def auth_test(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
   user = authenticate_user(form_data.username, form_data.password)
   if not user:
      raise credentials_exception
   access_token = create_access_token(data={"sub": user.username})
   return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", status_code=status.HTTP_200_OK, response_model=User)
async def get_me(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
   return get_current_active_user(token=token, db=db)

@router.post("/register/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def register_user(user: UserCreate, db=Depends(get_db)):
   cursor, conn = db
   # check if user already exists
   cursor.execute(f"SELECT * FROM USERS WHERE username = '{user.username}'")
   existing_user = cursor.fetchone()
   if existing_user:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
   # register user
   cursor.execute(f"INSERT INTO USERS (username, password, email, role_id) VALUES ('{user.username}', '{user.password}', '{user.email}', {user.role_id})")
   cursor.connection.commit()
   return
