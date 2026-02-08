from fastapi import APIRouter

from users.validation import SUser_registration


router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post("/register/")
def user_register(data: SUser_registration) -> dict:
    """Регистрирует нового пользователя в базе данных."""
    
    return data.model_dump()