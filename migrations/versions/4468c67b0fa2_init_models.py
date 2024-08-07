"""Init models

Revision ID: 4468c67b0fa2
Revises: 
Create Date: 2024-05-04 22:31:41.503036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4468c67b0fa2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metrics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('position', sa.Float(), nullable=False),
    sa.Column('ctr', sa.Float(), nullable=False),
    sa.Column('impression', sa.Float(), nullable=False),
    sa.Column('clicks', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('url',
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('url'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url')
    op.drop_table('metrics')
    # ### end Alembic commands ###
