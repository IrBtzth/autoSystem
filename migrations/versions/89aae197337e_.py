"""empty message

Revision ID: 89aae197337e
Revises: 
Create Date: 2023-05-09 19:24:01.296327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89aae197337e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_project_data'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_data')
    # ### end Alembic commands ###
