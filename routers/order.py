from fastapi import APIRouter, HTTPException, Depends
from routers import AsyncSession, db_helper, select, Order, OrderAddBody, get_timestamp

router = APIRouter()

@router.get("/{id}")
async def get_orders(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    orders = await db.scalars(select(Order).filter(Order.uid == id))
    for order in orders:
        data.append({
            "id": order.id,
            "amount": order.amount,
            "date": order.date,
            "uid": order.uid,
            "pid": order.pid,
            "address": order.address,
            "status": order.status,
            "notes": order.notes,
        })
    return {"orders": data}

@router.post("/")
async def add_order(body: OrderAddBody, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Order(
        amount = body.amount,
        date = get_timestamp(),
        uid = body.uid,
        pid = body.pid,
        address = body.address,
        status = "in progress",
        notes = body.notes,
    ))
    await db.commit()
    return {"message": "order added"}

@router.delete("/{id}")
async def delete_order(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    order = await db.scalar(select(Order).filter(Order.id == id))
    if order:
        await db.delete(order)
        await db.commit()
        return {"message": "order deleted"}
    raise HTTPException(404, "id not found")
