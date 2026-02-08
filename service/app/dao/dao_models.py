from sqlalchemy import or_, select, delete, insert
from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr

from database import session_maker
from migration.models import Users


class BaseDAO:
    """Базовый класс взаимодействия с данными."""

    model = None
        
    @classmethod
    def add_data(cls, **values) -> bool:
        """
        Добавляет данные в базу данных.

        Args:
            values: Словарь с данными для добавления.

                    Ключи должны соответствовать атрибутам ORM-модели.
                    Допустимый набор полей определяется конкретным DAO.
        
        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError
        """

        with session_maker() as session:
            query = insert(cls.model).values(**values)
            session.execute(query)
            
            try:
                session.commit()
            except SQLAlchemyError as error:
                session.rollback()
                raise error
            else:
                return True


class UsersDAO(BaseDAO):
    """Класс взаимодействия с данными таблицы users."""

    model = Users

    @classmethod
    def add_data(cls, **values) -> bool:
        """
        Добавляет пользователя в базу данных.

        Допустимые поля:
        - name
        - email
        - password
        """

        return super().add_data(**values)

    @classmethod
    def find_user(cls, email: EmailStr, name: str) -> Users | None:
        """
        Находит пользователя в базе данных.
        
        Args:
            email: Электронная почта.
            name: Имя пользователя.

        Returns:
            Пользователь или None, если он не найден.
        """

        with session_maker() as session:
            conditions = or_(
                cls.model.email == email,
                cls.model.name == name
            )
            query = select(cls.model).where(conditions)
            result = session.execute(query)
            
            return result.scalar_one_or_none()
        
    @classmethod
    def delete_user(cls, name: str) -> bool:
        """
        Удаляет данные пользователя из базы данных.
        
        Args:
            name: Имя пользователя

        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError
        """

        with session_maker() as session:
            query = delete(cls.model).where(cls.model.name == name)
            session.execute(query)

            try:
                session.commit()
            except SQLAlchemyError as error:
                session.rollback()
                return error
            else:
                return True