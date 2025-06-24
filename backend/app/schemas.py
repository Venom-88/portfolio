from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


# ---------- Схемы пользователя ----------

class UserCreate(BaseModel):
    """Запрос на регистрацию."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=128)


class UserRead(BaseModel):
    """Ответ клиенту о пользователе (без пароля)."""
    id: int
    username: str


class Token(BaseModel):
    """JWT-токен после логина/регистрации."""
    access_token: str
    token_type: str = "bearer"


# ---------- Схемы задачи ----------

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Создание задачи — те же поля, что и в основе."""
    pass


class TaskRead(TaskBase):
    """Ответ клиенту: все поля + id, статус и дата."""
    id: int
    is_done: bool
    created_at: datetime


class TaskUpdate(BaseModel):
    """Частичное обновление задачи: все поля необязательны."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_done: Optional[bool] = None

    # если все поля None — ошибка
    @validator("*", pre=True, always=True)
    def at_least_one_field(cls, v, values, **kwargs):  # type: ignore[method-parameters]
        if not any(values.values()) and v is None:
            raise ValueError("Нужно указать хотя бы одно поле для обновления")
        return v
