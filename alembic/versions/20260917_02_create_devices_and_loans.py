"""create devices and loans tables

Revision ID: 20260917_02
Revises: 20260917_01
Create Date: 2026-09-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260917_02"
down_revision: Union[str, Sequence[str], None] = "20260917_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("serial_number", sa.String(length=100), nullable=False),
        sa.Column("device_type", sa.String(length=50), nullable=False),
        sa.Column("brand", sa.String(length=100), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_devices_id", "devices", ["id"], unique=False)
    op.create_index("ix_devices_serial_number", "devices", ["serial_number"], unique=True)
    op.create_index("ix_devices_device_type", "devices", ["device_type"], unique=False)
    op.create_index("ix_devices_brand", "devices", ["brand"], unique=False)

    op.create_table(
        "loans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("loan_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("return_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint(
            "status IN ('active', 'returned', 'overdue')",
            name="ck_loans_status",
        ),
        sa.ForeignKeyConstraint(
            ["device_id"], ["devices.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_loans_id", "loans", ["id"], unique=False)
    op.create_index("ix_loans_user_id", "loans", ["user_id"], unique=False)
    op.create_index("ix_loans_device_id", "loans", ["device_id"], unique=False)
    op.create_index("ix_loans_status", "loans", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_loans_status", table_name="loans")
    op.drop_index("ix_loans_device_id", table_name="loans")
    op.drop_index("ix_loans_user_id", table_name="loans")
    op.drop_index("ix_loans_id", table_name="loans")
    op.drop_table("loans")
    op.drop_index("ix_devices_brand", table_name="devices")
    op.drop_index("ix_devices_device_type", table_name="devices")
    op.drop_index("ix_devices_serial_number", table_name="devices")
    op.drop_index("ix_devices_id", table_name="devices")
    op.drop_table("devices")
