"""empty message

Revision ID: 57eefc0ee95b
Revises: baaf8ee271a4
Create Date: 2017-04-10 12:41:29.575873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57eefc0ee95b'
down_revision = 'baaf8ee271a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'projects', ['key'])
    op.create_unique_constraint(None, 'projects', ['name'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'projects', type_='unique')
    op.drop_constraint(None, 'projects', type_='unique')
    # ### end Alembic commands ###