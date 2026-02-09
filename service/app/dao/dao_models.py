from sqlalchemy import select, delete, insert, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import ClauseElement
from pydantic import EmailStr

from typing import TypeVar, Type, Generic

from database import session_maker
from migration.models import Users


T = TypeVar("T")

class BaseDAO(Generic[T]):
    """Базовый класс взаимодействия с данными."""

    model: Type[T]
        
    @classmethod
    def _add_data(cls, **values) -> bool:
        """
        Добавляет данные в базу данных.

        Args:
            values: Словарь с данными для добавления.

                    Ключи должны соответствовать атрибутам ORM-модели.
                    Допустимый набор полей определяется конкретным DAO.
        
        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError.
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
            
    @classmethod
    def _find_where(cls, *conditions: ClauseElement) -> T | None:
        """
        Находит данные по условию.

        Args:
            conditions: Набор условий.
        
        Returns:
            Данные или None, если они не найдены.
        """

        with session_maker() as session:
            query = select(cls.model).where(*conditions)
            result = session.execute(query)
            
            return result.scalars().first()
        
    @classmethod
    def _delete_where(cls, *conditions: ClauseElement) -> bool:
        """
        Удаляет данные из базы данных.

        Args:
            conditions: Набор условий.
        
        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError.
        """

        with session_maker() as session:
            query = delete(cls.model).where(*conditions)
            session.execute(query)

            try:
                session.commit()
            except SQLAlchemyError as error:
                session.rollback()
                raise error
            else:
                return True
            
    @classmethod        
    def _update_data(cls, *conditions: ClauseElement, **values) -> bool:
        """
        Обновляет данные в базе данных

        Args:
            conditions: Набор условий
            values: Словарь с полями и значениями для обновления

        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError.
        """

        with session_maker() as session:
            query = update(cls.model).where(*conditions).values(**values)
            session.execute(query)

            try:
                session.commit()
            except SQLAlchemyError as error:
                session.rollback()
                raise error
            else:
                return True


class UsersDAO(BaseDAO[Users]):
    """Класс взаимодействия с данными таблицы users."""

    model = Users

    @classmethod
    def add_user(
        cls, 
        name: str, 
        email: EmailStr, 
        password: str, 
        surname: str, 
        middle_name: str
    ) -> bool:
        """
        Добавляет пользователя в базу данных.

        Args:
            name: Имя пользователя.
            email: Электронная почта.
            password: Хэшированный пароль.
            surname: Фамилия пользователя
            middle_name: Отчество пользователя

        Returns:
            True - если функция выполнилась без ошибок, иначе SQLAlchemyError.
        """

        return super()._add_data(
            name=name, 
            email=email, 
            password=password,
            surname=surname,
            middle_name=middle_name,
            is_active=True
        )

    @classmethod
    def find_user(cls, email: EmailStr) -> Users | bool:
        """
        Находит пользователя в базе данных.
        
        Args:
            email: Электронная почта.

        Returns:
            Пользователь - если найден, True - если найден, но не активный, 
            False - если не найден.
        """

        user = super()._find_where(cls.model.email == email)
        if user:
            if user.is_active:
                return user
            else:
                return True
        else:
            return False

    @classmethod
    def delete_user(cls, email: EmailStr) -> bool:
        """
        Удаляет данные пользователя из базы данных.
        
        Args:
            email: Электронная почта

        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError.
        """

        return super()._update_data(cls.model.email == email, is_active=False)
    
    @classmethod
    def update_user(cls, email: EmailStr, **values) -> bool:
        """
        Обновляет данные пользователя в базе данных.

        Args: 
            email: Электронная почта.
            values: Словарь с данными которые нужно поменять

        Returns:
            True - если функция завершилась без ошибок, иначе SQLAlchemyError. 
        """

        return super()._update_data(
            cls.model.email == email, 
            **values, 
            is_active=True
        )