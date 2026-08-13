"""Schemas HTTP para Empresa."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.services.empresa_service import normalizar_cnpj
from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class TipoEstabelecimento(str, Enum):
    """Valores aceitos para tipo de estabelecimento."""

    matriz = "matriz"
    filial = "filial"


class EmpresaCreate(BaseModel):
    """Dados aceitos para criar uma empresa via API."""

    model_config = ConfigDict(use_enum_values=True)

    cnpj: str = Field(..., min_length=1, max_length=18)
    razao_social: str = Field(..., min_length=1, max_length=255)
    nome_fantasia: str | None = Field(default=None, max_length=255)
    cnpj_raiz: str | None = Field(default=None, max_length=18)
    tipo_estabelecimento: TipoEstabelecimento | None = None
    regime_tributario: str | None = Field(default=None, max_length=80)
    cnae_principal: str | None = Field(default=None, max_length=20)
    municipio: str | None = Field(default=None, max_length=120)
    uf: str | None = Field(default=None, max_length=2)
    situacao: str | None = Field(default=None, max_length=40)

    @field_validator("cnpj")
    @classmethod
    def validar_cnpj_estrutural(cls, valor: str) -> str:
        cnpj = normalizar_cnpj(valor)
        if not cnpj:
            raise ValueError("CNPJ e obrigatorio.")
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve conter 14 digitos.")
        return cnpj

    @field_validator("razao_social")
    @classmethod
    def validar_razao_social(cls, valor: str) -> str:
        valor_normalizado = valor.strip()
        if not valor_normalizado:
            raise ValueError("Razao social e obrigatoria.")
        return valor_normalizado

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, valor: str | None) -> str | None:
        try:
            return normalizar_uf_compartilhada(valor)
        except ValueError as erro:
            raise ValueError(str(erro)) from erro


class EmpresaResponse(BaseModel):
    """Dados devolvidos pela API para uma empresa."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: str | None = None
    cnpj_raiz: str | None = None
    tipo_estabelecimento: str | None = None
    regime_tributario: str | None = None
    cnae_principal: str | None = None
    municipio: str | None = None
    uf: str | None = None
    situacao: str | None = None
    criado_em: datetime
    atualizado_em: datetime
