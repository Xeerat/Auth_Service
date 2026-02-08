from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Users(Base):
    """ORM-модель для таблицы users."""
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()