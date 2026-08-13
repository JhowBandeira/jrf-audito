"""Servico de aplicacao para Inscricao Estadual."""

from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.models.inscricao_estadual import InscricaoEstadual
from backend.repositories.empresa_repository import EmpresaRepository
from backend.repositories.inscricao_estadual_repository import InscricaoEstadualRepository
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class InscricaoEstadualDadosInvalidosError(Exception):
    """Erro para dados invalidos de Inscricao Estadual."""


class InscricaoEstadualJaExisteError(Exception):
    """Erro para Inscricao Estadual duplicada."""


def normalizar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
    texto = str(valor).strip()
    if not texto:
        raise InscricaoEstadualDadosInvalidosError(f"{nome_campo} e obrigatorio.")
    return texto


def normalizar_uf(uf: str) -> str:
    try:
        valor = normalizar_uf_compartilhada(uf)
    except ValueError as erro:
        raise InscricaoEstadualDadosInvalidosError(str(erro)) from erro
    if valor is None:
        raise InscricaoEstadualDadosInvalidosError("UF e obrigatoria.")
    return valor


class InscricaoEstadualService:
    """Coordena operacoes de aplicacao relacionadas a Inscricao Estadual."""

    def __init__(self, sessao: Session):
        self.sessao = sessao
        self.empresas = EmpresaRepository(sessao)
        self.repository = InscricaoEstadualRepository(sessao)

    def criar_inscricao_estadual(
        self,
        *,
        empresa_id: int,
        uf: str,
        inscricao_estadual: str,
        situacao: str | None = None,
        data_inicio: date | None = None,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> InscricaoEstadual:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")

        uf_normalizada = normalizar_uf(uf)
        ie_normalizada = normalizar_texto_obrigatorio(
            inscricao_estadual, "Inscricao estadual"
        )

        if self.repository.buscar_duplicada(empresa_id, uf_normalizada, ie_normalizada):
            raise InscricaoEstadualJaExisteError("Inscricao estadual ja cadastrada para esta empresa e UF.")

        try:
            inscricao = self.repository.criar_inscricao_estadual(
                empresa_id=empresa_id,
                uf=uf_normalizada,
                inscricao_estadual=ie_normalizada,
                situacao=situacao.strip() if situacao else None,
                data_inicio=data_inicio,
                data_fim=data_fim,
                observacoes=observacoes.strip() if observacoes else None,
            )
            self.sessao.commit()
            self.sessao.refresh(inscricao)
            return inscricao
        except IntegrityError as erro:
            self.sessao.rollback()
            raise InscricaoEstadualJaExisteError(
                "Inscricao estadual ja cadastrada para esta empresa e UF."
            ) from erro

    def listar_por_empresa(self, empresa_id: int) -> list[InscricaoEstadual]:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        return self.repository.listar_por_empresa(empresa_id)
