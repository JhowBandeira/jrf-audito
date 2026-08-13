"""Repositorio de dados para Inscricao Estadual."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.inscricao_estadual import InscricaoEstadual


class InscricaoEstadualRepository:
    """Operacoes de banco relacionadas a Inscricao Estadual."""

    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar_inscricao_estadual(self, **dados) -> InscricaoEstadual:
        inscricao = InscricaoEstadual(**dados)
        self.sessao.add(inscricao)
        self.sessao.flush()
        self.sessao.refresh(inscricao)
        return inscricao

    def buscar_por_id(self, inscricao_id: int) -> InscricaoEstadual | None:
        return self.sessao.get(InscricaoEstadual, inscricao_id)

    def listar_por_empresa(self, empresa_id: int) -> list[InscricaoEstadual]:
        stmt = (
            select(InscricaoEstadual)
            .where(InscricaoEstadual.empresa_id == empresa_id)
            .order_by(InscricaoEstadual.uf, InscricaoEstadual.id)
        )
        return list(self.sessao.execute(stmt).scalars().all())

    def buscar_duplicada(
        self, empresa_id: int, uf: str, inscricao_estadual: str
    ) -> InscricaoEstadual | None:
        stmt = select(InscricaoEstadual).where(
            InscricaoEstadual.empresa_id == empresa_id,
            InscricaoEstadual.uf == uf,
            InscricaoEstadual.inscricao_estadual == inscricao_estadual,
        )
        return self.sessao.execute(stmt).scalar_one_or_none()
