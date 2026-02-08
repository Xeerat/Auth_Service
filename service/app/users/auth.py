from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt

from database import AUTH_DATA

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль пользователя.
    
    Args:
        password: пароль для хеширования
    
    Returns:
        Хэш пароля
    """

    return pwd_context.hash(password)


def create_access_token(name: str) -> str:
    """
    Создает токен для пользователя

    Args:
        name: Имя пользователя
    
    Returns:
        Токен пользователя
    """

    expire = datetime.now(timezone.utc) + timedelta(days=14)
    to_encode = {"name": name, "exp": expire}

    try:
        encode_jwt = jwt.encode(
            to_encode, 
            AUTH_DATA["secret_key"],
            algorithm=AUTH_DATA["algorithm"]
        )
    except Exception as error:
        raise error
    else:
        return encode_jwt


def decode_access_token(token: str) -> str:
    """
    Расшифровывает токен пользователя

    Args:
        token: токен пользователя
    
    Returns:
        Имя пользователя
    """

    try:
        user_data = jwt.decode(
            token, 
            AUTH_DATA["secret_key"],
            AUTH_DATA["algorithm"]
        )
    except Exception as error:
        raise error
    else:
        return user_data.get("name")
