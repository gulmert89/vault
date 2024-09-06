"""Create a new column 'apt_num'

Revision ID: 04e89fb40af0
Revises: 725815baab6e
Create Date: 2023-06-01 19:43:15.796922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04e89fb40af0'
down_revision = '725815baab6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="address",
        column=sa.Column(name="apt_num", type_=sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("address", "apt_num")
