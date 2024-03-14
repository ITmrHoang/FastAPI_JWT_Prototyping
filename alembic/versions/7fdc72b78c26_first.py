"""first 

Revision ID: 7fdc72b78c26
Revises: 
Create Date: 2024-03-21 03:11:43.062673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7fdc72b78c26'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('salt', sa.String(length=16), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_supper_admin', sa.Boolean(), nullable=False),
    sa.Column('last_login', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('role_has_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_has_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_has_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_has_roles')
    op.drop_table('user_has_permissions')
    op.drop_table('role_has_permissions')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('permissions')
    # ### end Alembic commands ###
