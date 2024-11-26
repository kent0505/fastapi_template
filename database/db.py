from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base          import User, Test
from core.schemas           import *
from typing                 import List

# user
async def db_get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Retrieve a user by their username."""
    return await db.scalar(select(User).filter(User.username == username))

async def db_get_user_by_id(db: AsyncSession, id: int) -> User | None:
    """Retrieve a user by their ID."""
    return await db.scalar(select(User).filter(User.id == id))

async def db_add_user(db: AsyncSession, body: UserRegisterBody) -> None:
    """Add a new user to the database."""
    db.add(User(
        username = body.username, 
        password = body.password,
    ))
    await db.commit()

async def db_edit_user(db: AsyncSession, user: User, body: UserUpdateBody) -> None:
    """Update user details in the database."""
    user.username = body.new_username
    user.password = body.new_password
    await db.commit()

async def db_delete_user(db: AsyncSession, user: User) -> None:
    """Delete a user from the database."""
    await db.delete(user)
    await db.commit()

# test
async def db_get_tests(db: AsyncSession) -> List[Test]:
    """Retrieve all tests from the database."""
    return await db.scalars(select(Test))

async def db_get_test_by_id(db: AsyncSession, id: int) -> Test | None:
    """Retrieve a test by its ID."""
    return await db.scalar(select(Test).filter(Test.id == id))

async def db_add_test(db: AsyncSession, body: TestAddBody) -> None:
    """Add a new test to the database."""
    db.add(Test(
        title = body.title,
    ))
    await db.commit()

async def db_edit_test(db: AsyncSession, test: Test, body: TestUpdateBody) -> None:
    """Update test details in the database."""
    test.title = body.title
    await db.commit()

async def db_delete_test(db: AsyncSession, test: Test) -> None:
    """Delete a test from the database."""
    await db.delete(test)
    await db.commit()