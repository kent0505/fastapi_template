from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_helper     import db_helper
from database.db            import db_get_user_by_username, db_get_user_by_id, db_add_user, db_edit_user, db_delete_user
from core.schemas           import UserLoginBody, UserRegisterBody, UserUpdateBody
from core.jwt_handler       import check_password, signJWT, hash_password, JWTBearer

router = APIRouter()

@router.post("/login")
async def login(
    body: UserLoginBody, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_username(db, body.username)
    if user:
        hashed = check_password(body.password, user.password)
        if hashed and user.username == body.username:
            access_token = signJWT(user.id)
            print(access_token)
            return {"access_token": access_token}
    raise HTTPException(401, "username or password invalid")

@router.post("/register")
async def register(
    body: UserRegisterBody, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_username(db, body.username)
    if user:
        raise HTTPException(409, "this username already exists")
    body.password = hash_password(body.password)
    await db_add_user(db, body)
    return {"message": "new user added"}

@router.put("/", dependencies=[Depends(JWTBearer())])
async def update_user(
    body: UserUpdateBody, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_username(db, body.username)
    if not user:
        raise HTTPException(404, "user not found")
    if body.new_username != "" or body.new_password != "":
        hashed = check_password(body.password, user.password)
        if hashed:
            body.new_password = hash_password(body.new_password)
            await db_edit_user(db, user, body)
            return {"message": "user updated"}
        raise HTTPException(401, "username or password invalid")
    raise HTTPException(404, "user not found")

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_id(db, id)
    if user:
        await db_delete_user(db, user)
        return {"message": "user deleted"}
    raise HTTPException(404, "user not found")
