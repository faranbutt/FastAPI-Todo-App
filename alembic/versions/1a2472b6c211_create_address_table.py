"""Create Address table

Revision ID: 1a2472b6c211
Revises: 3363a47bbd31
Create Date: 2023-08-29 18:30:48.562976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2472b6c211'
down_revision: Union[str, None] = '3363a47bbd31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('address1',sa.String(),nullable=False),
                    sa.Column('address2',sa.String(),nullable=False),
                    sa.Column('city',sa.String(),nullable=False),
                    sa.Column('state',sa.String(),nullable=False),
                    sa.Column('country',sa.String(),nullable=False),
                    sa.Column('postalcode',sa.String(),nullable=False),
                    )

def downgrade() -> None:
    op.drop_table('address')
