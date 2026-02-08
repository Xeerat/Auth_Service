from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine


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


DB_URL = get_database_url()
engine = create_engine(DB_URL)