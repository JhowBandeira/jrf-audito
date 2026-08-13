"""Repositorio de dados para Participante."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.models.participante import Participante, ParticipantePapel


class ParticipanteRepository:
    """Operacoes de banco relacionadas a Participante."""

    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar_participante(self, *, papeis: list[str], **dados) -> Participante:
        participante = Participante(**dados)
        participante.papeis = [ParticipantePapel(papel=papel) for papel in papeis]
        self.sessao.add(participante)
        self.sessao.flush()
        self.sessao.refresh(participante)
        return participante

    def buscar_por_id(self, empresa_id: int, participante_id: int) -> Participante | None:
        stmt = select(Participante).options(selectinload(Participante.papeis)).where(
            Participante.empresa_id == empresa_id,
            Participante.id == participante_id,
        )
        return self.sessao.execute(stmt).scalar_one_or_none()

    def buscar_por_cpf_cnpj(self, empresa_id: int, cpf_cnpj: str) -> Participante | None:
        stmt = select(Participante).options(selectinload(Participante.papeis)).where(
            Participante.empresa_id == empresa_id,
            Participante.cpf_cnpj == cpf_cnpj,
        )
        return self.sessao.execute(stmt).scalar_one_or_none()

    def listar_por_empresa(self, empresa_id: int) -> list[Participante]:
        stmt = (
            select(Participante)
            .options(selectinload(Participante.papeis))
            .where(Participante.empresa_id == empresa_id)
            .order_by(Participante.razao_social_nome, Participante.id)
        )
        return list(self.sessao.execute(stmt).scalars().all())

    def buscar_duplicado(self, empresa_id: int, cpf_cnpj: str) -> Participante | None:
        return self.buscar_por_cpf_cnpj(empresa_id, cpf_cnpj)
