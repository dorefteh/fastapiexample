"""create posts table

Revision ID: a9f2e38bef29
Revises: 
Create Date: 2022-03-18 17:12:57.739535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9f2e38bef29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    #создает таблицу пост со столбцами id и title
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
