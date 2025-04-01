from fastapi import APIRouter, UploadFile, Depends, File, HTTPException

from ..database import get_db
from ..crud import register_product
from ..schemas import ProductOut, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# Get all products
@router.get("/", response_model=list[ProductOut])
def get_all_products(db=Depends(get_db)):
    cursor, conn = db
    # Get Products
    cursor.execute(f'''SELECT sku, name, description, price, stock, img
                       FROM products''')
    products = cursor.fetchall()  # Get all products as tuples

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    # Get Categories
    categories:dict[str, list[str]] = {}
    for product in products:
        statement = f'''SELECT categories.category
                        FROM categories
                            JOIN products_categories ON categories.id = products_categories.category_id
                            JOIN products ON products.sku = products_categories.product_sku
                        WHERE products.sku = \'{product[0]}\''''
        cursor.execute(statement)
        categories[product[0]] = []
        for category in cursor.fetchall():
            categories[product[0]].append(category[0])

    return [
        ProductOut(
            sku=product[0], 
            name=product[1], 
            description=product[2], 
            price=product[3], 
            stock=product[4], 
            img=None,
            categories=categories[product[0]],
        ) for product in products
    ]

@router.get("/{sku}", response_model=ProductOut)
def get_product(sku: str, db=Depends(get_db)):
    cursor, conn = db
    cursor.execute(f"SELECT sku, name, description, price, stock, img FROM products WHERE sku = '{sku}'")
    product = cursor.fetchone()  # Get the product as a tuple
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    statement = f'''SELECT categories.category
                    FROM categories
                        JOIN products_categories ON categories.id = products_categories.category_id
                        JOIN products ON products.sku = products_categories.product_sku
                    WHERE products.sku = \'{product[0]}\''''
    cursor.execute(statement)
    categories = []
    for category in cursor.fetchall():
        categories.append(category[0])
    
    return ProductOut(
        sku=product[0], 
        name=product[1], 
        description=product[2], 
        price=product[3], 
        stock=product[4],
        img=product[5],
        categories=categories
    )

@router.post("/", response_model=ProductOut)
def create_product(
    sku: str, 
    name: str, 
    description: str, 
    price: float, 
    stock: int, 
    file: UploadFile = File(...), 
    db=Depends(get_db)
):
    cursor, conn = db
    register_product(cursor, sku, name, description, price, stock, file)
    return ProductOut(
        sku=sku, name=name, description=description, price=price, stock=stock, img=f"/images/{sku}.png", categories=[]
    )
