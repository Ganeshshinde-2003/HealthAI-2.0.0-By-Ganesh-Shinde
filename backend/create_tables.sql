-- HealthAI Database Schema
-- Run this SQL in Neon SQL Editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    age INTEGER,
    gender VARCHAR(50),
    health_goals VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Create analyses table
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'completed',
    lab_report_filename VARCHAR(255),
    health_assessment_filename VARCHAR(255),
    lab_analysis JSONB,
    four_pillars JSONB,
    supplements JSONB,
    biomarkers_count INTEGER,
    overall_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS ix_analyses_created_at ON analyses(created_at);

-- Create monthly_reports table
CREATE TABLE IF NOT EXISTS monthly_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_month VARCHAR(7) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'completed',
    monthly_overview_summary JSONB,
    hormonal_balance_insight JSONB,
    logged_patterns JSONB,
    root_cause_tags JSONB,
    actionable_next_steps JSONB,
    radar_chart_data JSONB,
    top_symptoms TEXT,
    health_reflection TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_monthly_reports_user_id ON monthly_reports(user_id);
CREATE INDEX IF NOT EXISTS ix_monthly_reports_report_month ON monthly_reports(report_month);
CREATE INDEX IF NOT EXISTS ix_monthly_reports_created_at ON monthly_reports(created_at);

-- Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    session_id VARCHAR(255),
    context_type VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS ix_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS ix_chat_messages_created_at ON chat_messages(created_at);

-- Create daily_logs table
CREATE TABLE IF NOT EXISTS daily_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    log_date TIMESTAMP NOT NULL,
    meals JSONB,
    meal_satisfaction_score REAL,
    processed_food VARCHAR(50),
    sleep_hours REAL,
    sleep_quality REAL,
    sleep_notes TEXT,
    exercise_type VARCHAR(255),
    exercise_duration_minutes INTEGER,
    exercise_intensity VARCHAR(50),
    steps INTEGER,
    stress_level REAL,
    mood VARCHAR(100),
    recovery_activities JSONB,
    menstrual_cycle_day INTEGER,
    symptoms JSONB,
    notes TEXT,
    energy_level REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_daily_logs_user_id ON daily_logs(user_id);
CREATE INDEX IF NOT EXISTS ix_daily_logs_log_date ON daily_logs(log_date);

-- Create alembic_version table for migration tracking
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- Insert initial migration version
INSERT INTO alembic_version (version_num) VALUES ('a8943dee2b30')
ON CONFLICT (version_num) DO NOTHING;

-- Verify tables were created
SELECT
    tablename,
    schemaname
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
