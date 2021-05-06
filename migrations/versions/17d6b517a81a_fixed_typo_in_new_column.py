"""Fixed typo in new column

Revision ID: 17d6b517a81a
Revises: b89e8100e204
Create Date: 2021-05-06 22:16:58.323265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17d6b517a81a'
down_revision = 'b89e8100e204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prefill', sa.Text(), nullable=True))
        batch_op.drop_column('prefil')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prefil', sa.TEXT(), nullable=True))
        batch_op.drop_column('prefill')

    # ### end Alembic commands ###