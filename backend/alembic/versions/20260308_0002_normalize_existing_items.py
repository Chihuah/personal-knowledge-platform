"""normalize existing item data

Revision ID: 20260308_0002
Revises: 20260308_0001
Create Date: 2026-03-08 05:20:00
"""

from typing import Sequence, Union

from alembic import op


revision: str = "20260308_0002"
down_revision: Union[str, Sequence[str], None] = "20260308_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE knowledge_items
        SET source_platform = CASE
            WHEN lower(source_url) LIKE '%threads.com/%' OR lower(source_url) LIKE '%threads.net/%' THEN 'threads'
            WHEN lower(source_url) LIKE '%facebook.com/%' OR lower(source_url) LIKE '%fb.watch/%' THEN 'facebook'
            WHEN lower(source_url) LIKE '%youtube.com/%' OR lower(source_url) LIKE '%youtu.be/%' THEN 'youtube'
            ELSE source_platform
        END
        """
    )

    op.execute(
        """
        UPDATE knowledge_items
        SET content_type = CASE
            WHEN content_type IS NULL OR trim(content_type) = '' THEN 'unknown'
            WHEN lower(trim(content_type)) = 'article' OR trim(content_type) = '文章' THEN 'article'
            WHEN lower(trim(content_type)) = 'post' OR trim(content_type) = '貼文' THEN 'post'
            WHEN lower(trim(content_type)) IN ('video', 'video clip') OR trim(content_type) = '影片' THEN 'video'
            WHEN lower(trim(content_type)) = 'tool' OR trim(content_type) = '工具' THEN 'tool'
            WHEN lower(trim(content_type)) = 'tutorial' OR trim(content_type) = '教學' THEN 'tutorial'
            WHEN lower(trim(content_type)) = 'resource' OR trim(content_type) = '資源' THEN 'resource'
            WHEN lower(trim(content_type)) = 'unknown' OR trim(content_type) = '未知' THEN 'unknown'
            ELSE 'unknown'
        END
        """
    )

    op.execute(
        """
        UPDATE knowledge_items
        SET content_type = 'video'
        WHERE source_platform = 'youtube'
        """
    )

    op.execute(
        """
        UPDATE knowledge_items
        SET content_type = 'post'
        WHERE source_platform IN ('threads', 'facebook')
          AND content_type IN ('article', 'unknown')
        """
    )


def downgrade() -> None:
    pass
