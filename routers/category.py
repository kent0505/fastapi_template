from routers import *

router = APIRouter()

@router.get("/")
async def get_categories(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    categories = await db.scalars(select(Category))
    for category in categories:
        data.append({
            "id":    category.id,
            "title": category.title,
        })
    return {"categories": data}

@router.post("/")
async def add_category(title: str, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Category(title=title))
    await db.commit()
    return {"message": "category added"}

@router.put("/{id}")
async def edit_category(
    id: int, 
    title: str, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    category = await db.scalar(select(Category).filter(Category.id == id))
    if category:
        category.title = title
        await db.commit()
        return {"message": "category updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_category(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    category = await db.scalar(select(Category).filter(Category.id == id))
    if category:
        await db.delete(category)
        await db.commit()
        return {"message": "category deleted"}
    raise HTTPException(404, "id not found")
