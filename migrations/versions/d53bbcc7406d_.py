"""empty message

Revision ID: d53bbcc7406d
Revises: f58e37c51d11
Create Date: 2024-12-10 15:59:24.141093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd53bbcc7406d'
down_revision: Union[str, None] = 'f58e37c51d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
