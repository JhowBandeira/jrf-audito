"""Servico de aplicacao para Empresa."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.models.empresa import Empresa
from backend.repositories.empresa_repository import EmpresaRepository
from backend.utils.documentos import normalizar_documento, validar_documento_estrutural
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada

TIPOS_ESTABELECIMENTO = {"matriz", "filial"}


class EmpresaDadosInvalidosError(Exception):
    """Erro de aplicacao para dados cadastrais invalidos de Empresa."""


class EmpresaJaExisteError(Exception):
    """Erro de aplicacao para tentativa de cadastrar CNPJ duplicado."""


class EmpresaNaoEncontradaError(Exception):
    """Erro de aplicacao para Empresa nao encontrada."""


def normalizar_cnpj(cnpj: str) -> str:
    """Remove caracteres nao numericos do CNPJ, sem validar seus digitos."""
    return normalizar_documento(cnpj)


def validar_cnpj(cnpj: str) -> str:
    """Normaliza e valida estrutura basica do CNPJ."""
    try:
        return validar_documento_estrutural("PJ", cnpj)
    except ValueError as erro:
        raise EmpresaDadosInvalidosError(str(erro)) from erro


def normalizar_razao_social(razao_social: str) -> str:
    """Remove espacos das extremidades e exige conteudo."""
    valor = str(razao_social).strip()
    if not valor:
        raise EmpresaDadosInvalidosError("Razao social e obrigatoria.")
    return valor


def normalizar_tipo_estabelecimento(tipo_estabelecimento: str | None) -> str | None:
    """Padroniza tipo de estabelecimento como matriz ou filial."""
    if tipo_estabelecimento is None:
        return None
    valor = str(tipo_estabelecimento).strip().lower()
    if not valor:
        return None
    if valor not in TIPOS_ESTABELECIMENTO:
        raise EmpresaDadosInvalidosError("Tipo de estabelecimento deve ser matriz ou filial.")
    return valor


def normalizar_uf(uf: str | None) -> str | None:
    """Padroniza UF em maiusculo e valida siglas brasileiras."""
    try:
        return normalizar_uf_compartilhada(uf)
    except ValueError as erro:
        raise EmpresaDadosInvalidosError(str(erro)) from erro


class EmpresaService:
    """Coordena operacoes de aplicacao relacionadas a Empresa."""

    def __init__(self, sessao: Session):
        self.sessao = sessao
        self.repository = EmpresaRepository(sessao)

    def criar_empresa(
        self,
        *,
        cnpj: str,
        razao_social: str,
        nome_fantasia: str | None = None,
        cnpj_raiz: str | None = None,
        tipo_estabelecimento: str | None = None,
        regime_tributario: str | None = None,
        cnae_principal: str | None = None,
        municipio: str | None = None,
        uf: str | None = None,
        situacao: str | None = None,
    ) -> Empresa:
        cnpj_normalizado = validar_cnpj(cnpj)
        cnpj_raiz_normalizado = normalizar_cnpj(cnpj_raiz) if cnpj_raiz else None
        razao_social_normalizada = normalizar_razao_social(razao_social)
        tipo_estabelecimento_normalizado = normalizar_tipo_estabelecimento(tipo_estabelecimento)
        uf_normalizada = normalizar_uf(uf)

        if self.repository.buscar_empresa_por_cnpj(cnpj_normalizado):
            raise EmpresaJaExisteError(f"Empresa com CNPJ {cnpj_normalizado} ja cadastrada.")

        try:
            empresa = self.repository.criar_empresa(
                cnpj=cnpj_normalizado,
                razao_social=razao_social_normalizada,
                nome_fantasia=nome_fantasia.strip() if nome_fantasia else None,
                cnpj_raiz=cnpj_raiz_normalizado,
                tipo_estabelecimento=tipo_estabelecimento_normalizado,
                regime_tributario=regime_tributario.strip() if regime_tributario else None,
                cnae_principal=cnae_principal.strip() if cnae_principal else None,
                municipio=municipio.strip() if municipio else None,
                uf=uf_normalizada,
                situacao=situacao.strip() if situacao else None,
            )
            self.sessao.commit()
            self.sessao.refresh(empresa)
            return empresa
        except IntegrityError as erro:
            self.sessao.rollback()
            raise EmpresaJaExisteError(f"Empresa com CNPJ {cnpj_normalizado} ja cadastrada.") from erro

    def buscar_empresa_por_id(self, empresa_id: int) -> Empresa | None:
        return self.repository.buscar_empresa_por_id(empresa_id)

    def obter_empresa_por_id(self, empresa_id: int) -> Empresa:
        empresa = self.buscar_empresa_por_id(empresa_id)
        if empresa is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        return empresa

    def buscar_empresa_por_cnpj(self, cnpj: str) -> Empresa | None:
        return self.repository.buscar_empresa_por_cnpj(validar_cnpj(cnpj))

    def obter_empresa_por_cnpj(self, cnpj: str) -> Empresa:
        empresa = self.buscar_empresa_por_cnpj(cnpj)
        if empresa is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        return empresa

    def listar_empresas(self) -> list[Empresa]:
        return self.repository.listar_empresas()
