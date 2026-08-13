"""Dependencias compartilhadas da API."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.core.database import obter_sessao


def obter_sessao_api() -> Generator[Session, None, None]:
    """Entrega uma sessao de banco por request HTTP."""
    yield from obter_sessao()
