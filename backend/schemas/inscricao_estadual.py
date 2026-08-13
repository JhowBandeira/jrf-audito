"""Schemas HTTP para Inscricao Estadual."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.utils.ufs import normalizar_uf as normalizar_uf_compartilhada


class InscricaoEstadualCreate(BaseModel):
    """Dados aceitos para criar uma Inscricao Estadual."""

    uf: str = Field(..., min_length=1, max_length=2)
    inscricao_estadual: str = Field(..., min_length=1, max_length=40)
    situacao: str | None = Field(default=None, max_length=40)
    data_inicio: date | None = None
    data_fim: date | None = None
    observacoes: str | None = None

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

    @field_validator("inscricao_estadual")
    @classmethod
    def validar_inscricao_estadual(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Inscricao estadual e obrigatoria.")
        return texto


class InscricaoEstadualResponse(BaseModel):
    """Dados devolvidos pela API para Inscricao Estadual."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    uf: str
    inscricao_estadual: str
    situacao: str | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    observacoes: str | None = None
    criado_em: datetime
    atualizado_em: datetime
