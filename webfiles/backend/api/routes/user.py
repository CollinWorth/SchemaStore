from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from ..database import get_db
from ..schemas import UserOut, UserUpdate

router = APIRouter(
   prefix="/user",
   tags=["user"]
)

@router.get("/{username}",
            status_code=status.HTTP_200_OK,
            response_model=UserOut)
async def get_user(username: str, db=Depends(get_db)):
   cursor, conn = db
   query = f"""SELECT username, email, user_role
               FROM users
               JOIN roles ON users.role_id = roles.id
               WHERE username = '{username}'"""
   cursor.execute(query)
   user = cursor.fetchone()
   if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   return UserOut(
      username=user[0],
      email=user[1],
      role=user[2]
   )

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[UserOut])
async def list_users(db=Depends(get_db)):
   cursor, conn = db
   query = f"""SELECT username, email, user_role
               FROM users
               JOIN roles ON users.role_id = roles.id"""
   cursor.execute(query)
   users = cursor.fetchall()
   if not users:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
   return [UserOut(
      username=user[0],
      email=user[1],
      role=user[2]
   ) for user in users]

@router.delete("/",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_user(username: str, db=Depends(get_db)):
   cursor, conn = db
   query = f"""DELETE FROM users WHERE username = '{username}'"""
   cursor.execute(query)
   conn.commit()
   if cursor.rowcount == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   return None

@router.patch("/{username}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def update_user(username: str, user_update: UserUpdate, db=Depends(get_db)):
   cursor, conn = db
   query = f"UPDATE users SET"
   if user_update.username:
      query += f" username = '{user_update.username}',"
   if user_update.password:
      query += f" password = '{user_update.password}',"
   if user_update.email:
      query += f" email = '{user_update.email}',"
   if user_update.role_id:
      query += f" role_id = {user_update.role_id},"
   query = query.rstrip(",")
   if not query.endswith("SET"):
      query += f" WHERE username = '{username}'"
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
   cursor.execute(query)
   conn.commit()
   if cursor.rowcount == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
   return None
