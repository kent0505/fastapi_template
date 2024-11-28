from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas           import OrderAddBody
from typing                 import Literal
from database.db_helper     import db_helper
from database.db            import (
    db_get_orders, 
    db_get_order_by_id, 
    db_add_order, 
    db_edit_order, 
    db_delete_order,
) 

router = APIRouter()

@router.get("/")
async def get_orders(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    orders = await db_get_orders(db)
    for order in orders:
        data.append({
            "id":      order.id,
            "amount":  order.amount,
            "date":    order.date,
            "uid":     order.uid,
            "pid":     order.pid,
            "address": order.address,
            "status":  order.status,
            "notes":   order.notes,
        })
    return {"orders": data}

@router.post("/")
async def add_order(body: OrderAddBody, db: AsyncSession = Depends(db_helper.get_db)):
    await db_add_order(db, body)
    return {"message": "order added"}

@router.put("/{id}")
async def edit_order(
    id:     int, 
    status: Literal["in progress", "completed", "cancelled"],
    db:     AsyncSession = Depends(db_helper.get_db)
):
    order = await db_get_order_by_id(db, id)
    if order:
        await db_edit_order(db, order, status)
        return {"message": "order updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_order(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    order = await db_get_order_by_id(db, id)
    if order:
        await db_delete_order(db, order)
        return {"message": "order deleted"}
    raise HTTPException(404, "id not found")
