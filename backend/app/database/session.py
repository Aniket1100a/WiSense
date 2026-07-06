from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings

settings = Settings()

engine = create_engine(
    settings.database_url,
    future=True,
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session for request-scoped dependency injection."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
