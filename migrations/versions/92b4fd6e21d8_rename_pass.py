"""rename pass

Revision ID: 92b4fd6e21d8
Revises: 88d3480ab329
Create Date: 2023-12-30 12:46:14.868332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92b4fd6e21d8'
down_revision: Union[str, None] = '88d3480ab329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.String(), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###
