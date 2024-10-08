"""add group and config field

Revision ID: aebb936cffc4
Revises: fd25da4e8425
Create Date: 2024-08-26 22:24:13.037460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aebb936cffc4'
down_revision: Union[str, None] = 'fd25da4e8425'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('list', sa.Column('group', sa.Integer(), nullable=False))
    op.add_column('list', sa.Column('config', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'list', 'config', ['config'], ['id'])
    op.create_foreign_key(None, 'list', 'group', ['group'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'list', type_='foreignkey')
    op.drop_constraint(None, 'list', type_='foreignkey')
    op.drop_column('list', 'config')
    op.drop_column('list', 'group')
    # ### end Alembic commands ###
