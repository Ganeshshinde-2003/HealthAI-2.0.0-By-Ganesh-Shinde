# HealthAI Backend Setup Guide

## Setting Up on a New Device

Follow these steps to run the HealthAI backend on any device after cloning from GitHub.

---

## Prerequisites

- Python 3.9 or higher (Python 3.10+ recommended)
- pip (Python package manager)
- Git

---

## Step 1: Clone the Repository

```bash
git clone <your-github-repo-url>
cd ai-health-analyser/backend
```

---

## Step 2: Create Virtual Environment

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Flask
- python-dotenv
- SQLAlchemy
- Google Cloud libraries
- And all other dependencies

**If you get errors**, upgrade pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 4: Set Up Environment Variables

### Create `.env` file

Create a new file called `.env` in the `backend/` directory:

```bash
touch .env
```

### Copy from `.env.example`

Use `.env.example` as a template:

```bash
cp .env.example .env
```

### Fill in your actual values

Edit `.env` and add your actual credentials:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here

# Google Cloud Platform
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}

# Database
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# File Upload
MAX_UPLOAD_SIZE_MB=10

# Logging
LOG_LEVEL=INFO
```

**Important:** Never commit `.env` to Git (it's already in `.gitignore`)

---

## Step 5: Create Upload Directory

```bash
mkdir -p uploads
```

---

## Step 6: Run the Backend

```bash
python run.py
```

Or using Flask directly:
```bash
flask run
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

---

## Step 7: Test the API

Open a new terminal and test:

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

## Troubleshooting

### Error: "No module named 'dotenv'"

**Solution:**
```bash
pip install python-dotenv
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Virtual environment not activated or dependencies not installed
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Error: "Cannot connect to database"

**Solution:**
- Check DATABASE_URL in `.env` is correct
- For local development, database connection errors won't affect API (it runs in stateless mode)
- Database is only needed for saving data

### Error: "Missing GOOGLE_CREDENTIALS_JSON"

**Solution:**
- Copy credentials from `.streamlit/secrets.toml` if you have it
- Or get from Google Cloud Console
- Or run without Google AI features (will fail on /analyze endpoint)

### Port 5000 already in use

**Solution:** Kill the process or use a different port
```bash
# Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9

# Or change port in .env
FLASK_PORT=5001
```

### Import errors after installing dependencies

**Solution:** Make sure virtual environment is activated
```bash
which python  # Should show path to venv/bin/python
```

If not in venv:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

## Quick Start Script

Create a script to automate setup:

### `setup.sh` (macOS/Linux):

```bash
#!/bin/bash
echo "Setting up HealthAI Backend..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your credentials."
fi

# Create uploads directory
mkdir -p uploads

echo "Setup complete! Edit .env file, then run: python run.py"
```

Make it executable:
```bash
chmod +x setup.sh
./setup.sh
```

### `setup.bat` (Windows):

```batch
@echo off
echo Setting up HealthAI Backend...

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your credentials.
)

if not exist uploads mkdir uploads

echo Setup complete! Edit .env file, then run: python run.py
pause
```

---

## Production Deployment

For production deployment (Vercel, Railway, Render, etc.):

1. **Environment Variables:** Add all `.env` variables in your hosting platform's dashboard
2. **Database:** Ensure DATABASE_URL points to production database (Neon, etc.)
3. **CORS:** Update CORS_ORIGINS with your frontend URL
4. **Secret Key:** Use a strong, random SECRET_KEY
5. **Debug Mode:** Set FLASK_DEBUG=False and FLASK_ENV=production

---

## File Checklist

Make sure these files exist:
- ✅ `requirements.txt`
- ✅ `run.py`
- ✅ `.env` (create from `.env.example`)
- ✅ `.gitignore` (should include `.env`, `venv/`, etc.)
- ✅ `app/` directory with all routes and services
- ✅ `config/` directory
- ✅ `uploads/` directory (create it)

---

## Common Setup Flow

```bash
# 1. Clone repo
git clone <repo-url>
cd ai-health-analyser/backend

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Create uploads folder
mkdir -p uploads

# 6. Run backend
python run.py
```

---

## Dependencies Included

Your `requirements.txt` includes:
- Flask 3.1.0 (web framework)
- Flask-CORS 5.0.0 (CORS handling)
- **python-dotenv 1.0.1** (environment variables)
- gunicorn 23.0.0 (production server)
- google-cloud-aiplatform 1.70.0 (AI services)
- SQLAlchemy 2.0.36 (database ORM)
- psycopg2-binary 2.9.10 (PostgreSQL driver)
- And more...

All will be installed with `pip install -r requirements.txt`

---

## Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Ensure Python version is 3.9+
3. Verify virtual environment is activated
4. Make sure `.env` file exists with correct values
5. Check that all dependencies installed successfully

---

## Next Steps After Setup

1. Test all API endpoints
2. Set up database (see `DATABASE_SETUP.md`)
3. Deploy to production (optional)
4. Connect frontend to backend
