"""Initial schema with query_logs table

Revision ID: 001
Revises:
Create Date: 2025-01-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create query_logs table for storing query metadata and analytics.
    """
    op.create_table(
        'query_logs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('query_id', sa.String(length=36), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('mode', sa.String(length=20), nullable=False),
        sa.Column('session_id_hash', sa.String(length=64), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=False),
        sa.Column('chunk_count', sa.Integer(), nullable=False),
        sa.Column('error', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('query_id')
    )

    # Create indexes for common query patterns
    op.create_index('ix_query_logs_query_id', 'query_logs', ['query_id'])
    op.create_index('ix_query_logs_timestamp', 'query_logs', ['timestamp'])
    op.create_index('ix_query_logs_session_id_hash', 'query_logs', ['session_id_hash'])


def downgrade() -> None:
    """
    Drop query_logs table and indexes.
    """
    op.drop_index('ix_query_logs_session_id_hash', table_name='query_logs')
    op.drop_index('ix_query_logs_timestamp', table_name='query_logs')
    op.drop_index('ix_query_logs_query_id', table_name='query_logs')
    op.drop_table('query_logs')
