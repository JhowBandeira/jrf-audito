"""criar inscricoes estaduais e municipais

Revision ID: 20260810_0002
Revises: 20260807_0001
Create Date: 2026-08-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0002"
down_revision: str | None = "20260807_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "inscricoes_estaduais",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("uf", sa.String(length=2), nullable=False),
        sa.Column("inscricao_estadual", sa.String(length=40), nullable=False),
        sa.Column("situacao", sa.String(length=40), nullable=True),
        sa.Column("data_inicio", sa.Date(), nullable=True),
        sa.Column("data_fim", sa.Date(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "empresa_id",
            "uf",
            "inscricao_estadual",
            name="uq_inscricoes_estaduais_empresa_uf_ie",
        ),
    )
    op.create_index(op.f("ix_inscricoes_estaduais_id"), "inscricoes_estaduais", ["id"], unique=False)
    op.create_index(op.f("ix_inscricoes_estaduais_empresa_id"), "inscricoes_estaduais", ["empresa_id"], unique=False)
    op.create_index(op.f("ix_inscricoes_estaduais_uf"), "inscricoes_estaduais", ["uf"], unique=False)

    op.create_table(
        "inscricoes_municipais",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("municipio", sa.String(length=120), nullable=False),
        sa.Column("uf", sa.String(length=2), nullable=False),
        sa.Column("inscricao_municipal", sa.String(length=40), nullable=False),
        sa.Column("situacao", sa.String(length=40), nullable=True),
        sa.Column("data_inicio", sa.Date(), nullable=True),
        sa.Column("data_fim", sa.Date(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "empresa_id",
            "municipio",
            "uf",
            "inscricao_municipal",
            name="uq_inscricoes_municipais_empresa_municipio_uf_im",
        ),
    )
    op.create_index(op.f("ix_inscricoes_municipais_id"), "inscricoes_municipais", ["id"], unique=False)
    op.create_index(op.f("ix_inscricoes_municipais_empresa_id"), "inscricoes_municipais", ["empresa_id"], unique=False)
    op.create_index(op.f("ix_inscricoes_municipais_municipio"), "inscricoes_municipais", ["municipio"], unique=False)
    op.create_index(op.f("ix_inscricoes_municipais_uf"), "inscricoes_municipais", ["uf"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_inscricoes_municipais_uf"), table_name="inscricoes_municipais")
    op.drop_index(op.f("ix_inscricoes_municipais_municipio"), table_name="inscricoes_municipais")
    op.drop_index(op.f("ix_inscricoes_municipais_empresa_id"), table_name="inscricoes_municipais")
    op.drop_index(op.f("ix_inscricoes_municipais_id"), table_name="inscricoes_municipais")
    op.drop_table("inscricoes_municipais")
    op.drop_index(op.f("ix_inscricoes_estaduais_uf"), table_name="inscricoes_estaduais")
    op.drop_index(op.f("ix_inscricoes_estaduais_empresa_id"), table_name="inscricoes_estaduais")
    op.drop_index(op.f("ix_inscricoes_estaduais_id"), table_name="inscricoes_estaduais")
    op.drop_table("inscricoes_estaduais")
