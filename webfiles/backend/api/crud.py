from passlib.context import CryptContext
import logging

logging.basicConfig(level=logging.DEBUG)  # Set log level to debug

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_product(cursor, sku: str, name: str, description: str, price: float, stock: int, img_url: str):
    """Register a new product, storing the image URL."""
    cursor.execute(
        "INSERT INTO products (sku, name, description, price, stock, img) VALUES (%s, %s, %s, %s, %s, %s)",
        (sku, name, description, price, stock, img_url)
    )
    cursor.connection.commit()


def search_products_by_query(query: str, db):
    cursor, conn = db

    # Execute the query with the search string
    cursor.execute("""
        SELECT sku, name, description, price, stock, img
        FROM products
        WHERE name ILIKE %s OR description ILIKE %s
        LIMIT 50;
    """, (f"%{query}%", f"%{query}%"))

    results = cursor.fetchall()
    return results