from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class User(Base):
    username: Mapped[str]  = mapped_column(nullable=False, unique=True)
    password: Mapped[str]  = mapped_column(nullable=False)
    role:     Mapped[str]  = mapped_column(nullable=False)

class Test(Base):
    title: Mapped[str] = mapped_column(nullable=False)

class Category(Base):
    title: Mapped[str] = mapped_column(nullable=False)

class Product(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    iid:   Mapped[int] = mapped_column(nullable=False) # image id
    cid:   Mapped[int] = mapped_column(nullable=False) # category id

class Order(Base):
    amount:  Mapped[int] = mapped_column(nullable=False)
    date:    Mapped[int] = mapped_column(nullable=False) # timestamp
    uid:     Mapped[int] = mapped_column(nullable=False) # user id
    pid:     Mapped[int] = mapped_column(nullable=False) # product id
    address: Mapped[str] = mapped_column(nullable=False) # address lat and lon "41.315166, 69.243769"
    status:  Mapped[str] = mapped_column(nullable=False) # in progress | completed | cancelled
    notes:   Mapped[str] = mapped_column(nullable=False)

# class Image(Base):
#     url: Mapped[str] = mapped_column(nullable=False)