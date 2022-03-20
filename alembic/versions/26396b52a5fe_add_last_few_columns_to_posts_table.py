"""add last few columns to posts table

Revision ID: 26396b52a5fe
Revises: 6896d1a901d1
Create Date: 2022-03-19 12:59:15.551278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26396b52a5fe'
down_revision = '6896d1a901d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
        server_default=sa.text('NOW()'),))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
