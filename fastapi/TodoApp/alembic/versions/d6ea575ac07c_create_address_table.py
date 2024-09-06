"""Create address table

Revision ID: d6ea575ac07c
Revises: 3c3edfa93236
Create Date: 2023-06-01 18:44:33.891387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6ea575ac07c'
down_revision = '3c3edfa93236'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "address",
        sa.Column(
            name="id",
            type_=sa.Integer(),
            nullable=False,
            primary_key=True
        ),
        sa.Column(
            name="address1",
            type_=sa.String(),
            nullable=False
        ),
        sa.Column(
            name="address2",
            type_=sa.String(),
            nullable=False
        ),
        sa.Column(
            name="city",
            type_=sa.String(),
            nullable=False
        ),
        sa.Column(
            name="state",
            type_=sa.String(),
            nullable=False
        ),
        sa.Column(
            name="country",
            type_=sa.String(),
            nullable=False
        ),
        sa.Column(
            name="postalcode",
            type_=sa.String(),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_table(table_name="address")
