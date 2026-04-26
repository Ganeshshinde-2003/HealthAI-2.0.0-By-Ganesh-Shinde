# Database Setup Guide

## Overview
Your HealthAI backend now has PostgreSQL database integration using:
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Neon PostgreSQL** - Cloud database (free tier)

## Database Schema

### Tables Created:
1. **users** - User accounts and profiles
2. **analyses** - Lab analysis results (biomarkers, four pillars, supplements)
3. **monthly_reports** - Monthly health reports
4. **chat_messages** - Chat conversation history
5. **daily_logs** - Daily health tracking logs

## Running the Migration

Once your DATABASE_URL is properly set in `.env`, run:

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

This will create all the database tables.

## Verify Tables Were Created

Run the verification script:

```bash
python verify_tables.py
```

Expected output:
```
Found 6 tables in database:
  - alembic_version
  - analyses
  - chat_messages
  - daily_logs
  - monthly_reports
  - users

✓ All expected tables exist!
```

## Database Models

### User Model
```python
from app.models import User

# Create a new user
user = User(
    email="user@example.com",
    name="Jane Doe",
    age=30,
    gender="female"
)
db.session.add(user)
db.session.commit()
```

### Analysis Model
```python
from app.models import Analysis

# Save analysis results
analysis = Analysis(
    user_id=user.id,
    analysis_type="lab_report",
    lab_analysis=lab_data,  # JSON data
    four_pillars=pillars_data,  # JSON data
    supplements=supplements_data,  # JSON data
    biomarkers_count=15,
    overall_summary="Health status summary"
)
db.session.add(analysis)
db.session.commit()
```

### Monthly Report Model
```python
from app.models import MonthlyReport

# Save monthly report
report = MonthlyReport(
    user_id=user.id,
    report_month="2026-04",
    monthly_overview_summary=overview_data,  # JSON
    radar_chart_data=chart_data  # JSON
)
db.session.add(report)
db.session.commit()
```

### Chat Message Model
```python
from app.models import ChatMessage

# Save chat message
message = ChatMessage(
    user_id=user.id,
    role="user",
    message="How can I improve my sleep?",
    session_id="session-123"
)
db.session.add(message)
db.session.commit()
```

### Daily Log Model
```python
from app.models import DailyLog
from datetime import datetime

# Save daily log
log = DailyLog(
    user_id=user.id,
    log_date=datetime.now(),
    sleep_hours=7.5,
    sleep_quality=8.0,
    exercise_type="Running",
    exercise_duration_minutes=30,
    stress_level=4.0
)
db.session.add(log)
db.session.commit()
```

## Using in API Endpoints

### Example: Save Analysis in /analyze Endpoint

```python
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, Analysis

@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    # ... existing analysis logic ...

    # Get or create user
    user_email = request.form.get('email', 'anonymous@healthai.com')
    user = User.query.filter_by(email=user_email).first()
    if not user:
        user = User(email=user_email, is_active=True)
        db.session.add(user)
        db.session.flush()  # Get user.id

    # Save analysis to database
    analysis = Analysis(
        user_id=user.id,
        analysis_type='lab_report',
        status='completed',
        lab_report_filename=lab_report_file.filename if lab_report_file else None,
        lab_analysis=response_data.get('lab_analysis'),
        four_pillars=response_data.get('four_pillars'),
        supplements=response_data.get('supplements'),
        biomarkers_count=len(response_data.get('lab_analysis', {}).get('detailed_biomarkers', [])),
        overall_summary=response_data.get('lab_analysis', {}).get('overall_summary')
    )
    db.session.add(analysis)
    db.session.commit()

    # Return analysis with database ID
    return jsonify({
        'id': analysis.id,
        'data': response_data
    })
```

### Example: Get User's Analysis History

```python
@analysis_bp.route('/analyses/<int:user_id>', methods=['GET'])
def get_user_analyses(user_id):
    # Query user's analyses, ordered by most recent
    analyses = Analysis.query.filter_by(user_id=user_id)\
        .order_by(Analysis.created_at.desc())\
        .limit(10)\
        .all()

    return jsonify({
        'analyses': [a.to_dict() for a in analyses]
    })
```

## Migration Commands

### Create a new migration (after model changes)
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback last migration
```bash
alembic downgrade -1
```

### Check current migration version
```bash
alembic current
```

## Troubleshooting

### "relation does not exist" error
Run the migration:
```bash
alembic upgrade head
```

### Connection errors
1. Verify DATABASE_URL is correct in `.env`
2. Check Neon dashboard - database might be sleeping (free tier)
3. Ensure `?sslmode=require` is in the connection string

### Reset database (development only)
```bash
# Downgrade all migrations
alembic downgrade base

# Re-apply all migrations
alembic upgrade head
```

## Next Steps

1. ✅ Database setup complete
2. ⏳ Update API endpoints to save/retrieve data
3. ⏳ Add user authentication
4. ⏳ Create database queries for frontend
5. ⏳ Add data validation and error handling
