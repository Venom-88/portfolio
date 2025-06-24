from sqlmodel import SQLModel, Session, create_engine

# ---- настройки БД ----
DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},  # только для SQLite
)


def init_db() -> None:
    """Создать таблицы при старте приложения."""
    SQLModel.metadata.create_all(engine)


def get_session():        # <-- БЕЗ декоратора!
    """Зависимость FastAPI: выдаёт Session и закрывает его после запроса."""
    with Session(engine) as session:
        yield session
