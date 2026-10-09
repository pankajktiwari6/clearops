from collections.abc import Iterator
from functools import lru_cache
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


def _url() -> str:
    auth = ""
    if settings.DB_USERNAME:
        auth = f"{quote_plus(settings.DB_USERNAME)}:{quote_plus(settings.DB_PASSWORD or '')}@"
    return (
        f"mssql+pyodbc://{auth}{settings.DB_SERVER}/{settings.DB_DATABASE}"
        "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )


@lru_cache
def get_engine() -> Engine:
    """Created on first use so importing the app never needs the ODBC driver."""
    return create_engine(_url(), pool_pre_ping=True)


SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    with SessionLocal(bind=get_engine()) as db:
        yield db
