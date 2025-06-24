"""
Аутентификация / авторизация через JWT-токен + хэширование пароля.

Подключается как зависимость:
    from ..auth import get_current_user
    def route(user: User = Depends(get_current_user)):
        ...
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from .database import get_session
from .models import User

# --------------------------------------------------------------------------- #
#  Настройки (в проде лучше брать из переменных окружения)                    #
# --------------------------------------------------------------------------- #
SECRET_KEY = "CHANGE_ME_TO_RANDOM_STRING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 час

# --------------------------------------------------------------------------- #
#  Инструменты                                                                 #
# --------------------------------------------------------------------------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнение введённого пароля и сохранённого хэша."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Создать bcrypt-хэш пароля перед записью в БД."""
    return pwd_context.hash(password)


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> Optional[User]:
    """
    Проверка логина/пароля.

    Возвращает пользователя если всё ок, иначе None.
    """
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    sub: str,
    expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """
    Сгенерировать JWT-токен.

    sub — обычно имя пользователя или user_id.
    """
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """
    Зависимость FastAPI: достаём пользователя из токена.

    Если токен неверный или пользователь не найден — 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить токен",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user
