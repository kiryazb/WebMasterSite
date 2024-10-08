"""add last update date fiend to user query count

Revision ID: 788ead7f5c11
Revises: 4ef8930bfeb7
Create Date: 2024-08-29 20:04:12.586345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '788ead7f5c11'
down_revision: Union[str, None] = '4ef8930bfeb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_query_count', sa.Column('last_update_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_query_count', 'last_update_date')
    # ### end Alembic commands ###
