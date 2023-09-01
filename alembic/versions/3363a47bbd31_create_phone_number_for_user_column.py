"""Create phone number for user column

Revision ID: 3363a47bbd31
Revises: 
Create Date: 2023-08-28 17:46:34.413558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3363a47bbd31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
