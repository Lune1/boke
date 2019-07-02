"""empty message

Revision ID: e6338e2960ed
Revises: f5de0343538f
Create Date: 2019-07-01 13:18:57.081635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6338e2960ed'
down_revision = 'f5de0343538f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mypress', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mypress', 'date')
    # ### end Alembic commands ###
