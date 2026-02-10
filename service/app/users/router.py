from fastapi import APIRouter, Response, Request
from pydantic import EmailStr

from users.validation import SUser_registration, SUser_authentication
from users.validation import SUser_update_data
from users.auth import hash_password, create_access_token, require_role
from users.auth import decode_access_token
from users.admin import AdminRules
from migration.models import Users
from dao.dao_models import UsersDAO


router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post("/register/", summary="Регистрация нового пользователя")
def user_register(data: SUser_registration, response: Response) -> dict:
    """Регистрирует нового пользователя в базе данных."""
    
    found = UsersDAO.find_user(email=data.email)
    if isinstance(found, Users):
        return {"message": "Пользователь с таким email уже зарегистрирован."}
    
    # Заменяем пароль на хэшированный
    data = data.model_copy(update={"password": hash_password(data.password)})

    if found:
        UsersDAO.update_user(
            email=data.email, 
            **data.model_dump(exclude={"email", "confirm_password"})
        )
    else:
        UsersDAO.add_user(
            name=data.name, 
            email=data.email,
            password=data.password,
            surname= data.surname,
            middle_name=data.middle_name
        )

    token = create_access_token(data.email)
    response.set_cookie(key="users_access_token", value=token, httponly=True)

    return {"message": "Пользователь успешно зарегистрирован."}


@router.post("/logout/", summary="Выход из профиля")
def user_logout(response: Response) -> dict:
    """Разлогинивает пользователя."""

    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно разлогинен."}


@router.post("/login/", summary="Аутентификация пользователя")
def user_login(data: SUser_authentication, response: Response) -> dict:
    """Входит в аккаунт пользователя."""
    
    token = create_access_token(email=data.email)
    response.set_cookie(key="users_access_token", value=token, httponly=True)

    return {"message": "Пользователь успешно вошел в аккаунт."}


@router.post("/delete/", summary="Удаление пользователя")
def user_delete(request: Request, response: Response) -> dict:
    """Удаляет аккаунт пользователя из базы данных"""

    token = request.cookies.get("users_access_token")
    user_email = decode_access_token(token)
    UsersDAO.delete_user(user_email)

    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно удален"}


@router.post("/update/", summary="Обновление данные пользователя")
def user_update(data: SUser_update_data, request: Request) -> dict:
    """Обновляет данные пользователя."""

    token = request.cookies.get("users_access_token")
    user_email = decode_access_token(token)

    data = data.model_dump()
    for key in list(data.keys()):
        if data[key] is None:
            del data[key]

    if data.get("password") is not None:
        data["password"] = hash_password(data["password"])

    UsersDAO.update_user(email=user_email, **data)

    return {"message": "Данные успешно изменены"}


@router.get("/data/", summary="Получение данных о пользователе")
@require_role(role="admin")
def user_data(email: EmailStr, request: Request) -> dict:
    """Показывает данные о пользователе."""

    user = UsersDAO.find_user(email=email)
    return user.get_dict()


@router.get("/rules", summary="Показ правил для админа")
@require_role(role="admin")
def get_admin_rules(request: Request) -> dict:
    """Показывает правила для админа"""

    return AdminRules.rules


@router.post("/rules_add", summary="Добавление правила в правила админа")
@require_role(role="admin")
def add_admin_rules(new_rules: str, request: Request) -> dict:
    """Добавляет правило в правила админа"""

    return AdminRules.add_rules(new_rule=new_rules)


@router.post("/rules_del", summary="Удаление правила из правил админа")
@require_role(role="admin")
def del_admin_rules(number_rule: int, request: Request) -> dict:
    """Удаляет правило из правил админа"""

    return AdminRules.del_rules(number_rule=number_rule)