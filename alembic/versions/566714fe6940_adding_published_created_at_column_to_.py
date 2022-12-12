"""adding published, created_at column to posts table

Revision ID: 566714fe6940
Revises: 7282eb424a90
Create Date: 2022-12-08 20:28:12.287766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566714fe6940'
down_revision = '7282eb424a90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column( "posts", sa.Column("published", sa.Boolean, nullable = False, server_default='TRUE') )
    op.add_column( "posts", sa.Column( "created_at",sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')) )


def downgrade() -> None:
    op.drop_column( "posts", "published" )
    op.drop_column( "posts", "created_at" )
