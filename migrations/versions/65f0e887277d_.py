"""empty message

Revision ID: 65f0e887277d
Revises: 218bf18152a6
Create Date: 2021-01-22 23:36:47.981381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f0e887277d'
down_revision = '218bf18152a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('media', 'caption',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'caption',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('message')
    # ### end Alembic commands ###
