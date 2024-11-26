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

class Test(Base):
    title: Mapped[str] = mapped_column(nullable=False)