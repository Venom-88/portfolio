"""
Маршруты CRUD для задач текущего пользователя.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Task
from ..schemas import TaskCreate, TaskRead, TaskUpdate
from ..auth import get_current_user, User

router = APIRouter(prefix="/tasks", tags=["tasks"])


# ───────────────────────────── Helpers ────────────────────────────── #


def _apply_filters(
    base_query,
    status_filter: Optional[str],
) -> "select":  # type: ignore[name-defined]
    """Фильтр по статусу todo/done."""
    if status_filter == "todo":
        base_query = base_query.where(Task.is_done.is_(False))
    elif status_filter == "done":
        base_query = base_query.where(Task.is_done.is_(True))
    return base_query


def _apply_ordering(
    base_query,
    ordering: Optional[str],
) -> "select":  # type: ignore[name-defined]
    """
    Сортировка: `created_at` или `-created_at`, `is_done`, `-is_done`, ...

    Несколько полей можно передавать через запятую, пример:
        ?order=created_at,-is_done
    """
    if not ordering:
        return base_query

    for field in ordering.split(","):
        is_desc = field.startswith("-")
        column_name = field.lstrip("-")
        column = getattr(Task, column_name, None)
        if column is not None:
            base_query = base_query.order_by(column.desc() if is_desc else column.asc())
    return base_query


# ───────────────────────────── Endpoints ────────────────────────────── #


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> TaskRead:
    task = Task(**task_in.dict(), owner_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("", response_model=List[TaskRead])
def read_tasks(
    status: Optional[str] = Query(
        None,
        description="Фильтр по статусу: todo | done | (пусто=все)",
        regex="^(todo|done)$",
    ),
    order: Optional[str] = Query(
        None,
        description="Сортировка, например: created_at,-is_done",
    ),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[TaskRead]:
    query = select(Task).where(Task.owner_id == user.id)
    query = _apply_filters(query, status)
    query = _apply_ordering(query, order)
    return session.exec(query).all()


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> TaskRead:
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    task = session.get(Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    session.delete(task)
    session.commit()
