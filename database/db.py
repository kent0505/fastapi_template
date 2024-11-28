from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base          import User, Test
from core.schemas           import *
from typing                 import List


# user
async def db_get_user_by_username(db: AsyncSession, username: str) -> User | None:
    return await db.scalar(select(User).filter(User.username == username))
async def db_get_user_by_id(db: AsyncSession, id: int) -> User | None:
    return await db.scalar(select(User).filter(User.id == id))
async def db_add_user(db: AsyncSession, username: str, password: str, role: str) -> None:
    db.add(User(
        username = username, 
        password = password,
        role     = role,
    ))
    await db.commit()
async def db_edit_user(db: AsyncSession, user: User, body: UserUpdateBody) -> None:
    user.username = body.new_username
    user.password = body.new_password
    await db.commit()
async def db_delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()


# test
async def db_get_tests(db: AsyncSession) -> List[Test]:
    return await db.scalars(select(Test))
async def db_get_test_by_id(db: AsyncSession, id: int) -> Test | None:
    return await db.scalar(select(Test).filter(Test.id == id))
async def db_add_test(db: AsyncSession, body: TestAddBody) -> None:
    db.add(Test(
        title = body.title,
    ))
    await db.commit()
async def db_edit_test(db: AsyncSession, test: Test, body: TestUpdateBody) -> None:
    test.title = body.title
    await db.commit()
async def db_delete_test(db: AsyncSession, test: Test) -> None:
    await db.delete(test)
    await db.commit()
