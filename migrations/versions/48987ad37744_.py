"""empty message

Revision ID: 48987ad37744
Revises: 475737162b34
Create Date: 2020-07-11 14:48:52.304595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48987ad37744'
down_revision = '475737162b34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'id')
    # ### end Alembic commands ###
