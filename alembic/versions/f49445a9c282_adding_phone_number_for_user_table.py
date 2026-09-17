"""Adding phone number for user table

Revision ID: f49445a9c282
Revises: 0797321af7a0
Create Date: 2026-07-25 16:19:15.730230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f49445a9c282'
down_revision: Union[str, Sequence[str], None] = '0797321af7a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
