from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas           import CategoryAddBody, CategoryUpdateBody
from database.db_helper     import db_helper
from database.db            import (
    db_get_categories, 
    db_get_category_by_id, 
    db_add_category, 
    db_edit_category, 
    db_delete_category,
)

router = APIRouter()

@router.get("/")
async def get_categories(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    categories = await db_get_categories(db)
    for category in categories:
        data.append({
            "id":    category.id,
            "title": category.title,
        })
    return {"categories": data}

@router.post("/")
async def add_category(body: CategoryAddBody, db: AsyncSession = Depends(db_helper.get_db)):
    await db_add_category(db, body)
    return {"message": "category added"}

@router.put("/")
async def edit_category(body: CategoryUpdateBody, db: AsyncSession = Depends(db_helper.get_db)):
    category = await db_get_category_by_id(db, body.id)
    if category:
        await db_edit_category(db, category, body)
        return {"message": "category updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_category(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    category = await db_get_category_by_id(db, id)
    if category:
        await db_delete_category(db, category)
        return {"message": "category deleted"}
    raise HTTPException(404, "id not found")
