from routers          import *
from core.jwt_handler import *

router = APIRouter()

class _BodyEdit(BaseModel):
    username:     str = "otaw"
    password:     str = "123"
    new_username: str
    new_password: str

@router.post("/login")
async def login(
    username: str = "otaw",
    password: str = "123",
    db:       AsyncSession = Depends(db_helper.get_db),
):
    user = await db.scalar(select(User).filter(User.username == username))
    if user:
        hashed = check_password(password, user.password)
        if hashed and user.username == username:
            access_token = signJWT(user.id, role=user.role)
            print(access_token)
            return {"access_token": access_token}
    raise HTTPException(401, "username or password invalid")

@router.post("/register")
async def register(
    role:     Literal["admin", "user"],
    username: str = "otaw",
    password: str = "123",
    db:       AsyncSession = Depends(db_helper.get_db)
):
    user = await db.scalar(select(User).filter(User.username == username))
    if user:
        raise HTTPException(409, "this username already exists")
    password = hash_password(password)
    db.add(User(
        username = username, 
        password = password,
        role     = role,
    ))
    await db.commit()
    return {"message": f"new {role} added"}

@router.put("/", dependencies=[Depends(JWTBearer(role="admin"))])
async def edit_admin(
    body: _BodyEdit, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db.scalar(select(User).filter(User.username == body.username))
    if not user:
        raise HTTPException(404, "user not found")
    if body.new_username != "" or body.new_password != "":
        hashed = check_password(body.password, user.password)
        if hashed:
            body.new_password = hash_password(body.new_password)
            user.username     = body.new_username
            user.password     = body.new_password
            await db.commit()
            return {"message": "user updated"}
        raise HTTPException(401, "username or password invalid")
    raise HTTPException(404, "user not found")

@router.put("/", dependencies=[Depends(JWTBearer())])
async def edit_user(
    body: _BodyEdit, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db.scalar(select(User).filter(User.username == body.username))
    if not user:
        raise HTTPException(404, "user not found")
    if body.new_username != "" or body.new_password != "":
        hashed = check_password(body.password, user.password)
        if hashed:
            body.new_password = hash_password(body.new_password)
            user.username     = body.new_username
            user.password     = body.new_password
            await db.commit()
            return {"message": "user updated"}
        raise HTTPException(401, "username or password invalid")
    raise HTTPException(404, "user not found")

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    user = await db.scalar(select(User).filter(User.id == id))
    if user:
        await db.delete(user)
        await db.commit()
        return {"message": "user deleted"}
    raise HTTPException(404, "user not found")
