"""
Маршруты для регистрации и входа пользователя.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserRead, Token
from ..auth import hash_password, authenticate_user, create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    """
    Создать нового пользователя.

    Возвращает данные пользователя без пароля.
    """
    # Проверяем, что имени ещё нет
    if session.exec(select(User).where(User.username == user_in.username)).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user  # FastAPI сам сконвертирует в UserRead


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Token:
    """
    Проверка логина/пароля и выдача JWT.

    Использует стандартную форму OAuth2PasswordRequestForm:
        content-type: application/x-www-form-urlencoded
        fields: username, password
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(sub=user.username)
    return {"access_token": token, "token_type": "bearer"}
