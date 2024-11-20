"""initial migration

Revision ID: 6d6206370545
Revises: 
Create Date: 2024-11-19 13:26:49.226749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d6206370545'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac_address', sa.String(length=17), nullable=False),
    sa.Column('ip_address', sa.String(length=15), nullable=False),
    sa.Column('access_granted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mac_address')
    )
    op.create_table('otp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('otp_code', sa.String(length=6), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('otp')
    op.drop_table('device')
    # ### end Alembic commands ###
