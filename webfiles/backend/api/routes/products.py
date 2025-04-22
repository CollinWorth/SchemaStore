from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status

from ..database import get_db
from ..crud import register_product, search_products_by_query
from ..schemas import ProductOut, ProductCreate
from fastapi import Form 

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

@router.get("/search", response_model=list[ProductOut])
async def search_products(query: str, db=Depends(get_db)):
    # Call the search function, which already handles the empty results case
    results = search_products_by_query(query, db)

    return [ProductOut(**{
        "sku": p[0],
        "name": p[1],
        "description": p[2],
        "price": p[3],
        "stock": p[4],
        "img": p[5],
    }) for p in results]

@router.get("/{sku}", response_model=ProductOut)
def get_product(sku: str, db=Depends(get_db)):
    cursor, conn = db
    cursor.execute(f"SELECT sku, name, description, price, stock, img FROM products WHERE sku = '{sku}'")
    product = cursor.fetchone()  # Get the product as a tuple
    if not product:
        raise HTTPException(status_code=404, detail="Product not found sku")

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
        img=None
        #categories = categories
    )

@router.post("/", response_model=ProductOut)
def create_product(
    sku: str = Form(...), 
    name: str = Form(...), 
    description: str = Form(...), 
    price: float = Form(...), 
    stock: int = Form(...), 
    file: UploadFile = File(...), 
    db=Depends(get_db)
):
    cursor, conn = db
    register_product(cursor, sku, name, description, price, stock, file)
    return ProductOut(
        sku=sku, 
        name=name, 
        description=description, 
        price=price, 
        stock=stock, 
        img=f"/images/{sku}.png", 
        categories=[]
    )

@router.delete("/{sku}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(sku: str, db=Depends(get_db)):
    cursor, conn = db
    query = f"""DELETE FROM products_categories WHERE product_sku = '{sku}';
                DELETE FROM reserved_items WHERE product_sku = '{sku}';
                DELETE FROM products WHERE sku = '{sku}';"""
    cursor.execute(query)
    conn.commit()
    return {"message": "Product deleted successfully"}
