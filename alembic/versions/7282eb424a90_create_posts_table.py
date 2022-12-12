"""create posts table

Revision ID: 7282eb424a90
Revises: 
Create Date: 2022-12-08 19:59:14.262891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7282eb424a90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
        sa.Column("id", sa.Integer(), primary_key = True, nullable = False),
        sa.Column("title", sa.String(), nullable = False),
        sa.Column("content", sa.String(), nullable = False)
        )


def downgrade() -> None:
    op.drop_table("posts")
