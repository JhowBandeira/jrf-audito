"""Configuracao centralizada de banco de dados do JRF-Audito."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_PATH = DATABASE_DIR / "jrf_audito.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


class Base(DeclarativeBase):
    """Base declarativa unica para os models SQLAlchemy."""


def criar_engine(database_url: str = DATABASE_URL) -> Engine:
    """Cria a engine SQLAlchemy para a URL de banco informada."""
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        if database_url == DATABASE_URL:
            DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    return create_engine(database_url, connect_args=connect_args)


engine = criar_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def obter_sessao() -> Generator[Session, None, None]:
    """Fornece uma sessao de banco e garante seu fechamento."""
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()
