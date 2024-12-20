# from src.routers import *

# router = APIRouter()

# class _BodyLogin(BaseModel):
#     username:     str = "otaw"
#     password:     str = "123"
# class _BodyEdit(BaseModel):
#     username:     str = "otaw"
#     password:     str = "123"
#     new_username: str
#     new_password: str

# @router.post("/login")
# async def login(
#     body: _BodyLogin,
#     db:   AsyncSession = Depends(db_helper.get_db),
# ):
#     # check admin
#     admin = await db.scalar(select(User).filter(User.role == "admin"))
#     if not admin:
#         db.add(User(
#             username = settings.admin_username,
#             password = hash_password(settings.admin_password),
#             role     = "admin",
#         ))
#         await db.commit()

#     # login
#     user = await db.scalar(select(User).filter(User.username == body.username))
#     if user:
#         hashed = check_password(body.password, user.password)
#         if hashed and user.username == body.username:
#             access_token = signJWT(user.id, role=user.role)
#             print(access_token)
#             return {"access_token": access_token}
#     raise HTTPException(401, "username or password invalid")

# @router.post("/register")
# async def register_user(
#     body: _BodyLogin,
#     db:   AsyncSession = Depends(db_helper.get_db)
# ):
#     user = await db.scalar(select(User).filter(User.username == body.username))
#     if user:
#         raise HTTPException(409, "this username already exists")
#     password = hash_password(body.password)
#     db.add(User(
#         username = body.username, 
#         password = password,
#         role     = "user",
#     ))
#     await db.commit()
#     return {"message": "new user added"}

# @router.post("/register-admin", dependencies=[Depends(JWTBearer())])
# async def register_admin(
#     body: _BodyLogin,
#     role: Literal["admin", "user"],
#     db:   AsyncSession = Depends(db_helper.get_db)
# ):
#     user = await db.scalar(select(User).filter(User.username == body.username))
#     if user:
#         raise HTTPException(409, "this username already exists")
#     password = hash_password(body.password)
#     db.add(User(
#         username = body.username, 
#         password = password,
#         role     = role,
#     ))
#     await db.commit()
#     return {"message": f"new {role} added"}

# @router.put("/", dependencies=[Depends(JWTBearer(role="admin"))])
# async def edit_admin(
#     body: _BodyEdit, 
#     db:   AsyncSession = Depends(db_helper.get_db)
# ):
#     user = await db.scalar(select(User).filter(User.username == body.username))
#     if not user:
#         raise HTTPException(404, "user not found")
#     if body.new_username != "" or body.new_password != "":
#         hashed = check_password(body.password, user.password)
#         if hashed:
#             body.new_password = hash_password(body.new_password)
#             user.username     = body.new_username
#             user.password     = body.new_password
#             await db.commit()
#             return {"message": "user updated"}
#         raise HTTPException(401, "username or password invalid")
#     raise HTTPException(404, "user not found")

# @router.put("/", dependencies=[Depends(JWTBearer())])
# async def edit_user(
#     body: _BodyEdit, 
#     db:   AsyncSession = Depends(db_helper.get_db)
# ):
#     user = await db.scalar(select(User).filter(User.username == body.username))
#     if not user:
#         raise HTTPException(404, "user not found")
#     if body.new_username != "" or body.new_password != "":
#         hashed = check_password(body.password, user.password)
#         if hashed:
#             body.new_password = hash_password(body.new_password)
#             user.username     = body.new_username
#             user.password     = body.new_password
#             await db.commit()
#             return {"message": "user updated"}
#         raise HTTPException(401, "username or password invalid")
#     raise HTTPException(404, "user not found")

# @router.delete("/{id}", dependencies=[Depends(JWTBearer())])
# async def delete_user(
#     id: int, 
#     db: AsyncSession = Depends(db_helper.get_db)
# ):
#     user = await db.scalar(select(User).filter(User.id == id))
#     if user:
#         await db.delete(user)
#         await db.commit()
#         return {"message": "user deleted"}
#     raise HTTPException(404, "user not found")
