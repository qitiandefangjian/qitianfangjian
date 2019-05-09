"""sssssss2

Revision ID: b316bd2d7f14
Revises: 564ed74d4561
Create Date: 2019-05-01 23:34:28.579690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b316bd2d7f14'
down_revision = '564ed74d4561'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('state', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'state')
    # ### end Alembic commands ###
