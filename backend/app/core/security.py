import bcrypt

def get_password_hash(password: str) -> str:
    """Возвращает bcrypt-хэш в виде str."""
    salt = bcrypt.gensalt()                       # генерируем соль (12 cost по умолчанию)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    """Сравнивает открытый пароль и сохранённый bcrypt-хэш."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())
