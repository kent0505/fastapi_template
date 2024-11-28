from routers import *

router = APIRouter()

class _BodyAdd(BaseModel):
    title: str
class _BodyEdit(BaseModel):
    id:    int
    title: str

@router.get("/")
async def get_tests(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    tests = await db.scalars(select(Test))
    for test in tests:
        data.append({
            "id":    test.id,
            "title": test.title,
        })
    return {"tests": data}

@router.post("/")
async def add_test(body: _BodyAdd, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Test(title=body.title))
    await db.commit()
    return {"message": "test added"}

@router.put("/")
async def edit_test(body: _BodyEdit, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db.scalar(select(Test).filter(Test.id == body.id))
    if test:
        test.title = body.title
        await db.commit()
        return {"message": "test updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_test(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db.scalar(select(Test).filter(Test.id == id))
    if test:
        await db.delete(test)
        await db.commit()
        return {"message": "test deleted"}
    raise HTTPException(404, "id not found")
