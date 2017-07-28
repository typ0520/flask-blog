"""add email

Revision ID: 44bc1a7c4eec
Revises: 088c2546008e
Create Date: 2017-07-28 16:19:33.008399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44bc1a7c4eec'
down_revision = '088c2546008e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
