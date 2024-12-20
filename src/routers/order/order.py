# from src.routers import *

# router = APIRouter()

# class _Body(BaseModel):
#     amount:  int = 1
#     uid:     int
#     pid:     int
#     address: str = "41.315166, 69.243769"
#     notes:   str = ""

# @router.get("/{uid}", dependencies=[Depends(JWTBearer(role="user"))])
# async def get_orders(uid: int, db: AsyncSession = Depends(db_helper.get_db)):
#     orders = await db.scalars(select(Order).filter(Order.uid == uid))
#     return {"orders": [
#         {
#             "id":      order.id,
#             "amount":  order.amount,
#             "date":    order.date,
#             "uid":     order.uid,
#             "pid":     order.pid,
#             "address": order.address,
#             "status":  order.status,
#             "notes":   order.notes,
#         } 
#         for order in orders
#     ]}

# @router.post("/", dependencies=[Depends(JWTBearer())])
# async def add_order(body: _Body, db: AsyncSession = Depends(db_helper.get_db)):
#     if (body.uid or body.pid == 0):
#         raise HTTPException(404, "invalid uid or pid")
#     db.add(Order(
#         amount  = body.amount,
#         date    = get_timestamp(),
#         uid     = body.uid,
#         pid     = body.pid,
#         address = body.address,
#         status  = "in progress",
#         notes   = body.notes,
#     ))
#     await db.commit()
#     return {"message": "order added"}

# @router.delete("/{id}", dependencies=[Depends(JWTBearer())])
# async def delete_order(id: int, db: AsyncSession = Depends(db_helper.get_db)):
#     order = await db.scalar(select(Order).filter(Order.id == id))
#     if order:
#         await db.delete(order)
#         await db.commit()
#         return {"message": "order deleted"}
#     raise HTTPException(404, "id not found")
