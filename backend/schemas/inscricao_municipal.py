"""Schemas HTTP para Inscricao Municipal."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class InscricaoMunicipalCreate(BaseModel):
    """Dados aceitos para criar uma Inscricao Municipal."""

    municipio: str = Field(..., min_length=1, max_length=120)
    uf: str = Field(..., min_length=1, max_length=2)
    inscricao_municipal: str = Field(..., min_length=1, max_length=40)
    situacao: str | None = Field(default=None, max_length=40)
    data_inicio: date | None = None
    data_fim: date | None = None
    observacoes: str | None = None

    @field_validator("municipio")
    @classmethod
    def validar_municipio(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Municipio e obrigatorio.")
        return texto

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, valor: str) -> str:
        try:
            uf = normalizar_uf_compartilhada(valor)
        except ValueError as erro:
            raise ValueError(str(erro)) from erro
        if uf is None:
            raise ValueError("UF e obrigatoria.")
        return uf

    @field_validator("inscricao_municipal")
    @classmethod
    def validar_inscricao_municipal(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Inscricao municipal e obrigatoria.")
        return texto


class InscricaoMunicipalResponse(BaseModel):
    """Dados devolvidos pela API para Inscricao Municipal."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    municipio: str
    uf: str
    inscricao_municipal: str
    situacao: str | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    observacoes: str | None = None
    criado_em: datetime
    atualizado_em: datetime
