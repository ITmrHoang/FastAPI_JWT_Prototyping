"""update hashparss

Revision ID: 2c5cbc5ec078
Revises: 7fdc72b78c26
Create Date: 2024-03-22 08:13:24.205604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c5cbc5ec078'
down_revision: Union[str, None] = '7fdc72b78c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('_hashed_password', sa.String(), nullable=False))
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', '_hashed_password')
    # ### end Alembic commands ###
