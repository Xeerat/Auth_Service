from fastapi import APIRouter, Response, Request

from users.validation import SUser_registration
from users.auth import hash_password, create_access_token
from users.auth import decode_access_token
from dao.dao_models import UsersDAO


router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post("/register/", summary="Регистрация нового пользователя")
def user_register(data: SUser_registration, response: Response) -> dict:
    """Регистрирует нового пользователя в базе данных."""
    
    found = UsersDAO.find_user(email=data.email, name=data.name)
    if found:
        return {"message": "Такой пользователь уже существует"}
    
    data = data.model_dump()
    del data["confirm_password"]
    data["password"] = hash_password(data["password"])

    UsersDAO.add_data(**data)

    token = create_access_token(data.get("name"))
    response.set_cookie(key="users_access_token", value=token, httponly=True)

    return {"message": "Пользователь успешно зарегистрирован"}


@router.post("/delete/", summary="Удаление пользователя")
def user_delete(request: Request, response: Response) -> dict:
    """Удаляет пользователя"""

    token = request.cookies.get("users_access_token")
    user_name = decode_access_token(token)
    UsersDAO.delete_user(user_name)

    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно удален"}