# backend/app/models.py
from typing import List, Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped  # <— новый импорт!

# ────────────────────────────
# Модель пользователя
# ────────────────────────────
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # оставляем то же поле, что использовалось в маршрутах
    username: str = Field(unique=True, index=True)
    hashed_password: str

    # исправленная аннотация связи «пользователь → список задач»
    tasks: Mapped[List["Task"]] = Relationship(back_populates="owner")


# ────────────────────────────
# Модель задачи
# ────────────────────────────
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: int = Field(foreign_key="user.id")

    # обратная сторона связи
    owner: Mapped["User"] = Relationship(back_populates="tasks")
