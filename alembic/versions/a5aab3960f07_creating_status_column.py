"""creating status column

Revision ID: a5aab3960f07
Revises: 463c73b6229f
Create Date: 2023-07-20 14:50:22.556085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5aab3960f07'
down_revision = '463c73b6229f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('status', sa.Enum('created', 'cancelled', 'payed', 'processing', 'sent', 'delivered'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'status')
    # ### end Alembic commands ###