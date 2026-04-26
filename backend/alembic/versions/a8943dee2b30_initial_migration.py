"""Initial migration

Revision ID: a8943dee2b30
Revises: 
Create Date: 2026-04-26 13:57:33.177970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a8943dee2b30'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=50), nullable=True),
        sa.Column('health_goals', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create analyses table
    op.create_table('analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('analysis_type', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('lab_report_filename', sa.String(length=255), nullable=True),
        sa.Column('health_assessment_filename', sa.String(length=255), nullable=True),
        sa.Column('lab_analysis', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('four_pillars', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('supplements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('biomarkers_count', sa.Integer(), nullable=True),
        sa.Column('overall_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_user_id'), 'analyses', ['user_id'], unique=False)
    op.create_index(op.f('ix_analyses_created_at'), 'analyses', ['created_at'], unique=False)

    # Create monthly_reports table
    op.create_table('monthly_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('report_month', sa.String(length=7), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('monthly_overview_summary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('hormonal_balance_insight', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('logged_patterns', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('root_cause_tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('actionable_next_steps', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('radar_chart_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('top_symptoms', sa.Text(), nullable=True),
        sa.Column('health_reflection', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monthly_reports_user_id'), 'monthly_reports', ['user_id'], unique=False)
    op.create_index(op.f('ix_monthly_reports_report_month'), 'monthly_reports', ['report_month'], unique=False)
    op.create_index(op.f('ix_monthly_reports_created_at'), 'monthly_reports', ['created_at'], unique=False)

    # Create chat_messages table
    op.create_table('chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('context_type', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_user_id'), 'chat_messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_chat_messages_session_id'), 'chat_messages', ['session_id'], unique=False)
    op.create_index(op.f('ix_chat_messages_created_at'), 'chat_messages', ['created_at'], unique=False)

    # Create daily_logs table
    op.create_table('daily_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('log_date', sa.DateTime(), nullable=False),
        sa.Column('meals', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meal_satisfaction_score', sa.Float(), nullable=True),
        sa.Column('processed_food', sa.String(length=50), nullable=True),
        sa.Column('sleep_hours', sa.Float(), nullable=True),
        sa.Column('sleep_quality', sa.Float(), nullable=True),
        sa.Column('sleep_notes', sa.Text(), nullable=True),
        sa.Column('exercise_type', sa.String(length=255), nullable=True),
        sa.Column('exercise_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('exercise_intensity', sa.String(length=50), nullable=True),
        sa.Column('steps', sa.Integer(), nullable=True),
        sa.Column('stress_level', sa.Float(), nullable=True),
        sa.Column('mood', sa.String(length=100), nullable=True),
        sa.Column('recovery_activities', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('menstrual_cycle_day', sa.Integer(), nullable=True),
        sa.Column('symptoms', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('energy_level', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_logs_user_id'), 'daily_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_daily_logs_log_date'), 'daily_logs', ['log_date'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_daily_logs_log_date'), table_name='daily_logs')
    op.drop_index(op.f('ix_daily_logs_user_id'), table_name='daily_logs')
    op.drop_table('daily_logs')

    op.drop_index(op.f('ix_chat_messages_created_at'), table_name='chat_messages')
    op.drop_index(op.f('ix_chat_messages_session_id'), table_name='chat_messages')
    op.drop_index(op.f('ix_chat_messages_user_id'), table_name='chat_messages')
    op.drop_table('chat_messages')

    op.drop_index(op.f('ix_monthly_reports_created_at'), table_name='monthly_reports')
    op.drop_index(op.f('ix_monthly_reports_report_month'), table_name='monthly_reports')
    op.drop_index(op.f('ix_monthly_reports_user_id'), table_name='monthly_reports')
    op.drop_table('monthly_reports')

    op.drop_index(op.f('ix_analyses_created_at'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_user_id'), table_name='analyses')
    op.drop_table('analyses')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
