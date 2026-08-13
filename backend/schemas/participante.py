"""Schemas HTTP para Participante."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from backend.utils.documentos import normalizar_tipo_pessoa, validar_documento_estrutural
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class TipoPessoa(str, Enum):
    """Valores aceitos para tipo de pessoa."""

    PF = "PF"
    PJ = "PJ"


class PapelParticipante(str, Enum):
    """Papeis aceitos para um participante."""

    cliente = "cliente"
    fornecedor = "fornecedor"
    prestador = "prestador"
    tomador = "tomador"
    transportadora = "transportadora"
    outros = "outros"


class ParticipanteCreate(BaseModel):
    """Dados aceitos para criar um participante via API."""

    model_config = ConfigDict(use_enum_values=True)

    tipo_pessoa: TipoPessoa
    cpf_cnpj: str = Field(..., min_length=1, max_length=18)
    razao_social_nome: str = Field(..., min_length=1, max_length=255)
    papeis: list[PapelParticipante] = Field(..., min_length=1)
    nome_fantasia: str | None = Field(default=None, max_length=255)
    inscricao_estadual: str | None = Field(default=None, max_length=40)
    inscricao_municipal: str | None = Field(default=None, max_length=40)
    email: str | None = Field(default=None, max_length=255)
    telefone: str | None = Field(default=None, max_length=40)
    cep: str | None = Field(default=None, max_length=20)
    logradouro: str | None = Field(default=None, max_length=255)
    numero: str | None = Field(default=None, max_length=30)
    complemento: str | None = Field(default=None, max_length=120)
    bairro: str | None = Field(default=None, max_length=120)
    municipio: str | None = Field(default=None, max_length=120)
    uf: str | None = Field(default=None, max_length=2)
    situacao: str | None = Field(default=None, max_length=40)

    @model_validator(mode="after")
    def validar_documento_por_tipo(self) -> "ParticipanteCreate":
        try:
            tipo_pessoa = normalizar_tipo_pessoa(self.tipo_pessoa)
            self.cpf_cnpj = validar_documento_estrutural(tipo_pessoa, self.cpf_cnpj)
            self.tipo_pessoa = tipo_pessoa
        except ValueError as erro:
            raise ValueError(str(erro)) from erro
        return self

    @field_validator("razao_social_nome")
    @classmethod
    def validar_razao_social_nome(cls, valor: str) -> str:
        valor_normalizado = valor.strip()
        if not valor_normalizado:
            raise ValueError("Razao social/nome e obrigatorio.")
        return valor_normalizado

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, valor: str | None) -> str | None:
        try:
            return normalizar_uf_compartilhada(valor)
        except ValueError as erro:
            raise ValueError(str(erro)) from erro


class ParticipanteResponse(BaseModel):
    """Dados devolvidos pela API para um participante."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    tipo_pessoa: str
    cpf_cnpj: str
    razao_social_nome: str
    papeis: list[str]
    nome_fantasia: str | None = None
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    email: str | None = None
    telefone: str | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    uf: str | None = None
    situacao: str | None = None
    criado_em: datetime
    atualizado_em: datetime

    @model_validator(mode="before")
    @classmethod
    def extrair_papeis(cls, valor: Any) -> Any:
        if hasattr(valor, "papeis"):
            campos = (
                "id", "empresa_id", "tipo_pessoa", "cpf_cnpj", "razao_social_nome",
                "nome_fantasia", "inscricao_estadual", "inscricao_municipal", "email",
                "telefone", "cep", "logradouro", "numero", "complemento", "bairro",
                "municipio", "uf", "situacao", "criado_em", "atualizado_em",
            )
            dados = {campo: getattr(valor, campo) for campo in campos}
            dados["papeis"] = [papel.papel for papel in valor.papeis]
            return dados
        return valor
