from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
import datetime

from ..database import get_db
from ..schemas import OrderOut, OrderCreate, OrderUpdate, OrderItem

router = APIRouter(
   prefix="/order",
   tags=["order"]
)

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[OrderOut])
async def get_orders(username: Optional[str]=None, db=Depends(get_db)):
   cursor, conn = db
   query = f"""SELECT id, username, ship_addr, total, create_at
               FROM orders"""
   cursor.execute(query)
   orders = cursor.fetchall()
   if not orders:
      raise HTTPException(status_code=404, detail="No orders found")
   orders_list = []
   for order in orders:
      order_id, username, ship_address, total, create_at = order
      cursor.execute(f"""SELECT product_sku, amount
                         FROM ordered_items
                         WHERE order_id = '{order_id}'""")
      products = cursor.fetchall()
      items = [OrderItem(product_sku=product[0], amount=product[1]) for product in products]
      orders_list.append(OrderOut(order_num=order_id, username=username, ship_address=ship_address, total=total, products=items, create_at=create_at))
   return orders_list

@router.get("/{username}",
            status_code=status.HTTP_200_OK,
            response_model=List[OrderOut])
async def get_orders_by_username(username: str, db=Depends(get_db)):
   cursor, conn = db
   query = f"""SELECT order_id, username, ship_addr, total, create_at
               FROM orders
               WHERE username = '{username}'"""
   cursor.execute(query)
   orders = cursor.fetchall()
   if not orders:
      raise HTTPException(status_code=404, detail="No orders found")
   orders_list = []
   for order in orders:
      order_id, username, ship_address, total, create_at = order
      cursor.execute(f"""SELECT product_sku, quantity
                         FROM ordered_items
                         WHERE order_id = '{order_id}'""")
      products = cursor.fetchall()
      items = [OrderItem(product_sku=product[0], quantity=product[1]) for product in products]
      orders_list.append(OrderOut(order_id=order_id, username=username, ship_address=ship_address, total=total, items=items, create_at=create_at))
   return orders_list

@router.post("/",
            status_code=status.HTTP_201_CREATED,
            response_model=None)
async def create_order(order: OrderCreate, db=Depends(get_db)):
   cursor, conn = db
   total = 0
   for item in order.products:
      cursor.execute(f"""SELECT price
                         FROM products
                         WHERE sku = '{item.product_sku}'""")
      product = cursor.fetchone()
      if not product:
         raise HTTPException(status_code=404, detail=f"Product {item.product_sku} not found")
      price = product[0]
      total += item.amount * price
   timestamp = datetime.datetime.now()

   # Insert the order into the orders table
   cursor.execute(f"""INSERT INTO orders (username, ship_addr, total, create_at)
                      VALUES ('{order.username}', '{order.ship_address}', {total}, '{timestamp}')""")
   
   cursor.execute(f"""SELECT id FROM orders WHERE username = '{order.username}' AND ship_addr = '{order.ship_address}' AND total = {total} AND create_at = '{timestamp}'""")
   order_id = cursor.fetchone()[0]

   for item in order.products:
      cursor.execute(f"""INSERT INTO ordered_items (order_id, product_sku, amount)
                         VALUES ('{order_id}', '{item.product_sku}', {item.amount})""")

      cursor.execute(f"""SELECT amount
                         FROM reserved_items
                         WHERE product_sku = '{item.product_sku}' AND username = '{order.username}'""")
      reserved_item = cursor.fetchone()
      if not reserved_item:
         raise HTTPException(status_code=404, detail=f"Reserved item {item.product_sku} not found")
      if reserved_item[0] < item.amount:
         raise HTTPException(status_code=400, detail="Not enough reserved items")
      if reserved_item[0] == item.amount:
         cursor.execute(f"""DELETE FROM reserved_items
                            WHERE product_sku = '{item.product_sku}' AND username = '{order.username}'""")
      else:
         cursor.execute(f"""UPDATE reserved_items
                            SET amount = amount - {item.amount}
                            WHERE product_sku = '{item.product_sku}' AND username = '{order.username}'""")
      conn.commit()

@router.patch("/{order_id}",
            status_code=status.HTTP_200_OK,
            response_model=None)
async def update_order(order_id: int, order: OrderUpdate, db=Depends(get_db)):
   cursor, conn = db
   cursor.execute(f"""SELECT order_id
                      FROM orders
                      WHERE order_id = '{order_id}'""")
   existing_order = cursor.fetchone()
   if not existing_order:
      raise HTTPException(status_code=404, detail="Order not found")

   if order.username:
      cursor.execute(f"""UPDATE orders
                         SET username = '{order.username}'
                         WHERE order_id = '{order_id}'""")
   if order.ship_addr:
      cursor.execute(f"""UPDATE orders
                         SET ship_addr = '{order.ship_address}'
                         WHERE order_id = '{order_id}'""")
   if order.product_add:
      for item in order.product_add:
         cursor.execute(f"""SELECT price
                            FROM products
                            WHERE sku = '{item.product_sku}'""")
         product = cursor.fetchone()
         if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_sku} not found")
         price = product[0]
         total = item.amount * price
         cursor.execute(f"""INSERT INTO ordered_items (order_id, product_sku, amount)
                            VALUES ('{order_id}', '{item.product_sku}', {item.amount})""")
         cursor.execute(f"""UPDATE reserved_items
                            SET amount = amount - {item.amount}
                            WHERE product_sku = '{item.product_sku}'""")
         cursor.execute(f"""DELETE FROM reserved_items
                            WHERE product_sku = '{item.product_sku}' AND amount <= 0""")
         cursor.execute(f"""UPDATE orders
                            SET total = total + {total}
                            WHERE order_id = '{order_id}'""")
   if order.product_remove:
      for item in order.product_remove:
         cursor.execute(f"""SELECT amount
                            FROM ordered_items
                            WHERE order_id = '{order_id}' AND product_sku = '{item.product_sku}'""")
         existing_item = cursor.fetchone()
         if not existing_item:
            raise HTTPException(status_code=404, detail=f"Product {item.product_sku} not found in order")
         existing_amount = existing_item[0]
         if item.amount > existing_amount:
            raise HTTPException(status_code=400, detail="Cannot remove more than existing amount")
         cursor.execute(f"""SELECT price
                            FROM products
                            WHERE sku = '{item.product_sku}'""")
         product = cursor.fetchone()
         if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_sku} not found")
         price = product[0]
         deduct_from_total = item.amount * price
         cursor.execute(f"""UPDATE ordered_items
                            SET amount = amount - {item.amount}
                            WHERE order_id = '{order_id}' AND product_sku = '{item.product_sku}'""")
         cursor.execute(f"""UPDATE products
                            SET stock = stock + {item.amount}
                            WHERE sku = '{item.product_sku}'""")
         cursor.execute(f"""UPDATE orders
                            SET total = total - {deduct_from_total}
                            WHERE order_id = '{order_id}'""")
   conn.commit()

@router.delete("/{order_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_order(order_id: int, db=Depends(get_db)):
   cursor, conn = db
   cursor.execute(f"""SELECT product_sku, amount
                      FROM ordered_items
                      WHERE order_id = '{order_id}'""")
   products = cursor.fetchall()
   for product in products:
      cursor.execute(f"""UPDATE products
                         SET stock = stock + {product[1]}
                         WHERE sku = '{product[0]}'""")
   cursor.execute(f"""DELETE FROM ordered_items WHERE order_id = '{order_id}'""")
   cursor.execute(f"""DELETE FROM orders WHERE id = '{order_id}'""")
   conn.commit()