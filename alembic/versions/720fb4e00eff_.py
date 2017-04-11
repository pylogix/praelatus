"""empty message

Revision ID: 720fb4e00eff
Revises: 57eefc0ee95b
Create Date: 2017-04-11 15:42:35.349172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '720fb4e00eff'
down_revision = '57eefc0ee95b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'labels', ['name'])
    op.add_column('permission_scheme_permissions', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('permission_scheme_permissions_permission_scheme_id_role_id__key', 'permission_scheme_permissions', type_='unique')
    op.create_unique_constraint(None, 'statuses', ['name'])
    op.create_unique_constraint(None, 'ticket_types', ['name'])
    op.create_unique_constraint(None, 'tickets', ['key'])
    op.add_column('users_roles', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('users_roles_user_id_role_id_key', 'users_roles', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_roles_user_id_role_id_key', 'users_roles', ['user_id', 'role_id'])
    op.drop_column('users_roles', 'id')
    op.drop_constraint(None, 'tickets', type_='unique')
    op.drop_constraint(None, 'ticket_types', type_='unique')
    op.drop_constraint(None, 'statuses', type_='unique')
    op.create_unique_constraint('permission_scheme_permissions_permission_scheme_id_role_id__key', 'permission_scheme_permissions', ['permission_scheme_id', 'role_id', 'permission_id'])
    op.drop_column('permission_scheme_permissions', 'id')
    op.drop_constraint(None, 'labels', type_='unique')
    # ### end Alembic commands ###
