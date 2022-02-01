"""create money stock table

Revision ID: 000f95cfe32d
Revises: 
Create Date: 2022-01-30 12:35:10.608023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000f95cfe32d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'moneystock',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Integer(), nullable=False, unique=True, index=True),
        sa.Column('type', sa.String()),
        sa.Column('amount', sa.Integer()),
    )


def downgrade():
    op.drop_table('MoneyStock')
