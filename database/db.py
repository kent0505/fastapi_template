from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base          import User, Test, Category, Product, Order
from core.schemas           import *
from core.utils             import get_timestamp
from typing                 import List


# user
async def db_get_user_by_username(db: AsyncSession, username: str) -> User | None:
    return await db.scalar(select(User).filter(User.username == username))
async def db_get_user_by_id(db: AsyncSession, id: int) -> User | None:
    return await db.scalar(select(User).filter(User.id == id))
async def db_add_user(db: AsyncSession, body: UserRegisterBody) -> None:
    db.add(User(
        username = body.username, 
        password = body.password,
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


# category
async def db_get_categories(db: AsyncSession) -> List[Category]:
    return await db.scalars(select(Category))
async def db_get_category_by_id(db: AsyncSession, id: int) -> Category | None:
    return await db.scalar(select(Category).filter(Category.id == id))
async def db_add_category(db: AsyncSession, body: CategoryAddBody) -> None:
    db.add(Category(
        title = body.title,
    ))
    await db.commit()
async def db_edit_category(db: AsyncSession, category: Category, body: CategoryUpdateBody) -> None:
    category.title = body.title
    await db.commit()
async def db_delete_category(db: AsyncSession, category: Category) -> None:
    await db.delete(category)
    await db.commit()


# product
async def db_get_products(db: AsyncSession) -> List[Product]:
    return await db.scalars(select(Product))
async def db_get_product_by_id(db: AsyncSession, id: int) -> Product | None:
    return await db.scalar(select(Product).filter(Product.id == id))
async def db_add_product(db: AsyncSession, body: ProductAddBody) -> None:
    db.add(Product(
        title = body.title,
        price = body.price,
        iid   = body.iid,
        cid   = body.cid,
    ))
    await db.commit()
async def db_edit_product(db: AsyncSession, product: Product, body: ProductUpdateBody) -> None:
    product.title = body.title
    product.price = body.price
    product.iid   = body.iid
    product.cid   = body.cid
    await db.commit()
async def db_delete_product(db: AsyncSession, product: Product) -> None:
    await db.delete(product)
    await db.commit()



# order
async def db_get_orders(db: AsyncSession) -> List[Order]:
    return await db.scalars(select(Order))
async def db_get_order_by_id(db: AsyncSession, id: int) -> Order | None:
    return await db.scalar(select(Order).filter(Order.id == id))
async def db_add_order(db: AsyncSession, body: OrderAddBody) -> None:
    db.add(Order(
        amount  = body.amount,
        date    = get_timestamp(),
        uid     = body.uid,
        pid     = body.pid,
        address = body.address,
        status  = "in progress",
        notes   = body.notes,
    ))
    await db.commit()
async def db_edit_order(db: AsyncSession, order: Order, status: str) -> None:
    order.status = status
    await db.commit()
async def db_delete_order(db: AsyncSession, order: Order) -> None:
    await db.delete(order)
    await db.commit()
