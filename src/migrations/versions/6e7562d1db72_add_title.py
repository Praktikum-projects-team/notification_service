"""add title

Revision ID: 6e7562d1db72
Revises: 9809c779453b
Create Date: 2023-08-04 22:44:26.730004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e7562d1db72'
down_revision = '9809c779453b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('templates', sa.Column('title', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('templates', 'title')
