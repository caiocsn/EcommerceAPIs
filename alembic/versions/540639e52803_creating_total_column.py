"""creating total column

Revision ID: 540639e52803
Revises: a5aab3960f07
Create Date: 2023-07-21 03:30:00.929444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '540639e52803'
down_revision = 'a5aab3960f07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('total', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'total')
    # ### end Alembic commands ###