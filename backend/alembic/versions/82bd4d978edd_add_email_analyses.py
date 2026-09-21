"""add email analyses

Revision ID: 82bd4d978edd
Revises: 75308209d998
Create Date: 2026-09-18 11:31:39.367132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82bd4d978edd'
down_revision: Union[str, Sequence[str], None] = '75308209d998'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'email_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_id', sa.Integer(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False),
        sa.Column('importance', sa.String(length=20), nullable=False),
        sa.Column('actions', sa.Text(), nullable=True),
        sa.Column('deadlines', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['email_id'], ['emails.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_id')
    )


def downgrade() -> None:
    op.drop_table('email_analyses')
