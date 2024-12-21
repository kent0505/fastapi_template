from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class Test(Base):
    title: Mapped[str] = mapped_column(nullable=False)

# class Quiz(Base):
#     question: Mapped[str] = mapped_column(nullable=False)
#     answer: Mapped[str] = mapped_column(nullable=False)

# class User(Base):
#     userid:    Mapped[int] = mapped_column(nullable=False)
#     username:  Mapped[str] = mapped_column(nullable=False)
#     firstname: Mapped[str] = mapped_column(nullable=False)
#     lastname:  Mapped[str] = mapped_column(nullable=False)
#     role:      Mapped[str] = mapped_column(nullable=False, default="user") # user | admin 
#     status:    Mapped[str] = mapped_column(nullable=False, default="active"), # active | ban
#     coins:     Mapped[int] = mapped_column(nullable=False)
