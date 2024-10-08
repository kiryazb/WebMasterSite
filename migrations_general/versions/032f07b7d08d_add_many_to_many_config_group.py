"""add many to many Config-Group

Revision ID: 032f07b7d08d
Revises: 90cf6df62c39
Create Date: 2024-08-14 11:45:34.671802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '032f07b7d08d'
down_revision: Union[str, None] = '90cf6df62c39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_config_association',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('config_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['config_id'], ['config.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('group_id', 'config_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_config_association')
    op.drop_table('group')
    # ### end Alembic commands ###
