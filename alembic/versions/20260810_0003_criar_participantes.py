"""criar participantes

Revision ID: 20260810_0003
Revises: 20260810_0002
Create Date: 2026-08-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0003"
down_revision: str | None = "20260810_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "participantes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("tipo_pessoa", sa.String(length=2), nullable=False),
        sa.Column("cpf_cnpj", sa.String(length=14), nullable=False),
        sa.Column("razao_social_nome", sa.String(length=255), nullable=False),
        sa.Column("nome_fantasia", sa.String(length=255), nullable=True),
        sa.Column("inscricao_estadual", sa.String(length=40), nullable=True),
        sa.Column("inscricao_municipal", sa.String(length=40), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("telefone", sa.String(length=40), nullable=True),
        sa.Column("cep", sa.String(length=20), nullable=True),
        sa.Column("logradouro", sa.String(length=255), nullable=True),
        sa.Column("numero", sa.String(length=30), nullable=True),
        sa.Column("complemento", sa.String(length=120), nullable=True),
        sa.Column("bairro", sa.String(length=120), nullable=True),
        sa.Column("municipio", sa.String(length=120), nullable=True),
        sa.Column("uf", sa.String(length=2), nullable=True),
        sa.Column("situacao", sa.String(length=40), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("empresa_id", "cpf_cnpj", name="uq_participantes_empresa_cpf_cnpj"),
    )
    op.create_index(op.f("ix_participantes_id"), "participantes", ["id"], unique=False)
    op.create_index(op.f("ix_participantes_empresa_id"), "participantes", ["empresa_id"], unique=False)
    op.create_index(op.f("ix_participantes_cpf_cnpj"), "participantes", ["cpf_cnpj"], unique=False)
    op.create_index(op.f("ix_participantes_razao_social_nome"), "participantes", ["razao_social_nome"], unique=False)
    op.create_index(op.f("ix_participantes_uf"), "participantes", ["uf"], unique=False)

    op.create_table(
        "participantes_papeis",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("participante_id", sa.Integer(), nullable=False),
        sa.Column("papel", sa.String(length=40), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["participante_id"], ["participantes.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("participante_id", "papel", name="uq_participantes_papeis_participante_papel"),
    )
    op.create_index(op.f("ix_participantes_papeis_id"), "participantes_papeis", ["id"], unique=False)
    op.create_index(op.f("ix_participantes_papeis_participante_id"), "participantes_papeis", ["participante_id"], unique=False)
    op.create_index(op.f("ix_participantes_papeis_papel"), "participantes_papeis", ["papel"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_participantes_papeis_papel"), table_name="participantes_papeis")
    op.drop_index(op.f("ix_participantes_papeis_participante_id"), table_name="participantes_papeis")
    op.drop_index(op.f("ix_participantes_papeis_id"), table_name="participantes_papeis")
    op.drop_table("participantes_papeis")
    op.drop_index(op.f("ix_participantes_uf"), table_name="participantes")
    op.drop_index(op.f("ix_participantes_razao_social_nome"), table_name="participantes")
    op.drop_index(op.f("ix_participantes_cpf_cnpj"), table_name="participantes")
    op.drop_index(op.f("ix_participantes_empresa_id"), table_name="participantes")
    op.drop_index(op.f("ix_participantes_id"), table_name="participantes")
    op.drop_table("participantes")
