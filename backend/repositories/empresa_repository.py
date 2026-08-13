"""Repositorio de dados para Empresa."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.empresa import Empresa


class EmpresaRepository:
    """Operacoes de banco relacionadas ao model Empresa."""

    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar_empresa(self, **dados) -> Empresa:
        empresa = Empresa(**dados)
        self.sessao.add(empresa)
        self.sessao.flush()
        self.sessao.refresh(empresa)
        return empresa

    def buscar_empresa_por_id(self, empresa_id: int) -> Empresa | None:
        return self.sessao.get(Empresa, empresa_id)

    def buscar_empresa_por_cnpj(self, cnpj: str) -> Empresa | None:
        stmt = select(Empresa).where(Empresa.cnpj == cnpj)
        return self.sessao.execute(stmt).scalar_one_or_none()

    def listar_empresas(self) -> list[Empresa]:
        stmt = select(Empresa).order_by(Empresa.razao_social, Empresa.id)
        return list(self.sessao.execute(stmt).scalars().all())
