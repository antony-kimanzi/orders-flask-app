"""update order_ref

Revision ID: aa376e2bcca1
Revises: 0948af6eae2a
Create Date: 2025-01-19 20:36:36.775819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa376e2bcca1'
down_revision = '0948af6eae2a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_ref', sa.String(length=50), nullable=True))
        batch_op.create_unique_constraint('uq_order_ref', ['order_ref'])

def downgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint('uq_order_ref', type_='unique')
        batch_op.drop_column('order_ref')
