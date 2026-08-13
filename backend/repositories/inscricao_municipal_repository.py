"""Repositorio de dados para Inscricao Municipal."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.inscricao_municipal import InscricaoMunicipal


class InscricaoMunicipalRepository:
    """Operacoes de banco relacionadas a Inscricao Municipal."""

    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar_inscricao_municipal(self, **dados) -> InscricaoMunicipal:
        inscricao = InscricaoMunicipal(**dados)
        self.sessao.add(inscricao)
        self.sessao.flush()
        self.sessao.refresh(inscricao)
        return inscricao

    def buscar_por_id(self, inscricao_id: int) -> InscricaoMunicipal | None:
        return self.sessao.get(InscricaoMunicipal, inscricao_id)

    def listar_por_empresa(self, empresa_id: int) -> list[InscricaoMunicipal]:
        stmt = (
            select(InscricaoMunicipal)
            .where(InscricaoMunicipal.empresa_id == empresa_id)
            .order_by(InscricaoMunicipal.uf, InscricaoMunicipal.municipio, InscricaoMunicipal.id)
        )
        return list(self.sessao.execute(stmt).scalars().all())

    def buscar_duplicada(
        self, empresa_id: int, municipio: str, uf: str, inscricao_municipal: str
    ) -> InscricaoMunicipal | None:
        stmt = select(InscricaoMunicipal).where(
            InscricaoMunicipal.empresa_id == empresa_id,
            InscricaoMunicipal.municipio == municipio,
            InscricaoMunicipal.uf == uf,
            InscricaoMunicipal.inscricao_municipal == inscricao_municipal,
        )
        return self.sessao.execute(stmt).scalar_one_or_none()
