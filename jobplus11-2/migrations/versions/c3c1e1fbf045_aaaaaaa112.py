"""aaaaaaa112

Revision ID: c3c1e1fbf045
Revises: e80aa02d84aa
Create Date: 2019-05-04 20:12:56.074340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c1e1fbf045'
down_revision = 'e80aa02d84aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('job_ibfk_1', 'job', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('job_ibfk_1', 'job', 'user', ['id'], ['id'])
    # ### end Alembic commands ###
