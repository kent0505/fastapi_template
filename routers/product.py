from routers import *

router = APIRouter()

class _BodyAdd(BaseModel):
    title: str
    price: int
    iid:   int
    cid:   int
class _BodyEdit(BaseModel):
    id:    int
    title: str
    price: int
    iid:   int
    cid:   int

@router.get("/")
async def get_products(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    products = await db.scalars(select(Product))
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
async def add_product(body: _BodyAdd, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Product(
        title = body.title,
        price = body.price,
        iid   = body.iid,
        cid   = body.cid,
    ))
    await db.commit()
    return {"message": "product added"}

@router.put("/")
async def edit_product(body: _BodyEdit, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db.scalar(select(Product).filter(Product.id == body.id))
    if product:
        product.title = body.title
        product.price = body.price
        product.iid   = body.iid
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
