""" delete logs tables

Revision ID: 5e1281e05d92
Revises: c25f17540c5c
Create Date: 2024-07-19 12:48:59.419775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5e1281e05d92'
down_revision = 'c25f17540c5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('update_logs_indicator')
    op.drop_table('update_logs_query')
    op.drop_table('update_logs_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('update_logs_url',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('update_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='update_logs_url_pkey')
    )
    op.create_table('update_logs_query',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('update_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='update_logs_query_pkey')
    )
    op.create_table('update_logs_indicator',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('update_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='update_logs_indicator_pkey')
    )
    # ### end Alembic commands ###
