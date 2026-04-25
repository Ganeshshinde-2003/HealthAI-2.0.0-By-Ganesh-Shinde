# Setup Guide - Nova Health (HealthAI v2.0)

Complete setup instructions for the Flask + Next.js architecture.

---

## 📋 Prerequisites

### Required Software

- **Python** 3.9 or higher
- **Node.js** 18.0 or higher
- **npm** 9.0 or higher (comes with Node.js)
- **Git** (for version control)

### Google Cloud Platform

- Active GCP project with billing enabled
- Vertex AI API enabled
- Service account with Vertex AI permissions
- Service account JSON key file downloaded

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
cd /path/to/ai-health-analyser
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install latest dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your preferred editor
```

**Required `.env` values:**
```bash
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

```bash
# Start backend server
python run.py
```

Backend should now be running at: `http://localhost:5000` ✅

### Step 3: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install latest dependencies
npm install

# Configure environment
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Required `.env.local` values:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

```bash
# Start frontend development server
npm run dev
```

Frontend should now be running at: `http://localhost:3000` ✅

### Step 4: Test the Application

1. Open browser: `http://localhost:3000`
2. Upload a lab report (PDF, DOCX, or Excel)
3. Click "Analyze My Data ✨"
4. View results!

---

## 📁 Detailed Setup

### Backend Configuration

#### Option 1: Using Service Account File

1. Download your GCP service account JSON file
2. Place it in a secure location (e.g., `~/.gcp/healthai-credentials.json`)
3. Update `.env`:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=/Users/yourname/.gcp/healthai-credentials.json
   ```

#### Option 2: Using Application Default Credentials

```bash
gcloud auth application-default login
```

Then in `.env`:
```bash
# GOOGLE_APPLICATION_CREDENTIALS can be omitted
```

### Frontend Configuration

The frontend only needs the backend API URL:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_MAX_FILE_SIZE_MB=10
```

---

## 🔧 Development Workflow

### Running Both Servers

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Auto-Reload

- **Backend**: Flask auto-reloads on file changes when `FLASK_DEBUG=True`
- **Frontend**: Next.js auto-reloads on file changes automatically

### Checking Health

**Backend Health Check:**
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "HealthAI Backend API",
  "version": "2.0.0",
  "environment": "development"
}
```

---

## 📦 Package Management

### Backend (Python)

**Install new package:**
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

**Update all packages to latest:**
```bash
pip install --upgrade -r requirements.txt
```

### Frontend (Node.js)

**Install new package:**
```bash
npm install package-name
# or for dev dependencies
npm install --save-dev package-name
```

**Update all packages:**
```bash
npm update
```

**Check for outdated packages:**
```bash
npm outdated
```

---

## 🏭 Production Deployment

### Backend (Gunicorn)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app('production')"

# With logs
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile access.log \
  --error-logfile error.log \
  "backend.app:create_app('production')"
```

### Frontend (Next.js)

```bash
# Build for production
npm run build

# Start production server
npm start

# Or use PM2
npm install -g pm2
pm2 start npm --name "healthai-frontend" -- start
```

### Using Docker (Optional)

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:create_app()"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    env_file:
      - ./backend/.env

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:5000/api
    depends_on:
      - backend
```

---

## 🔍 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill -9 <PID>
```

**Import errors:**
```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

**Vertex AI errors:**
```bash
# Verify credentials
gcloud auth application-default login

# Check project ID
echo $GCP_PROJECT_ID

# Test Vertex AI access
gcloud ai models list --region=us-central1
```

### Frontend Issues

**Port already in use:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

**Module not found:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
1. Verify backend is running: `curl http://localhost:5000/api/health`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check browser console for CORS errors

### Common Issues

**CORS Errors:**
- Verify backend CORS is configured
- Check `frontend` URL is allowed in backend CORS settings
- Try clearing browser cache

**File Upload Fails:**
- Check file size < 10MB
- Verify file type is supported (PDF, DOCX, XLSX, XLS, TXT, CSV)
- Check backend logs for errors

**Slow Analysis:**
- First analysis may take 60-90 seconds
- Check Vertex AI quotas in GCP console
- Verify network connection

---

## 📊 Monitoring

### Backend Logs

```bash
# View logs in development
tail -f logs/backend.log

# Or see output in terminal running backend
```

### Frontend Logs

```bash
# View Next.js logs
# Check terminal running npm run dev

# Browser console
# Open DevTools → Console tab
```

### Health Monitoring

Create a simple monitoring script:

```bash
#!/bin/bash
# monitor.sh

while true; do
  echo "Checking backend health..."
  curl -s http://localhost:5000/api/health | jq

  echo "Checking frontend..."
  curl -s http://localhost:3000 > /dev/null && echo "Frontend OK" || echo "Frontend DOWN"

  sleep 60
done
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run manual tests
python -m pytest tests/

# Test specific endpoint
curl -X POST http://localhost:5000/api/analyze \
  -F "lab_reports=@sample_data/test_lab.pdf"
```

### Frontend Tests

```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` files**
   - Added to `.gitignore` by default

2. **Use strong secret keys**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Rotate credentials regularly**
   - Update GCP service account keys every 90 days

4. **Use environment-specific configs**
   - Separate `.env` for dev/staging/prod

5. **Enable HTTPS in production**
   - Use nginx or similar reverse proxy
   - Get SSL certificate (Let's Encrypt)

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Google Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs/)

---

## ✅ Setup Checklist

### Backend
- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` configured with GCP credentials
- [ ] Backend server starts without errors
- [ ] Health check endpoint responds

### Frontend
- [ ] Node.js 18+ installed
- [ ] Dependencies installed
- [ ] `.env.local` configured
- [ ] Frontend server starts without errors
- [ ] Can access at localhost:3000

### Integration
- [ ] Frontend can communicate with backend
- [ ] File upload works
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] Download JSON works

---

## 🎉 Success!

If you've completed all steps, you should have:
- ✅ Backend API running on port 5000
- ✅ Frontend UI running on port 3000
- ✅ Ability to upload files and get AI analysis
- ✅ Modern, responsive UI with Nova Health branding

Enjoy using Nova Health! 🌿

---

**Need Help?** Check MIGRATION.md for architecture details or open an issue on GitHub.
