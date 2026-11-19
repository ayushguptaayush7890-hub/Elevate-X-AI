"""initial baseline

Revision ID: 0001_baseline
Revises: 
Create Date: 2026-11-14 12:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_baseline"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Phase 1 baseline migration setup
    pass


def downgrade() -> None:
    pass

