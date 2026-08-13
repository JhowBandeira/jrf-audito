"""Model de inscricao municipal vinculada a Empresa."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class InscricaoMunicipal(Base):
    """Inscricao Municipal pertencente a uma Empresa."""

    __tablename__ = "inscricoes_municipais"
    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "municipio",
            "uf",
            "inscricao_municipal",
            name="uq_inscricoes_municipais_empresa_municipio_uf_im",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    municipio: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    uf: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    inscricao_municipal: Mapped[str] = mapped_column(String(40), nullable=False)
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

    empresa = relationship("Empresa", back_populates="inscricoes_municipais")
