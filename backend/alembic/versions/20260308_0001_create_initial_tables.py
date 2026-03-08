"""create initial tables

Revision ID: 20260308_0001
Revises:
Create Date: 2026-03-08 05:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260308_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "knowledge_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("source_platform", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("author", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("raw_content", sa.Text(), nullable=True),
        sa.Column("cleaned_content", sa.Text(), nullable=True),
        sa.Column("short_summary", sa.Text(), nullable=True),
        sa.Column("full_summary", sa.Text(), nullable=True),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("category", sa.Text(), nullable=True),
        sa.Column("content_type", sa.Text(), nullable=True),
        sa.Column("processing_status", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("search_document", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_url"),
    )
    op.create_index(
        "ix_knowledge_items_source_url",
        "knowledge_items",
        ["source_url"],
        unique=True,
    )
    op.create_index(
        "ix_knowledge_items_captured_at",
        "knowledge_items",
        ["captured_at"],
        unique=False,
    )
    op.create_index(
        "ix_knowledge_items_processing_status",
        "knowledge_items",
        ["processing_status"],
        unique=False,
    )
    op.create_index(
        "ix_knowledge_items_category",
        "knowledge_items",
        ["category"],
        unique=False,
    )

    op.create_table(
        "ingestion_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("knowledge_item_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["knowledge_item_id"],
            ["knowledge_items.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ingestion_logs_knowledge_item_id",
        "ingestion_logs",
        ["knowledge_item_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ingestion_logs_knowledge_item_id", table_name="ingestion_logs")
    op.drop_table("ingestion_logs")
    op.drop_index("ix_knowledge_items_category", table_name="knowledge_items")
    op.drop_index("ix_knowledge_items_processing_status", table_name="knowledge_items")
    op.drop_index("ix_knowledge_items_captured_at", table_name="knowledge_items")
    op.drop_index("ix_knowledge_items_source_url", table_name="knowledge_items")
    op.drop_table("knowledge_items")
