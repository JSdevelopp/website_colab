"""empty message

Revision ID: 5fb2b6d949e6
Revises: 063502feb244
Create Date: 2023-08-23 13:33:16.714531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fb2b6d949e6'
down_revision = '063502feb244'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_dollars', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('quantity_count', sa.Integer(), nullable=True))
        batch_op.drop_index('ix_books_price')
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.INTEGER(), nullable=True))
        batch_op.create_index('ix_books_price', ['price'], unique=False)
        batch_op.drop_column('quantity_count')
        batch_op.drop_column('price_dollars')

    # ### end Alembic commands ###