from pydantic import BaseModel, EmailStr, model_validator
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
    confirm_password: str = Form(
        ..., 
        min_length=8, 
        description="Повторенный пароль"
    )

    @model_validator(mode='after')
    def passwords_match(cls, values):
        """Проверяет совпадение паролей."""

        password = values.password
        confirm_password = values.confirm_password
        if confirm_password != password:
            raise ValueError("Пароли не совпадают")
        
        return values