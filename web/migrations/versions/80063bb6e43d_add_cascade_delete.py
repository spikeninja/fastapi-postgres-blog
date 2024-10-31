"""STRUCTURE MIGRATION: add cascade delete

Revision ID: 80063bb6e43d
Revises: 237c153f1533
Create Date: 2024-10-31 20:05:36.402592

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '80063bb6e43d'
down_revision: Union[str, None] = '237c153f1533'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FKEY_NAME = "comments_post_id_fkey"


def upgrade() -> None:
    """"""

    op.drop_constraint(FKEY_NAME, 'comments', type_='foreignkey')
    op.create_foreign_key(
        FKEY_NAME,
        'comments',
        'posts',
        ['post_id'],
        ['id'],
        ondelete='cascade'
    )


def downgrade() -> None:
    """"""

    op.drop_constraint(FKEY_NAME, 'comments', type_='foreignkey')
    op.create_foreign_key(FKEY_NAME, 'comments', 'posts', ['post_id'], ['id'])
