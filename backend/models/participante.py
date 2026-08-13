"""Models de participante e papeis vinculados a Empresa."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Participante(Base):
    """Cadastro central de terceiros no contexto de uma Empresa."""

    __tablename__ = "participantes"
    __table_args__ = (
        UniqueConstraint("empresa_id", "cpf_cnpj", name="uq_participantes_empresa_cpf_cnpj"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False, index=True)
    tipo_pessoa: Mapped[str] = mapped_column(String(2), nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(String(14), nullable=False, index=True)
    razao_social_nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    nome_fantasia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    inscricao_estadual: Mapped[str | None] = mapped_column(String(40), nullable=True)
    inscricao_municipal: Mapped[str | None] = mapped_column(String(40), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    cep: Mapped[str | None] = mapped_column(String(20), nullable=True)
    logradouro: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(30), nullable=True)
    complemento: Mapped[str | None] = mapped_column(String(120), nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(120), nullable=True)
    municipio: Mapped[str | None] = mapped_column(String(120), nullable=True)
    uf: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    situacao: Mapped[str | None] = mapped_column(String(40), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    empresa = relationship("Empresa", back_populates="participantes")
    papeis = relationship("ParticipantePapel", back_populates="participante", cascade="all, delete-orphan")


class ParticipantePapel(Base):
    """Papel exercido por um participante dentro do contexto da empresa."""

    __tablename__ = "participantes_papeis"
    __table_args__ = (
        UniqueConstraint("participante_id", "papel", name="uq_participantes_papeis_participante_papel"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    participante_id: Mapped[int] = mapped_column(ForeignKey("participantes.id"), nullable=False, index=True)
    papel: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    participante = relationship("Participante", back_populates="papeis")
