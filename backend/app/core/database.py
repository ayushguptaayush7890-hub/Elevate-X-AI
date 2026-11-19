"""
Database connection, session management, and SQLAlchemy 2.0 Base setup.
"""

from typing import Generator, Tuple, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.core.logging import logger


# SQLAlchemy 2.0 Declarative Base Class
class Base(DeclarativeBase):
    pass


# Engine Creation with connection pooling
engine_kwargs = {
    "echo": settings.DEBUG and settings.APP_ENV == "development",
    "pool_pre_ping": True,
}

# Add pool options for PostgreSQL (SQLite does not support pool_size/max_overflow)
if not settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs.update({
        "pool_size": settings.DATABASE_POOL_SIZE,
        "max_overflow": settings.DATABASE_MAX_OVERFLOW,
        "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
        "pool_recycle": settings.DATABASE_POOL_RECYCLE,
    })
else:
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False}
    })

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session per request.
    Guarantees clean session teardown.
    """
    db: Session = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        logger.error(f"Database session error: {err}")
        db.rollback()
        raise
    finally:
        db.close()


def check_db_connection() -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Verifies actual database connectivity by executing a lightweight query.
    Returns: (is_connected: bool, dialect: str, error_message: str | None)
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            dialect = engine.dialect.name
            return True, dialect, None
    except Exception as exc:
        logger.warning(f"Database connectivity check failed: {str(exc)}")
        return False, None, str(exc)

