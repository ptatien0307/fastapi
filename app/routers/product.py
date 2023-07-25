from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from typing import Optional

from ..schemas.schemas import Product

router = APIRouter()

# GET PRODUCTS
@router.get("/posts")
def get_products():
    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()
    return {"data": products}

# CREATE PRODUCT
@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_product(item: Product):
    cursor.execute("""INSERT INTO products (name, price) VALUES (%s, %s) RETURNING *""", (item.name, item.price))
    new_product = cursor.fetchone()
    connection.commit()

    return {"data": new_product}


# GET ONE PRODUCT
@router.get("/posts/{id}")
def get_product(id: int, response: Response):
    cursor.execute("""SELECT * FROM products WHERE id = %s""", (str(id), ))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found')
    return {"data": product}

# DELETE ONE PRODUCT
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_product(id: int):
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id), ))
    deleted_product = cursor.fetchone()
    connection.commit()
    if not deleted_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A PRODUCT
@router.put("/posts/{id}")
def update_one_product(id: int, product: Product):
    cursor.execute("""UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING * """, (product.name, product.price, str(id)))
    updated_product = cursor.fetchone()
    connection.commit()
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found')
    return {"data": updated_product}

