# db.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 🧩 Преобразуем URL в async формат
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# ⚙️ Создаём движок с авто-проверкой соединения и рециклом
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,   # ✅ проверяет соединение перед использованием
    pool_recycle=1800,    # ♻️ обновляет соединения каждые 30 минут
    pool_size=5,          # оптимальный пул
    max_overflow=10,      # допускаем временное расширение пула
)

# 🧠 Настраиваем асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 🔁 Dependency для FastAPI
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# 🧱 Базовая модель
Base = declarative_base()
