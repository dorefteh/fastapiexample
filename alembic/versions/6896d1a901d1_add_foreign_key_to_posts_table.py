"""add foreign-key to posts table

Revision ID: 6896d1a901d1
Revises: d0b48f6b1c40
Create Date: 2022-03-19 12:26:03.662675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6896d1a901d1'
down_revision = 'd0b48f6b1c40'
branch_labels = None
depends_on = None

'''Последовательность аргументов метода create_foreign_key:
1название ключа, 2начальная таблица(в которой будет находится столбец с внешним ключем),
3таблица на которую ссылается ключ, 4столбец для присвоения, 
5столбец на котороц ссылаются, 6выравнивание при удалении ключа
'''
def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", 
    referent_table="users", local_cols=['owner_id'], remote_cols=['id'], 
    ondelete="CASCADE")
    pass


'''Удаляем ограничение указывая название ключа а также столбец'''
def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
