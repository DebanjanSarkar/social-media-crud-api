"""create users table

Revision ID: 25e0f6cac48d
Revises: 566714fe6940
Create Date: 2022-12-09 00:04:35.921193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25e0f6cac48d'
down_revision = '566714fe6940'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", 
        sa.Column("id", sa.Integer(), primary_key = True, nullable = False),
        sa.Column("email", sa.String(), unique = True, nullable = False),
        sa.Column("password", sa.String(), nullable = False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')),
        )


def downgrade() -> None:
    op.drop_table("users")
