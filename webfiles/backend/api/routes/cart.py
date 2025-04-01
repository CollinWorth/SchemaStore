from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from psycopg2 import Error

from ..database import get_db

router = APIRouter(
   prefix="/cart",
   tags=["cart"]
)

class Cart(BaseModel):
   username: str
   products: dict[str, int]

class Item(BaseModel):
   username: str
   product_sku: str
   amount: int

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=Cart)
async def getCart(username: str, db=Depends(get_db)):
   cursor, conn = db
   query = f"""SELECT product_sku, amount FROM "reserved_items"
                  WHERE "username" = '{username}'"""

   cursor.execute(query)
   cart = cursor.fetchall()

   products = {sku: amount for sku, amount in cart}

   return Cart(
      username=username,
      products=products
   )

@router.post("/",
             status_code=status.HTTP_204_NO_CONTENT,
             response_model=None
            )
async def addToCart(item: Item, db=Depends(get_db)):
   cursor, conn = db

   # Check if same sku already in cart
   statement = f"""SELECT "product_sku" FROM "reserved_items" WHERE "username" = '{item.username}' AND "product_sku" = '{item.product_sku}'"""
   cursor.execute(statement)
   duplicate_item = cursor.fetchone()

   try:
      statement = f"""UPDATE "products" SET "stock" = "stock" - {item.amount} WHERE "sku" = '{item.product_sku}'"""
      cursor.execute(statement)
   except Error as e:
      if e.pgcode == '23514':
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
               "error": "CHECK constraint violated",
               "message": f"There isn't enough {item.product_sku} in stock"
            }
         )
      else:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
               "error": "Database error",
               "message": str(e)
            }
         )
   finally:
      if duplicate_item:
         statement = f"""UPDATE "reserved_items" SET "amount" = "amount" + {item.amount}
                            WHERE "product_sku" = '{item.product_sku}' AND "username" = '{item.username}'"""
      else:
         statement = f"""INSERT INTO "reserved_items" ("username", "product_sku", "amount")
                         VALUES ('{item.username}', '{item.product_sku}', '{item.amount}')"""
      cursor.execute(statement)
      cursor.connection.commit()
      return None

@router.delete("/",
                status_code=status.HTTP_204_NO_CONTENT,
                response_model=None)
async def deleteItem(item: Item, db = Depends(get_db)):
   cursor, conn = db

   # Find the amount currently in cart
   statement = f"""SELECT "amount" FROM "reserved_items" WHERE "product_sku" = '{item.product_sku}' AND "username" = '{item.username}'"""
   cursor.execute(statement)
   amount_in_cart = cursor.fetchone()[0]

   # Delete either entire row from cart or amount requested
   if amount_in_cart - item.amount <= 0:
      statement = f"""DELETE FROM "reserved_items" WHERE "product_sku" = '{item.product_sku}' AND "username" = '{item.username}'"""
   else:
      statement = f"""UPDATE "reserved_items" SET "amount" = "amount" - {item.amount} WHERE "product_sku" = '{item.product_sku}' AND "username" = '{item.username}'"""
   cursor.execute(statement)

   # Check that we are actually deleting something
   if cursor.rowcount == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

   # Update the product listing
   statement = f"""UPDATE "products" SET "stock" = "stock" + {item.amount} WHERE "sku" = '{item.product_sku}'"""
   cursor.execute(statement)


   cursor.connection.commit()
   return None