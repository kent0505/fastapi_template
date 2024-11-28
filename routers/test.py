from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_helper     import db_helper
from core.schemas           import TestAddBody, TestUpdateBody
from database.db            import (
    db_get_tests, 
    db_get_test_by_id, 
    db_add_test, 
    db_edit_test, 
    db_delete_test,
)

router = APIRouter()

@router.get("/")
async def get_tests(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    tests = await db_get_tests(db)
    for test in tests:
        data.append({
            "id":    test.id,
            "title": test.title,
        })
    return {"tests": data}

@router.post("/")
async def add_test(body: TestAddBody, db: AsyncSession = Depends(db_helper.get_db)):
    await db_add_test(db, body)
    return {"message": "test added"}

@router.put("/")
async def edit_test(body: TestUpdateBody, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db_get_test_by_id(db, body.id)
    if test:
        await db_edit_test(db, test, body)
        return {"message": "test updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_test(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db_get_test_by_id(db, id)
    if test:
        await db_delete_test(db, test)
        return {"message": "test deleted"}
    raise HTTPException(404, "id not found")
