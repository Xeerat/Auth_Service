from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()


def get_database_url() -> str:
    """ 
    Формирует URL для подключения к базе данных.

    Returns:   
        Строка URL для подключения к базе данных.
    """
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    name = getenv("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def get_auth_data() -> dict:
    """
    Получает особые данные для создания токенов.

    Returns:
        Словарь с особыми данными для генерации токена
    """

    return {
        "secret_key": getenv("SECRET_KEY"),
        "algorithm": getenv("ALGORITHM")
    }


DB_URL = get_database_url()

engine = create_engine(DB_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

AUTH_DATA = get_auth_data()