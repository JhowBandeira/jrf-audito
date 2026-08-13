"""criar tabela empresas

Revision ID: 20260807_0001
Revises:
Create Date: 2026-08-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260807_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "empresas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cnpj", sa.String(length=14), nullable=False),
        sa.Column("razao_social", sa.String(length=255), nullable=False),
        sa.Column("nome_fantasia", sa.String(length=255), nullable=True),
        sa.Column("cnpj_raiz", sa.String(length=8), nullable=True),
        sa.Column("tipo_estabelecimento", sa.String(length=20), nullable=True),
        sa.Column("regime_tributario", sa.String(length=80), nullable=True),
        sa.Column("cnae_principal", sa.String(length=20), nullable=True),
        sa.Column("municipio", sa.String(length=120), nullable=True),
        sa.Column("uf", sa.String(length=2), nullable=True),
        sa.Column("situacao", sa.String(length=40), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cnpj", name="uq_empresas_cnpj"),
    )
    op.create_index(op.f("ix_empresas_id"), "empresas", ["id"], unique=False)
    op.create_index(op.f("ix_empresas_cnpj"), "empresas", ["cnpj"], unique=False)
    op.create_index(op.f("ix_empresas_cnpj_raiz"), "empresas", ["cnpj_raiz"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_empresas_cnpj_raiz"), table_name="empresas")
    op.drop_index(op.f("ix_empresas_cnpj"), table_name="empresas")
    op.drop_index(op.f("ix_empresas_id"), table_name="empresas")
    op.drop_table("empresas")
