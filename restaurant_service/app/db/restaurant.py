from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 1) Обычный (синхронный) engine
engine = create_engine(
    settings.RESTAURANT_DATABASE_URL,    # например: postgresql+psycopg2://user:pass@localhost/dbname
    echo=True,
)

# 2) Обычная сессия
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 3) Базовый класс для моделей
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) Создание таблиц (один раз при старте)
def init_db():
    import app.models.restaurant
    Base.metadata.create_all(bind=engine)

# 5) Зависимость для FastAPI
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
