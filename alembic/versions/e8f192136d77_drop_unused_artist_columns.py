"""drop unused artist columns

Revision ID: e8f192136d77
Revises: 
Create Date: 2025-04-10 12:09:04.975393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f192136d77'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('artist', 'found_year', schema='staging')
    op.drop_column('artist', 'wealth_index', schema='staging')
    op.drop_column('artist', 'crime_index', schema='staging')
    op.drop_column('artist', 'popularity_index', schema='staging')
    op.drop_column('artist', 'sex_index', schema='staging')
    op.drop_column('artist', 'scandal_index', schema='staging')
    op.drop_column('artist', 'performance_count', schema='staging')
    op.drop_column('artist', 'fan_subculture', schema='staging')

# def downgrade():
#     op.add_column('artist', sa.Column('found_year', sa.Integer), schema='staging')
#     op.add_column('artist', sa.Column('scandal_index', sa.Float), schema='staging')
#     op.add_column('artist', sa.Column('fan_subculture', sa.Text), schema='staging')
