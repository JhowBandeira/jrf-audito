"""Model de inscricao estadual vinculada a Empresa."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class InscricaoEstadual(Base):
    """Inscricao Estadual pertencente a uma Empresa."""

    __tablename__ = "inscricoes_estaduais"
    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "uf",
            "inscricao_estadual",
            name="uq_inscricoes_estaduais_empresa_uf_ie",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    uf: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    inscricao_estadual: Mapped[str] = mapped_column(String(40), nullable=False)
    situacao: Mapped[str | None] = mapped_column(String(40), nullable=True)
    data_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    empresa = relationship("Empresa", back_populates="inscricoes_estaduais")
