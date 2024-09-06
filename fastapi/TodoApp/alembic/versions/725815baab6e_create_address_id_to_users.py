"""Create address_id to users

Revision ID: 725815baab6e
Revises: d6ea575ac07c
Create Date: 2023-06-01 18:55:43.786956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '725815baab6e'
down_revision = 'd6ea575ac07c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="users",
        column=sa.Column(
            name="address_id",
            type_=sa.Integer(),
            nullable=True
        )
    )
    op.create_foreign_key(
        constraint_name="address_users_fk",
        source_table="users",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="address_users_fk",
        table_name="users"
    )
    op.drop_column(
        table_name="users",
        column_name="address_id"
    )
