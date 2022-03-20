"""add contetnt column to posts table

Revision ID: eda6ce18cb52
Revises: a9f2e38bef29
Create Date: 2022-03-18 18:14:31.527772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eda6ce18cb52'
down_revision = 'a9f2e38bef29'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
