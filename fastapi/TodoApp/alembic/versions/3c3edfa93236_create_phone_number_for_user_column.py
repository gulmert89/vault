"""Create phone number for user column

Revision ID: 3c3edfa93236
Revises: 
Create Date: 2023-06-01 18:19:43.578974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c3edfa93236'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="users",
        column=sa.Column(
            name="phone_number",
            type_=sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column(
        table_name="users",
        column_name="phone_number"
    )
