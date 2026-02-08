from pydantic import BaseModel, EmailStr
from fastapi import Form


class SUser_registration(BaseModel):
    """Проверка валидности данных при регистрации."""
    
    email: EmailStr = Form(..., description="Электронная почта")
    name: str = Form(
        ..., 
        min_length=5,
        max_length=10, 
        description="Имя пользователя"
    )
    password: str = Form(..., min_length=8, description="Пароль")