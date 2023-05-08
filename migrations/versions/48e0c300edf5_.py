"""empty message

Revision ID: 48e0c300edf5
Revises: 
Create Date: 2023-05-06 09:03:06.877615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e0c300edf5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfs', schema=None) as batch_op:
        #batch_op.drop_constraint(None, type_='foreignkey')
        
        batch_op.drop_column('usersId')

    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_role_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_role_name'), type_='unique')

    with op.batch_alter_table('portfs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usersId', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['usersId'], ['id'])

    # ### end Alembic commands ###