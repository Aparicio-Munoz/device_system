"""add authentication fields to users

Revision ID: 20260917_03
Revises: 20260917_02
Create Date: 2026-09-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260917_03"
down_revision: Union[str, Sequence[str], None] = "20260917_02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DISABLED_PASSWORD_HASH = (
    "$2b$12$QxzgiKrYJP0Hzqj9EgQVGulPMTN556zCfWhq/k5Dg.eQgS1/bp5EW"
)


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE users SET hashed_password = :disabled_hash "
            "WHERE hashed_password IS NULL"
        ).bindparams(disabled_hash=DISABLED_PASSWORD_HASH)
    )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "hashed_password",
            existing_type=sa.String(length=255),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_column("users", "hashed_password")
