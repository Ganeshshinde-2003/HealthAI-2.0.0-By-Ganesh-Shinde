# Nova Health - AI-Powered Health Analysis Platform (v2.0)

> Your personal health intelligence layer powered by Google Vertex AI

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15.1.0-black.svg)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7.2-blue.svg)](https://www.typescriptlang.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4.svg)](https://cloud.google.com/vertex-ai)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

---

## 🌟 Overview

Nova Health (formerly HealthAI) combines advanced AI with functional medicine principles to provide personalized, comprehensive health insights. **Version 2.0** features a completely redesigned architecture with separated backend and frontend for better scalability, performance, and user experience.

### ✨ Key Features

- 🔬 **Comprehensive Biomarker Analysis** - 50+ biomarkers with optimal vs clinical ranges
- 💪 **Four Pillars Framework** - Personalized scoring for Eat, Sleep, Move, Recover
- 📊 **Monthly Health Reports** - Longitudinal trend analysis with visualizations
- 💊 **Smart Supplement Recommendations** - Evidence-based, personalized dosing
- 🎯 **Root Cause Analysis** - Identifies underlying health patterns
- 🔒 **HIPAA-Compliant** - Secure processing with Google Cloud infrastructure
- 🚀 **Modern Architecture** - RESTful API with responsive Next.js frontend
- 📱 **Mobile-Ready** - Fully responsive design for all devices

---

## 🏗️ Architecture

### Version 2.0 - Separated Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│                     │         │                     │
│   Next.js Frontend  │────────▶│   Flask Backend     │
│   (TypeScript)      │  HTTP   │   (Python)          │
│                     │◀────────│                     │
│   Port: 3000        │  JSON   │   Port: 5000        │
│                     │         │                     │
└─────────────────────┘         └─────────────────────┘
                                          │
                                          │
                                          ▼
                                ┌─────────────────────┐
                                │                     │
                                │  Google Vertex AI   │
                                │  (Gemini 2.5)       │
                                │                     │
                                └─────────────────────┘
```

### Technology Stack

#### Backend
- **Framework**: Flask 3.1.0
- **AI Model**: Google Vertex AI - Gemini 2.5 Flash Lite
- **File Processing**: PyMuPDF, python-docx, pandas, openpyxl
- **Validation**: jsonschema
- **Server**: Gunicorn (production)

#### Frontend
- **Framework**: Next.js 15.1.0 with App Router
- **Language**: TypeScript 5.7.2
- **Styling**: Tailwind CSS 3.4.17
- **HTTP Client**: Axios 1.7.9
- **UI Components**: Custom React components with Lucide icons
- **File Upload**: react-dropzone 14.3.5

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google Cloud Platform account with Vertex AI enabled
- Service account with Vertex AI permissions

### 5-Minute Setup

1. **Clone and navigate to the project**
   ```bash
   cd /path/to/ai-health-analyser
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your GCP credentials
   python run.py
   ```
   Backend runs at: `http://localhost:5000` ✅

3. **Setup Frontend** (new terminal)
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local if needed
   npm run dev
   ```
   Frontend runs at: `http://localhost:3000` ✅

4. **Open browser and start analyzing!**
   ```
   http://localhost:3000
   ```

For detailed setup instructions, see **[SETUP.md](SETUP.md)**

---

## 📱 Applications

### 1. Health Analyzer
Comprehensive health analysis with lab reports and health assessments.

**URL**: `http://localhost:3000/`

**Features:**
- Multi-format file upload (PDF, DOCX, Excel, CSV, TXT)
- Real-time AI analysis with progress tracking
- Interactive results display with expandable sections
- Biomarker categorization (Optimal, Keep in Mind, Attention Needed)
- Four Pillars wellness scoring
- Personalized supplement recommendations
- Download results as JSON

**Use Case:** Individual health analysis, health coaching

---

### 2. Monthly Health Reporter
Longitudinal health tracking with trend analysis.

**URL**: `http://localhost:3000/monthly-report`

**Features:**
- Monthly overview and trend summary
- Key improvements and areas of focus tracking
- Daily log pattern analysis
- Historical trend visualization
- Behavior goal tracking
- Root cause identification
- Downloadable monthly reports

**Use Case:** Long-term health tracking, progress monitoring

---

## 🔧 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```
Returns API status and version information.

#### Analyze Health Data
```http
POST /api/analyze
Content-Type: multipart/form-data

lab_reports: File[] (required)
health_assessment: File (optional)
```
Returns complete health analysis including biomarkers, four pillars, and supplements.

#### Generate Monthly Report
```http
POST /api/monthly-report
Content-Type: multipart/form-data

previous_lab_report: File (required)
daily_logs: File (required)
weekly_assessments: File (optional)
```
Returns comprehensive monthly health report with trends.

For complete API documentation, see **[API.md](API.md)** (to be created)

---

## 💡 Usage

### For Individuals

1. **Prepare your files:**
   - Lab report (PDF, DOCX, or Excel)
   - Health assessment (symptoms, concerns, goals)

2. **Upload and analyze:**
   - Go to `http://localhost:3000`
   - Upload files through the drag-and-drop interface
   - Click "Analyze My Data ✨"
   - Wait 30-60 seconds for AI processing

3. **Review insights:**
   - Browse categorized biomarker results
   - Review Four Pillars scores and recommendations
   - Check personalized supplement suggestions
   - Download JSON for your records

### For Health Professionals

- Process multiple clients efficiently
- Export analysis results as JSON
- Track Four Pillars scores over time
- Prepare personalized interventions
- Share results securely

---

## 📦 Project Structure

```
ai-health-analyser/
├── backend/                    # Flask Backend
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── routes/            # API endpoints
│   │   │   ├── health.py      # Health check
│   │   │   ├── analysis.py    # Health analysis
│   │   │   ├── monthly.py     # Monthly reports
│   │   │   └── chat.py        # Chat (future)
│   │   ├── services/          # Business logic
│   │   │   ├── analysis_service.py
│   │   │   └── monthly_service.py
│   │   └── utils/             # Utilities
│   │       ├── ai_client.py   # Vertex AI client
│   │       ├── file_processor.py
│   │       ├── validators.py
│   │       └── prompt_loader.py
│   ├── config/
│   │   └── config.py          # Configuration
│   ├── prompts/               # AI prompts & schemas
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Entry point
│   └── .env.example           # Environment template
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App router pages
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Health analyzer
│   │   │   └── monthly-report/
│   │   │       └── page.tsx   # Monthly report
│   │   ├── components/        # React components
│   │   │   ├── FileUpload.tsx
│   │   │   ├── AnalysisResults.tsx
│   │   │   └── LoadingAnalysis.tsx
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts         # API client
│   │   │   └── utils.ts       # Helper functions
│   │   ├── types/             # TypeScript types
│   │   │   └── index.ts
│   │   └── styles/            # Styles
│   │       └── globals.css
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.js     # Tailwind config
│   └── .env.example           # Environment template
│
├── MIGRATION.md               # Migration documentation
├── SETUP.md                   # Setup instructions
├── README.md                  # This file (v1 - Streamlit)
└── README-V2.md               # This file (v2 - Flask + Next.js)
```

---

## 🔒 Privacy & Security

- ✅ No persistent storage of health data
- ✅ HIPAA-compliant Google Cloud infrastructure
- ✅ Encrypted credential management
- ✅ No third-party analytics or tracking
- ✅ Secure API communication with CORS protection
- ✅ Environment-based configuration
- ✅ Input validation and sanitization

**Important:** This application is for educational purposes. Always consult a licensed healthcare provider for medical decisions.

---

## 📋 What's New in v2.0

### Improvements

✅ **Separated Architecture** - Independent backend and frontend for better scalability
✅ **Modern Tech Stack** - Latest versions of all frameworks and libraries
✅ **RESTful API** - Clean API design following best practices
✅ **TypeScript** - Type-safe frontend development
✅ **Responsive Design** - Mobile-first, works on all devices
✅ **Better Performance** - Optimized bundle size and load times
✅ **Developer Experience** - Hot reload, better error handling, clearer logs
✅ **Deployment Ready** - Docker support, production configurations

### Migration from v1.0

If you're migrating from the Streamlit version, see **[MIGRATION.md](MIGRATION.md)** for:
- Detailed architecture comparison
- Component mapping guide
- Setup instructions
- Breaking changes
- Testing guidelines

---

## 🤝 Contributing

This is currently a personal project. Feedback and suggestions are welcome!

### Reporting Issues
- Check existing issues first
- Provide detailed description
- Include steps to reproduce
- Share relevant error messages
- Specify environment (OS, Python version, Node version)

---

## 📝 License

Proprietary - All rights reserved by Ganesh Shinde.

---

## 👤 Author

**Ganesh Shinde**

- Personal health analysis platform
- Built with passion for precision health and wellness
- Email: [contact information]
- LinkedIn: [LinkedIn profile]

---

## 🙏 Acknowledgments

- Google Cloud Platform & Vertex AI for powerful AI capabilities
- Flask and Next.js communities for excellent frameworks
- Python and JavaScript ecosystems for robust libraries
- Functional medicine and precision health movement for inspiration

---

## 📧 Support

For questions, issues, or feedback:
- Open an issue on GitHub
- Check **[SETUP.md](SETUP.md)** for setup help
- Check **[MIGRATION.md](MIGRATION.md)** for architecture details
- Review API logs for debugging

---

## ⚠️ Disclaimer

**Medical Disclaimer:** Nova Health is provided for informational and educational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease or health condition. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it because of information provided by this application.

**AI Disclaimer:** Results generated by AI models may contain errors or inaccuracies. Always verify recommendations with qualified healthcare professionals.

---

## 📊 Version History

**Version 2.0.0** (Current)
- Complete architecture overhaul
- Flask + Next.js separation
- Latest package versions
- Enhanced UI/UX
- RESTful API design

**Version 1.0.0**
- Initial Streamlit-based application
- Basic health analysis
- Monthly reporting

---

## 🔮 Roadmap

### Phase 1 (Current)
- [x] Separate backend and frontend
- [x] Modern tech stack implementation
- [x] Core functionality migration
- [ ] Comprehensive testing
- [ ] Performance optimization

### Phase 2 (Q2 2026)
- [ ] User authentication and authorization
- [ ] Database integration for history
- [ ] Real-time progress updates (WebSocket)
- [ ] Enhanced data visualizations
- [ ] PDF report generation

### Phase 3 (Q3 2026)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and trends
- [ ] AI chat assistant
- [ ] Doctor integration features
- [ ] Multi-language support

### Phase 4 (Q4 2026)
- [ ] Wearable device integration
- [ ] Community features
- [ ] Telehealth integration
- [ ] Insurance integration
- [ ] Enterprise features

---

**Built with ❤️ for precision health and personalized wellness**

*Last Updated: April 24, 2026*

---

## 📚 Documentation Index

- **[SETUP.md](SETUP.md)** - Complete setup and installation guide
- **[MIGRATION.md](MIGRATION.md)** - Migration from v1.0 to v2.0
- **[API.md](API.md)** - API documentation (to be created)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines (to be created)
- **[CHANGELOG.md](CHANGELOG.md)** - Version history (to be created)
