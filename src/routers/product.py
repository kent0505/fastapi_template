from src.routers import *

router = APIRouter()

class _Body(BaseModel):
    title: str
    image: str
    price: int
    cid:   int

@router.get("/")
async def get_products(db: AsyncSession = Depends(db_helper.get_db)):
    products = await db.scalars(select(Product))
    return {"products": [
        {
            "id":    product.id,
            "title": product.title,
            "image": product.image,
            "price": product.price,
            "cid":   product.cid,
        } 
        for product in products
    ]}

@router.post("/")
async def add_product(body: _Body, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Product(
        title = body.title,
        image = body.image,
        price = body.price,
        cid   = body.cid,
    ))
    await db.commit()
    return {"message": "product added"}

@router.put("/{id}")
async def edit_product(id: int, body: _Body, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db.scalar(select(Product).filter(Product.id == id))
    if product:
        product.title = body.title
        product.image = body.image
        product.price = body.price
        product.cid   = body.cid
        await db.commit()
        return {"message": "product updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db.scalar(select(Product).filter(Product.id == id))
    if product:
        await db.delete(product)
        await db.commit()
        return {"message": "product deleted"}
    raise HTTPException(404, "id not found")