"""Added prefil column in Activity

Revision ID: b89e8100e204
Revises: efdc45fc6149
Create Date: 2021-05-06 22:15:51.254790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b89e8100e204'
down_revision = 'efdc45fc6149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prefil', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.drop_column('prefil')

    # ### end Alembic commands ###