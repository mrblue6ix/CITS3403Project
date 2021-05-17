"""empty message

Revision ID: 66cdf574de7c
Revises: bf69ce5fcd5d
Create Date: 2021-05-09 22:24:19.406771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66cdf574de7c'
down_revision = 'bf69ce5fcd5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('num_correct')
        batch_op.drop_column('num_incorrect')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num_incorrect', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('num_correct', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
