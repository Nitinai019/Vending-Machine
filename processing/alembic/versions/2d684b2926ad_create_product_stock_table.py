"""create product stock table

Revision ID: 2d684b2926ad
Revises: 000f95cfe32d
Create Date: 2022-01-30 12:49:15.935367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d684b2926ad'
down_revision = '000f95cfe32d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'productstock',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Integer(), nullable=False, unique=True, index=True),
        sa.Column('price', sa.String()),
        sa.Column('amount', sa.Integer()),
    )


def downgrade():
    op.drop_table('productstock')
