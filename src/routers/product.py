from src.routers import *

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer(role="user"))])
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

@router.post("/", dependencies=[Depends(JWTBearer())])
async def add_product(
    request: Request, 
    file: UploadFile, 
    title: str = Form(), 
    description: str = Form(), 
    price: int = Form(), 
    cid: int = Form(), 
    db: AsyncSession = Depends(db_helper.get_db)
):
    category = await db.scalar(select(Category).filter(Category.id == cid))
    if category:
        valid_file = check_picked_file(file)
        print(valid_file)
        if valid_file:
            unique_name = add_image(file)
            db.add(Product(
                title=title,
                description=description,
                image=unique_name,
                price=price,
                cid=cid,
            ))
            await db.commit()
            return {"message": "product added"}
        raise HTTPException(400, "file error")
    raise HTTPException(404, "cid not found")

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def edit_product(
    request: Request, 
    id: int, 
    file: UploadFile, 
    title: str = Form(), 
    description: str = Form(), 
    price: int = Form(), 
    cid: int = Form(), 
    db: AsyncSession = Depends(db_helper.get_db)
):
    category = await db.scalar(select(Category).filter(Category.id == cid))
    if category:
        product = await db.scalar(select(Product).filter(Product.id == id))
        if product:
            valid_file = check_picked_file(file)
            if valid_file:
                remove_image(product.image)
                unique_name=add_image(file)
                product.image=unique_name
                product.title=title
                product.description=description
                product.price=price
                product.cid=cid
                await db.commit()
                return {"message": "product updated"}
            raise HTTPException(400, "file error")
        raise HTTPException(404, "id not found")
    raise HTTPException(404, "cid not found")

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_product(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    product = await db.scalar(select(Product).filter(Product.id == id))
    if product:
        await db.delete(product)
        await db.commit()
        return {"message": "product deleted"}
    raise HTTPException(404, "id not found")
