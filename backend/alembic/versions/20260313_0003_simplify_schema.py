"""simplify schema for storage-only platform

Revision ID: 20260313_0003
Revises: 20260308_0002
Create Date: 2026-03-13 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260313_0003"
down_revision: Union[str, Sequence[str], None] = "20260308_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop ingestion_logs table
    op.execute("DROP TABLE IF EXISTS ingestion_logs CASCADE")

    # Drop columns that are no longer needed
    op.execute("ALTER TABLE knowledge_items DROP COLUMN IF EXISTS captured_at")
    op.execute("ALTER TABLE knowledge_items DROP COLUMN IF EXISTS thumbnail_url")
    op.execute("ALTER TABLE knowledge_items DROP COLUMN IF EXISTS description")
    op.execute("ALTER TABLE knowledge_items DROP COLUMN IF EXISTS cleaned_content")
    op.execute("ALTER TABLE knowledge_items DROP COLUMN IF EXISTS error_message")

    # Set all existing items to 'ready' status
    op.execute("UPDATE knowledge_items SET processing_status = 'ready' WHERE processing_status != 'ready'")

    # Add index on category if not exists
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'ix_knowledge_items_category') THEN
                CREATE INDEX ix_knowledge_items_category ON knowledge_items (category);
            END IF;
        END $$;
    """)


def downgrade() -> None:
    # Re-add dropped columns
    op.add_column("knowledge_items", sa.Column("captured_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("knowledge_items", sa.Column("thumbnail_url", sa.Text(), nullable=True))
    op.add_column("knowledge_items", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("knowledge_items", sa.Column("cleaned_content", sa.Text(), nullable=True))
    op.add_column("knowledge_items", sa.Column("error_message", sa.Text(), nullable=True))

    # Re-create ingestion_logs table
    op.create_table(
        "ingestion_logs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("knowledge_item_id", sa.Uuid(), sa.ForeignKey("knowledge_items.id", ondelete="CASCADE")),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
