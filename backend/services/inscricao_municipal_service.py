"""Servico de aplicacao para Inscricao Municipal."""

from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.models.inscricao_municipal import InscricaoMunicipal
from backend.repositories.empresa_repository import EmpresaRepository
from backend.repositories.inscricao_municipal_repository import InscricaoMunicipalRepository
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class InscricaoMunicipalDadosInvalidosError(Exception):
    """Erro para dados invalidos de Inscricao Municipal."""


class InscricaoMunicipalJaExisteError(Exception):
    """Erro para Inscricao Municipal duplicada."""


def normalizar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
    texto = str(valor).strip()
    if not texto:
        raise InscricaoMunicipalDadosInvalidosError(f"{nome_campo} e obrigatorio.")
    return texto


def normalizar_uf(uf: str) -> str:
    try:
        valor = normalizar_uf_compartilhada(uf)
    except ValueError as erro:
        raise InscricaoMunicipalDadosInvalidosError(str(erro)) from erro
    if valor is None:
        raise InscricaoMunicipalDadosInvalidosError("UF e obrigatoria.")
    return valor


class InscricaoMunicipalService:
    """Coordena operacoes de aplicacao relacionadas a Inscricao Municipal."""

    def __init__(self, sessao: Session):
        self.sessao = sessao
        self.empresas = EmpresaRepository(sessao)
        self.repository = InscricaoMunicipalRepository(sessao)

    def criar_inscricao_municipal(
        self,
        *,
        empresa_id: int,
        municipio: str,
        uf: str,
        inscricao_municipal: str,
        situacao: str | None = None,
        data_inicio: date | None = None,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> InscricaoMunicipal:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")

        municipio_normalizado = normalizar_texto_obrigatorio(municipio, "Municipio")
        uf_normalizada = normalizar_uf(uf)
        im_normalizada = normalizar_texto_obrigatorio(
            inscricao_municipal, "Inscricao municipal"
        )

        if self.repository.buscar_duplicada(
            empresa_id, municipio_normalizado, uf_normalizada, im_normalizada
        ):
            raise InscricaoMunicipalJaExisteError("Inscricao municipal ja cadastrada para esta empresa, municipio e UF.")

        try:
            inscricao = self.repository.criar_inscricao_municipal(
                empresa_id=empresa_id,
                municipio=municipio_normalizado,
                uf=uf_normalizada,
                inscricao_municipal=im_normalizada,
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
            raise InscricaoMunicipalJaExisteError(
                "Inscricao municipal ja cadastrada para esta empresa, municipio e UF."
            ) from erro

    def listar_por_empresa(self, empresa_id: int) -> list[InscricaoMunicipal]:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        return self.repository.listar_por_empresa(empresa_id)
