"""Model inicial de empresa do JRF-Audito."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Empresa(Base):
    """Cadastro minimo de empresa, sempre individualizado por CNPJ."""

    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cnpj: Mapped[str] = mapped_column(String(14), nullable=False, unique=True, index=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_fantasia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cnpj_raiz: Mapped[str | None] = mapped_column(String(8), nullable=True, index=True)
    tipo_estabelecimento: Mapped[str | None] = mapped_column(String(20), nullable=True)
    regime_tributario: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cnae_principal: Mapped[str | None] = mapped_column(String(20), nullable=True)
    municipio: Mapped[str | None] = mapped_column(String(120), nullable=True)
    uf: Mapped[str | None] = mapped_column(String(2), nullable=True)
    situacao: Mapped[str | None] = mapped_column(String(40), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    inscricoes_estaduais = relationship("InscricaoEstadual", back_populates="empresa", cascade="all, delete-orphan")
    inscricoes_municipais = relationship("InscricaoMunicipal", back_populates="empresa", cascade="all, delete-orphan")
    participantes = relationship("Participante", back_populates="empresa", cascade="all, delete-orphan")
