from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Users(Base):
    """ORM-модель для таблицы users."""
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    role: Mapped[str] = mapped_column()

    def get_dict(self):
        """
        Выводит данные о пользователе в виде словаря.
        
        Returns:
            Словарь с данными о пользователе.
        """

        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "middle_name": self.middle_name,
            "is_active": self.is_active,
            "role": self.role
        }
