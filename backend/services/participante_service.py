"""Servico de aplicacao para Participante."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.models.participante import Participante
from backend.repositories.empresa_repository import EmpresaRepository
from backend.repositories.participante_repository import ParticipanteRepository
from backend.services.empresa_service import EmpresaNaoEncontradaError
from backend.utils.documentos import normalizar_documento, normalizar_tipo_pessoa, validar_documento_estrutural
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada

PAPEIS_PARTICIPANTE = {"cliente", "fornecedor", "prestador", "tomador", "transportadora", "outros"}


class ParticipanteDadosInvalidosError(Exception):
    """Erro para dados invalidos de Participante."""


class ParticipanteJaExisteError(Exception):
    """Erro para Participante duplicado no contexto da Empresa."""


class ParticipanteNaoEncontradoError(Exception):
    """Erro para Participante nao encontrado."""


def normalizar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
    texto = str(valor).strip()
    if not texto:
        raise ParticipanteDadosInvalidosError(f"{nome_campo} e obrigatorio.")
    return texto


def normalizar_texto_opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None


def normalizar_papeis(papeis: list[str]) -> list[str]:
    if not papeis:
        raise ParticipanteDadosInvalidosError("Informe pelo menos um papel do participante.")
    papeis_normalizados: list[str] = []
    for papel in papeis:
        papel_normalizado = str(papel).strip().lower()
        if not papel_normalizado:
            continue
        if papel_normalizado not in PAPEIS_PARTICIPANTE:
            raise ParticipanteDadosInvalidosError("Papel de participante invalido.")
        if papel_normalizado not in papeis_normalizados:
            papeis_normalizados.append(papel_normalizado)
    if not papeis_normalizados:
        raise ParticipanteDadosInvalidosError("Informe pelo menos um papel do participante.")
    return papeis_normalizados


def normalizar_uf(uf: str | None) -> str | None:
    try:
        return normalizar_uf_compartilhada(uf)
    except ValueError as erro:
        raise ParticipanteDadosInvalidosError(str(erro)) from erro


def validar_documento_para_busca(cpf_cnpj: str) -> str:
    documento = normalizar_documento(cpf_cnpj)
    if not documento:
        raise ParticipanteDadosInvalidosError("CPF/CNPJ e obrigatorio.")
    if len(documento) not in (11, 14):
        raise ParticipanteDadosInvalidosError("CPF/CNPJ deve conter 11 ou 14 digitos.")
    return documento


class ParticipanteService:
    """Coordena operacoes de aplicacao relacionadas a Participante."""

    def __init__(self, sessao: Session):
        self.sessao = sessao
        self.empresas = EmpresaRepository(sessao)
        self.repository = ParticipanteRepository(sessao)

    def criar_participante(
        self,
        *,
        empresa_id: int,
        tipo_pessoa: str,
        cpf_cnpj: str,
        razao_social_nome: str,
        papeis: list[str],
        nome_fantasia: str | None = None,
        inscricao_estadual: str | None = None,
        inscricao_municipal: str | None = None,
        email: str | None = None,
        telefone: str | None = None,
        cep: str | None = None,
        logradouro: str | None = None,
        numero: str | None = None,
        complemento: str | None = None,
        bairro: str | None = None,
        municipio: str | None = None,
        uf: str | None = None,
        situacao: str | None = None,
    ) -> Participante:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        try:
            tipo_pessoa_normalizado = normalizar_tipo_pessoa(tipo_pessoa)
            documento_normalizado = validar_documento_estrutural(tipo_pessoa_normalizado, cpf_cnpj)
        except ValueError as erro:
            raise ParticipanteDadosInvalidosError(str(erro)) from erro

        razao_social_nome_normalizado = normalizar_texto_obrigatorio(razao_social_nome, "Razao social/nome")
        papeis_normalizados = normalizar_papeis(papeis)
        uf_normalizada = normalizar_uf(uf)

        if self.repository.buscar_duplicado(empresa_id, documento_normalizado):
            raise ParticipanteJaExisteError("Participante ja cadastrado para esta empresa.")

        try:
            participante = self.repository.criar_participante(
                empresa_id=empresa_id,
                tipo_pessoa=tipo_pessoa_normalizado,
                cpf_cnpj=documento_normalizado,
                razao_social_nome=razao_social_nome_normalizado,
                nome_fantasia=normalizar_texto_opcional(nome_fantasia),
                inscricao_estadual=normalizar_texto_opcional(inscricao_estadual),
                inscricao_municipal=normalizar_texto_opcional(inscricao_municipal),
                email=normalizar_texto_opcional(email),
                telefone=normalizar_texto_opcional(telefone),
                cep=normalizar_texto_opcional(cep),
                logradouro=normalizar_texto_opcional(logradouro),
                numero=normalizar_texto_opcional(numero),
                complemento=normalizar_texto_opcional(complemento),
                bairro=normalizar_texto_opcional(bairro),
                municipio=normalizar_texto_opcional(municipio),
                uf=uf_normalizada,
                situacao=normalizar_texto_opcional(situacao),
                papeis=papeis_normalizados,
            )
            self.sessao.commit()
            self.sessao.refresh(participante)
            return participante
        except IntegrityError as erro:
            self.sessao.rollback()
            raise ParticipanteJaExisteError("Participante ja cadastrado para esta empresa.") from erro

    def listar_por_empresa(self, empresa_id: int) -> list[Participante]:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        return self.repository.listar_por_empresa(empresa_id)

    def obter_por_id(self, empresa_id: int, participante_id: int) -> Participante:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        participante = self.repository.buscar_por_id(empresa_id, participante_id)
        if participante is None:
            raise ParticipanteNaoEncontradoError("Participante nao encontrado.")
        return participante

    def obter_por_cpf_cnpj(self, empresa_id: int, cpf_cnpj: str) -> Participante:
        if self.empresas.buscar_empresa_por_id(empresa_id) is None:
            raise EmpresaNaoEncontradaError("Empresa nao encontrada.")
        documento_normalizado = validar_documento_para_busca(cpf_cnpj)
        participante = self.repository.buscar_por_cpf_cnpj(empresa_id, documento_normalizado)
        if participante is None:
            raise ParticipanteNaoEncontradoError("Participante nao encontrado.")
        return participante
