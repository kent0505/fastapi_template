from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas           import ProductAddBody, ProductUpdateBody
from database.db_helper     import db_helper
from database.db            import (
    db_get_products, 
    db_get_product_by_id, 
    db_add_product, 
    db_edit_product, 
    db_delete_product,
)

router = APIRouter()

@router.get("/")
async def get_products(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    products = await db_get_products(db)
    for product in products:
        data.append({
            "id":    product.id,
            "title": product.title,
            "price": product.price,
            "iid":   product.iid,
            "cid":   product.cid,
        })
    return {"products": data}

@router.post("/")
async def add_product(body: ProductAddBody, db: AsyncSession = Depends(db_helper.get_db)):
    await db_add_product(db, body)
    return {"message": "product added"}

@router.put("/")
async def edit_product(body: ProductUpdateBody, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db_get_product_by_id(db, body.id)
    if product:
        await db_edit_product(db, product, body)
        return {"message": "product updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db_get_product_by_id(db, id)
    if product:
        await db_delete_product(db, product)
        return {"message": "product deleted"}
    raise HTTPException(404, "id not found")
