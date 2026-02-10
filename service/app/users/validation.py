from pydantic import BaseModel, EmailStr, model_validator
from fastapi import Form

from typing import Optional

from users.auth import verify_password


class SUser_registration(BaseModel):
    """Проверка валидности данных при регистрации."""
    
    email: EmailStr = Form(..., description="Электронная почта.")
    name: str = Form(..., description="Имя пользователя.")
    surname: str = Form(..., description="Фамилия пользователя.")
    middle_name: str = Form(..., description="Отчество пользователя.")
    password: str = Form(..., min_length=8, description="Пароль.")
    confirm_password: str = Form(
        ..., 
        min_length=8, 
        description="Повторный пароль."
    )

    @model_validator(mode='after')
    def passwords_match(self):
        """
        Проверяет совпадение паролей.

        Raises:
            ValueError - если пароли не сопадают.
        """

        if self.confirm_password != self.password:
            raise ValueError("Пароли не совпадают")
        
        return self
    

class SUser_authentication(BaseModel):
    """Проверка валидности данных при аутентификации."""

    email: EmailStr = Form(..., description="Электронная почта.")
    password: str = Form(..., min_length=8, description="Пароль.")

    @model_validator(mode='after')
    def auth_verify_password(self):
        """
        Проверяет, соответствует ли введённый пароль сохранённому хэшу.

        Raises:
            ValueError - если пароль не подходит или пользователя нет.
        """

        if not verify_password(self.email, self.password):
            raise ValueError("Неверно введена почта или пароль")
        return self


class SUser_update_data(BaseModel):
    """Проверка валидности измененных данных."""
    
    name: Optional[str] = Form(
        None, 
        description="Новое имя пользователя."
    )
    surname: Optional[str] = Form(
        None, 
        description="Новая фамилия пользователя."
    )
    middle_name: Optional[str] = Form(
        None,
        description="Новое отчество пользователя."
    )
    password: Optional[str] = Form(
        None, 
        min_length=8, 
        description="Новый пароль."
    )