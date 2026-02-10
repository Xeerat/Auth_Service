from datetime import datetime, timedelta, timezone
from functools import wraps

from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr
from fastapi import HTTPException, Request

from database import AUTH_DATA
from dao.dao_models import UsersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль пользователя.
    
    Args:
        password: пароль для хеширования.
    
    Returns:
        Хэш пароля.
    """

    return pwd_context.hash(password)


def create_access_token(email: EmailStr) -> str:
    """
    Создает токен для пользователя.

    Args:
        email: электронная почта.
    
    Returns:
        Токен пользователя.

    Raises:
        Exception - если возникла ошибка при генерации токена. 
    """

    expire = datetime.now(timezone.utc) + timedelta(days=14)
    to_encode = {"email": email, "exp": expire}

    try:
        token = jwt.encode(
            to_encode, 
            key=AUTH_DATA["secret_key"],
            algorithm=AUTH_DATA["algorithm"]
        )
    except Exception as error:
        raise error
    
    return token


def decode_access_token(token: str) -> EmailStr:
    """
    Расшифровывает токен пользователя.

    Args:
        token: токен пользователя.
    
    Returns:
        Электронную почту пользователя.

    Raises:
        Exception - если возникла ошибка при расшифровке токена.
    """

    try:
        user_data = jwt.decode(
            token, 
            AUTH_DATA["secret_key"],
            AUTH_DATA["algorithm"]
        )
    except Exception as error:
        raise error
    
    return user_data.get("email")


def verify_password(email: EmailStr, password: str) -> bool:
    """
    Проверяет, соответствует ли введённый пароль сохранённому хэшу.

    Args:
        email: электронная почта пользователя.
        password: пароль, который нужно проверить.
    
    Returns:
        True - если пароль совпал, иначе False.
    """

    user = UsersDAO.find_user(email=email)
    if isinstance(user, bool):
        return False
    
    if pwd_context.verify(password, user.password) is False:
        return False

    return True


def require_role(role: str):
    """
    Декоратор для авторизации пользователя.

    Функция, к которой применяется декоратор, должна иметь аргумент
    request: Request. Иначе возникнет ошибка.

    Args:
        role: роль, необходимая для выполнения функции.
    
    Raises:
        HTTPException(401) - если пользователь не авторизован.
        HTTPException(403) - если у пользователя нет доступа к данной функции.
    """

    def decorator(func):
        """Внутренняя функция декоратор."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Авторизует пользователя."""

            request: Request = kwargs.get("request")
            token = request.cookies.get("users_access_token")

            if token is None:
                raise HTTPException(
                    status_code=401, 
                    detail="Пользователь не авторизован"
                )

            user_email = decode_access_token(token)
            user = UsersDAO.find_user(email=user_email)

            if isinstance(user, bool):
                raise HTTPException(
                    status_code=401, 
                    detail="Пользователь не авторизован"
                )
          
            if user.role != role:
                raise HTTPException(
                    status_code=403,
                    detail="Нет доступа"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator