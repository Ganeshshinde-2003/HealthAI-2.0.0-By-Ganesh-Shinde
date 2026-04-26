# HealthAI Backend - Complete Guide

**Version:** 2.0.0
**Author:** Ganesh Shinde
**Stack:** Flask + PostgreSQL + Google Vertex AI

---

## 📚 Table of Contents

1. [Tech Stack & Why We Chose It](#tech-stack--why-we-chose-it)
2. [Project Structure](#project-structure)
3. [Setup Guide](#setup-guide)
4. [Database Architecture](#database-architecture)
5. [API Documentation](#api-documentation)
6. [Development Workflow](#development-workflow)
7. [Troubleshooting](#troubleshooting)
8. [Deployment](#deployment)

---

## 🔧 Tech Stack & Why We Chose It

### Backend Framework: **Flask 3.1.0**
**Why Flask?**
- ✅ **Lightweight & Fast** - Perfect for REST APIs
- ✅ **Easy to Learn** - Simple, Pythonic syntax
- ✅ **Flexible** - No forced structure, build what you need
- ✅ **Great for AI/ML** - Seamless integration with Python AI libraries
- ✅ **Production Ready** - Used by Netflix, Reddit, Airbnb

**Alternatives Considered:**
- FastAPI - Too complex for current needs, async not required
- Django - Too heavy, includes unnecessary features (admin panel, ORM overhead)
- Express.js - Would require Node.js, team is Python-focused

---

### Database: **PostgreSQL (via Neon)**
**Why PostgreSQL?**
- ✅ **Structured Health Data** - User profiles, lab results need consistent schema
- ✅ **Relationships** - Users → Analyses → Reports (relational data)
- ✅ **ACID Compliance** - Critical for health data integrity
- ✅ **JSON Support** - Store flexible biomarker data as JSONB
- ✅ **Complex Queries** - Generate monthly reports, filter by date ranges
- ✅ **Industry Standard** - Most companies use PostgreSQL for production

**Why Neon?**
- ✅ **Free Tier** - 0.5GB storage, perfect for development
- ✅ **Serverless** - Auto-scales, sleeps when inactive (saves costs)
- ✅ **Fast Setup** - No infrastructure management
- ✅ **Modern** - Built for cloud-native apps
- ✅ **Branching** - Create database branches like Git (great for testing)

**Alternatives Considered:**
- MongoDB - NoSQL doesn't fit relational health data, harder to query trends
- MySQL - Less modern features, weaker JSON support than PostgreSQL
- SQLite - File-based, not suitable for production with multiple users

---

### ORM: **SQLAlchemy 2.0.36**
**Why SQLAlchemy?**
- ✅ **Pythonic** - Write database queries in Python, not raw SQL
- ✅ **Safe** - Prevents SQL injection automatically
- ✅ **Flexible** - Can use ORM or raw SQL when needed
- ✅ **Migrations** - Works seamlessly with Alembic
- ✅ **Type Safety** - Models are Python classes with type hints

**Example:**
```python
# Instead of raw SQL:
# "SELECT * FROM users WHERE email = ?"
# Use SQLAlchemy:
user = User.query.filter_by(email="user@example.com").first()
```

---

### Database Migrations: **Alembic 1.14.0**
**Why Alembic?**
- ✅ **Version Control for Database** - Track schema changes like Git
- ✅ **Safe Updates** - Modify tables without losing data
- ✅ **Team Collaboration** - Everyone stays in sync
- ✅ **Rollback Support** - Undo changes if something breaks
- ✅ **Auto-generate** - Creates migration scripts from model changes

**How It Works:**
1. Change your models (add a field, create a table)
2. Run: `alembic revision --autogenerate -m "Add new field"`
3. Review the generated migration
4. Run: `alembic upgrade head` to apply changes
5. Database is updated without data loss!

---

### AI Engine: **Google Vertex AI (Gemini 2.5 Flash Lite)**
**Why Gemini?**
- ✅ **Best for Structured Output** - JSON responses with schema validation
- ✅ **Large Context Window** - Can process entire lab reports
- ✅ **Fast** - Flash Lite is optimized for speed
- ✅ **Affordable** - Cost-effective for health analysis
- ✅ **Safety Features** - Built-in content filtering for medical data
- ✅ **Multimodal** - Can process text, images, PDFs

**Alternatives Considered:**
- OpenAI GPT-4 - More expensive, slower JSON mode
- Anthropic Claude - Great but more expensive for this use case
- Open-source LLMs - Need hosting infrastructure, less reliable

---

### File Processing Libraries

**PyMuPDF (PDF)** - Fast, accurate PDF text extraction
**python-docx (Word)** - Parse .docx files
**openpyxl (Excel)** - Read Excel spreadsheets with lab results
**pandas** - Data manipulation and analysis

**Why These?**
- Users upload lab reports in various formats
- Need reliable text extraction to feed AI
- Industry-standard libraries with good documentation

---

### Other Key Dependencies

**Flask-CORS** - Allow frontend (Next.js) to call API
**python-dotenv** - Manage environment variables securely
**gunicorn** - Production-grade WSGI server
**psycopg2-binary** - PostgreSQL driver for Python
**jsonschema** - Validate AI responses match expected format

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── extensions.py            # SQLAlchemy db instance
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User accounts
│   │   ├── analysis.py          # Lab analysis results
│   │   ├── monthly_report.py    # Monthly health reports
│   │   ├── chat_message.py      # Chat history
│   │   └── daily_log.py         # Daily health tracking
│   ├── routes/                  # API endpoints
│   │   ├── health.py            # Health check endpoints
│   │   ├── analysis.py          # /analyze endpoint
│   │   ├── monthly.py           # /monthly-report endpoint
│   │   └── chat.py              # /chat endpoint
│   ├── services/                # Business logic
│   │   ├── analysis_service.py  # Health analysis processing
│   │   └── monthly_service.py   # Monthly report generation
│   └── utils/                   # Helper functions
│       ├── ai_client.py         # Gemini API wrapper
│       ├── file_processor.py    # Extract text from files
│       ├── prompt_loader.py     # Load prompts & schemas
│       ├── validators.py        # JSON validation
│       └── response_transformer.py  # Format AI output
├── config/
│   └── config.py                # Configuration classes
├── prompts/
│   ├── analysis.txt             # AI prompts for analysis
│   ├── monthly.txt              # AI prompts for reports
│   └── schemas/                 # JSON schemas
│       ├── analysis_schema.json
│       └── monthly_schema.json
├── alembic/                     # Database migrations
│   ├── versions/                # Migration files
│   └── env.py                   # Migration environment
├── uploads/                     # Temporary file storage
├── .env                         # Environment variables (NOT in Git)
├── .env.example                 # Template for .env
├── .gitignore                   # Ignore sensitive files
├── requirements.txt             # Python dependencies
├── run.py                       # App entry point
└── BACKEND_GUIDE.md            # This file
```

---

## 🚀 Setup Guide

### Prerequisites

- Python 3.9+ (3.10+ recommended)
- pip (Python package manager)
- Git
- Neon PostgreSQL account (free at https://neon.tech)
- Google Cloud account with Vertex AI enabled

---

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd ai-health-analyser/backend
```

---

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal.

---

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Alembic (migrations)
- Google Cloud AI libraries
- File processing libraries
- All other dependencies

---

### Step 4: Set Up Environment Variables

#### Create `.env` file:
```bash
cp .env.example .env
```

#### Edit `.env` with your credentials:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-random-secret-key-here

# Google Cloud Platform
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}

# Database (from Neon dashboard)
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# CORS (your frontend URL)
CORS_ORIGINS=http://localhost:3000

# File Upload
MAX_UPLOAD_SIZE_MB=10

# Logging
LOG_LEVEL=INFO
```

**How to get credentials:**
- **Google Cloud:** https://console.cloud.google.com
- **Neon Database:** https://console.neon.tech

**Important:** Never commit `.env` to Git! (It's already in `.gitignore`)

---

### Step 5: Create Upload Directory

```bash
mkdir -p uploads
```

---

### Step 6: Set Up Database

#### Option A: Using Neon SQL Editor (Recommended for first time)

1. Go to https://console.neon.tech
2. Open your project
3. Click "SQL Editor"
4. Run this SQL:

```sql
-- Create users table
CREATE TABLE users (
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

-- Create analyses table
CREATE TABLE analyses (
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

-- Create indexes
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);

-- (Continue with other tables...)
```

#### Option B: Using Alembic (If your connection is stable)

```bash
alembic upgrade head
```

---

### Step 7: Run the Backend

```bash
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

---

### Step 8: Test the API

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "HealthAI Backend",
  "version": "2.0.0"
}
```

---

## 🗄️ Database Architecture

### Why PostgreSQL for HealthAI?

**HealthAI stores complex, relational health data:**

1. **Users** have multiple **Analyses**
2. **Analyses** contain **Biomarkers** (as JSON)
3. **Users** create **Daily Logs**
4. **Users** generate **Monthly Reports**
5. **Users** have **Chat History**

This is **relational data** → Perfect for PostgreSQL!

---

### Database Schema

#### **1. Users Table**
Stores user accounts and profiles.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    age INTEGER,
    gender VARCHAR(50),
    health_goals VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

**Why these fields?**
- `email` - User identification (unique)
- `age`, `gender` - Personalized health recommendations
- `health_goals` - Context for AI analysis
- `is_active` - Soft delete (don't actually delete user data)

---

#### **2. Analyses Table**
Stores lab analysis results (biomarkers, four pillars, supplements).

```sql
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    analysis_type VARCHAR(100),      -- 'lab_report', 'health_assessment'
    status VARCHAR(50),               -- 'completed', 'pending', 'failed'
    lab_report_filename VARCHAR(255),
    health_assessment_filename VARCHAR(255),
    lab_analysis JSONB,               -- Biomarkers data (flexible structure)
    four_pillars JSONB,               -- Four pillars analysis
    supplements JSONB,                -- Supplement recommendations
    biomarkers_count INTEGER,
    overall_summary TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Why JSONB for analysis data?**
- Biomarkers vary per lab report (different tests, different formats)
- JSONB allows flexible structure while still being queryable
- Can still search within JSON: `WHERE lab_analysis->>'status' = 'optimal'`

---

#### **3. Monthly Reports Table**
Stores monthly health trend reports.

```sql
CREATE TABLE monthly_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    report_month VARCHAR(7),          -- 'YYYY-MM' format
    status VARCHAR(50),
    monthly_overview_summary JSONB,
    hormonal_balance_insight JSONB,
    logged_patterns JSONB,
    root_cause_tags JSONB,
    actionable_next_steps JSONB,
    radar_chart_data JSONB,
    top_symptoms TEXT,
    health_reflection TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

#### **4. Chat Messages Table**
Stores conversation history for context-aware responses.

```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(50),                 -- 'user' or 'assistant'
    message TEXT,
    session_id VARCHAR(255),          -- Group messages by conversation
    context_type VARCHAR(100),        -- 'lab_analysis', 'general', etc.
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

#### **5. Daily Logs Table**
Stores daily health tracking (sleep, meals, exercise, mood).

```sql
CREATE TABLE daily_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    log_date TIMESTAMP,
    -- Eat Well
    meals JSONB,
    meal_satisfaction_score FLOAT,
    processed_food VARCHAR(50),
    -- Sleep Well
    sleep_hours FLOAT,
    sleep_quality FLOAT,
    sleep_notes TEXT,
    -- Move Well
    exercise_type VARCHAR(255),
    exercise_duration_minutes INTEGER,
    exercise_intensity VARCHAR(50),
    steps INTEGER,
    -- Recover Well
    stress_level FLOAT,
    mood VARCHAR(100),
    recovery_activities JSONB,
    menstrual_cycle_day INTEGER,
    symptoms JSONB,
    -- General
    notes TEXT,
    energy_level FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Why so many columns?**
- Tracks "Four Pillars" - Eat, Sleep, Move, Recover
- Each pillar has specific metrics
- Used to generate monthly trend reports
- Women's health focus - menstrual cycle tracking

---

### Database Relationships

```
users (1) ─── (many) analyses
  │
  ├── (many) monthly_reports
  │
  ├── (many) chat_messages
  │
  └── (many) daily_logs
```

**CASCADE DELETE:** If user is deleted, all their data is deleted too.

---

### Using the Database in Code

#### **Create a User:**
```python
from app.extensions import db
from app.models import User

user = User(
    email="jane@example.com",
    name="Jane Doe",
    age=30,
    gender="female",
    is_active=True
)
db.session.add(user)
db.session.commit()
```

#### **Save Analysis Results:**
```python
from app.models import Analysis

analysis = Analysis(
    user_id=user.id,
    analysis_type='lab_report',
    lab_analysis={
        "overall_summary": "Good health",
        "detailed_biomarkers": [...]
    },
    four_pillars={...},
    supplements={...},
    biomarkers_count=15
)
db.session.add(analysis)
db.session.commit()
```

#### **Query User's Analysis History:**
```python
# Get last 10 analyses for a user
analyses = Analysis.query\
    .filter_by(user_id=user.id)\
    .order_by(Analysis.created_at.desc())\
    .limit(10)\
    .all()

# Convert to JSON
results = [a.to_dict() for a in analyses]
```

---

## 🌐 API Documentation

### Base URL
```
http://localhost:5000/api
```

---

### **Health Check Endpoints**

#### `GET /health`
Check if backend is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "HealthAI Backend",
  "version": "2.0.0",
  "timestamp": "2026-04-26T10:30:00"
}
```

#### `GET /ping`
Simple ping endpoint.

**Response:**
```json
{
  "message": "pong"
}
```

---

### **Analysis Endpoint**

#### `POST /analyze`
Upload lab reports and health assessment for AI analysis.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lab_reports` | File[] | Yes | PDF/DOCX/XLSX lab reports |
| `health_assessment` | File | No | Health assessment document |
| `email` | String | No | User email (for saving to DB) |

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "lab_reports=@lab_report.pdf" \
  -F "health_assessment=@assessment.docx" \
  -F "email=user@example.com"
```

**Response:**
```json
{
  "lab_analysis": {
    "overall_summary": "Your health markers are generally good...",
    "biomarkers_tested_count": 15,
    "biomarker_categories_summary": {...},
    "detailed_biomarkers": [...]
  },
  "four_pillars": {
    "introduction": "...",
    "pillars": [...]
  },
  "supplements": {
    "description": "...",
    "structure": {
      "recommendations": [...]
    }
  }
}
```

---

### **Monthly Report Endpoint**

#### `POST /monthly-report`
Generate monthly health report from daily logs.

**Request:**
```bash
curl -X POST http://localhost:5000/api/monthly-report \
  -F "previous_lab_report=@lab.pdf" \
  -F "daily_logs=@logs.xlsx" \
  -F "weekly_assessments=@assessments.csv"
```

**Response:**
```json
{
  "monthly_overview_summary": {...},
  "hormonal_balance_insight": {...},
  "logged_patterns": {...},
  "root_cause_tags": [...],
  "actionable_next_steps": {...},
  "radar_chart_data": {...}
}
```

---

### **Chat Endpoint**

#### `POST /chat`
Chat with health AI assistant.

**Request:**
```json
{
  "message": "How can I improve my sleep?",
  "context": "lab_analysis",  // optional
  "session_id": "abc123"      // optional
}
```

**Response:**
```json
{
  "response": "Based on your recent analysis...",
  "session_id": "abc123"
}
```

---

## 🔄 Development Workflow

### Making Model Changes

1. **Edit the model:**
```python
# app/models/user.py
class User(db.Model):
    # Add new field
    phone_number = Column(String(20), nullable=True)
```

2. **Create migration:**
```bash
alembic revision --autogenerate -m "Add phone number to users"
```

3. **Review migration file:**
```bash
# Check alembic/versions/xxx_add_phone_number.py
```

4. **Apply migration:**
```bash
alembic upgrade head
```

5. **Rollback if needed:**
```bash
alembic downgrade -1
```

---

### Adding New Endpoints

1. **Create route file:**
```python
# app/routes/my_feature.py
from flask import Blueprint, jsonify

my_feature_bp = Blueprint('my_feature', __name__)

@my_feature_bp.route('/my-endpoint', methods=['GET'])
def my_endpoint():
    return jsonify({"message": "Hello!"})
```

2. **Register blueprint:**
```python
# app/__init__.py
from app.routes.my_feature import my_feature_bp
app.register_blueprint(my_feature_bp, url_prefix='/api')
```

3. **Test:**
```bash
curl http://localhost:5000/api/my-endpoint
```

---

### Testing

```bash
# Manual testing
curl http://localhost:5000/api/health

# With pytest (if tests are added)
pytest
```

---

## 🐛 Troubleshooting

### "No module named 'dotenv'"
**Solution:**
```bash
pip install python-dotenv
# or
pip install -r requirements.txt
```

---

### "Cannot connect to database"
**Causes:**
- DATABASE_URL is incorrect
- Neon database is sleeping (free tier)
- Network/firewall blocking connection

**Solution:**
1. Check DATABASE_URL in `.env`
2. Visit Neon dashboard - database wakes up when accessed
3. Try creating tables via Neon SQL Editor instead of local migration

---

### "GOOGLE_CREDENTIALS_JSON not found"
**Solution:**
- Copy credentials from Google Cloud Console
- Paste entire JSON into .env
- Make sure it's on one line or properly escaped

---

### "Port 5000 already in use"
**Solution:**
```bash
# Kill process
lsof -ti:5000 | xargs kill -9

# Or change port in .env
FLASK_PORT=5001
```

---

### Alembic Migration Fails
**Solutions:**

1. **Create tables directly in Neon SQL Editor**
2. **Check database connection:** Ensure DATABASE_URL is correct
3. **Skip migration and use db.create_all():**
```python
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
```

---

## 🚀 Deployment

### Deploy to Railway

1. **Create Railway account:** https://railway.app
2. **Connect GitHub repo**
3. **Add environment variables** (from .env)
4. **Railway auto-detects** Python/Flask
5. **Deploy!**

### Deploy to Render

1. **Create Render account:** https://render.com
2. **New Web Service** → Connect repo
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `gunicorn run:app`
5. **Add environment variables**
6. **Deploy!**

### Deploy to Vercel (Serverless)

1. **Install Vercel CLI:** `npm i -g vercel`
2. **Create `vercel.json`:**
```json
{
  "builds": [
    {"src": "run.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/(.*)", "dest": "run.py"}
  ]
}
```
3. **Deploy:** `vercel --prod`

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment | `development` or `production` |
| `FLASK_DEBUG` | Debug mode | `True` or `False` |
| `FLASK_PORT` | Server port | `5000` |
| `SECRET_KEY` | Session encryption | Random string |
| `PROJECT_ID` | GCP project ID | `my-project-123` |
| `LOCATION` | GCP region | `us-central1` |
| `GOOGLE_CREDENTIALS_JSON` | Service account JSON | Full JSON object |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host/db` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000` |
| `MAX_UPLOAD_SIZE_MB` | Max file size | `10` |
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG`, `ERROR` |

---

## 🎓 Key Concepts

### Why Stateless API?
- Each request is independent
- No server-side sessions (except database)
- Easy to scale horizontally
- Works great with modern frontends (Next.js, React)

### Why JSON Schemas?
- Validate AI responses match expected format
- Catch errors early
- Ensure frontend gets consistent data
- Self-documenting API

### Why JSONB in PostgreSQL?
- Flexible structure for biomarkers (each lab has different tests)
- Still queryable with SQL
- Fast indexing
- Best of both worlds: structure + flexibility

---

## 🆘 Need Help?

1. **Check this guide** - Most answers are here
2. **Read error messages** - They usually tell you what's wrong
3. **Check logs** - `tail -f backend.log`
4. **Google the error** - With "Flask" or "SQLAlchemy"
5. **Ask the team** - Someone probably solved it before

---

## 📚 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Tutorial:** https://docs.sqlalchemy.org/en/20/tutorial/
- **Alembic Guide:** https://alembic.sqlalchemy.org/
- **Neon Documentation:** https://neon.tech/docs
- **Google Vertex AI:** https://cloud.google.com/vertex-ai/docs
- **PostgreSQL Guide:** https://www.postgresql.org/docs/

---

**🎉 You're ready to build with HealthAI backend!**

For questions or issues, check the troubleshooting section or reach out to the team.

**Happy Coding! 🚀**
