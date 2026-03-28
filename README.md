# HealthAI - AI-Powered Health Analysis Platform

> Personal health analysis application powered by Google Vertex AI, specializing in personalized health and precision medicine.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50.0-FF4B4B.svg)](https://streamlit.io)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4.svg)](https://cloud.google.com/vertex-ai)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

---

## 🌟 Overview

HealthAI combines advanced AI with functional medicine principles to provide personalized, comprehensive health insights. Built with a precision health approach, it analyzes lab reports, daily health logs, and wellness assessments to deliver actionable recommendations tailored to each individual's unique biology and health goals.

### ✨ Key Features

- 🔬 **Comprehensive Biomarker Analysis** - 50+ biomarkers with optimal vs clinical ranges
- 💪 **Four Pillars Framework** - Personalized scoring for Eat, Sleep, Move, Recover
- 📊 **Monthly Health Reports** - Trend analysis with radar chart visualization
- 💊 **Smart Supplement Recommendations** - Evidence-based, personalized dosing
- 🎯 **Root Cause Analysis** - Identifies underlying health patterns
- 🔒 **HIPAA-Compliant** - Secure processing with Google Cloud infrastructure

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Cloud Platform account with Vertex AI enabled
- pip or pip3 package manager

### Installation

1. **Clone or download the repository**
   ```bash
   cd /path/to/ai-health-analyser
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure Google Cloud credentials**

   Create `.streamlit/secrets.toml`:
   ```toml
   PROJECT_ID = "your-gcp-project-id"
   LOCATION = "us-central1"
   google_credentials = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "service-account@project.iam.gserviceaccount.com",
     ...
   }
   '''
   ```

4. **Run the application**
   ```bash
   # Standard health analyzer
   streamlit run app.py

   # Monthly health reporter
   streamlit run monthly_report.py

   # Prompt testing version (for developers)
   streamlit run app2.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

---

## 📱 Applications

### 1. Standard Health Analyzer (`app.py`)
Comprehensive health analysis with lab reports and health assessments.

**Features:**
- Multi-format file upload (PDF, DOCX, Excel, CSV, TXT)
- Biomarker analysis with optimal ranges
- Four Pillars wellness scoring
- Supplement recommendations
- Interactive JSON output

**Use Case:** Individual health analysis, health coaching

---

### 2. Monthly Health Reporter (`monthly_report.py`)
Longitudinal health tracking with trend analysis.

**Features:**
- Monthly overview and trend summary
- Hormonal balance insights
- Daily log pattern analysis
- Radar chart visualization
- Behavior goal tracking
- Root cause identification

**Use Case:** Long-term health tracking, progress monitoring

---

### 3. Prompt Testing Version (`app2.py`)
Development version with live prompt editing.

**Features:**
- All features from standard analyzer
- Real-time prompt modification
- Debugging tools
- AI response testing

**Use Case:** Development, prompt optimization, QA testing

---

## 💡 Usage

### For Individuals

1. **Prepare your files:**
   - Lab report (PDF, DOCX, or Excel)
   - Health assessment (symptoms, concerns, goals)

2. **Upload and analyze:**
   - Upload files through the interface
   - Click "Analyze My Data ✨"
   - Wait 30-60 seconds for AI processing

3. **Review insights:**
   - Browse interactive JSON output
   - Copy full JSON for your records
   - Implement recommendations

### For Health Professionals

- Process multiple clients sequentially
- Save JSON outputs for client records
- Track Four Pillars scores over time
- Prepare personalized interventions

---

## 🏗️ Architecture

```
User Interface (Streamlit)
         ↓
File Processing Layer
         ↓
AI Processing Engine (Vertex AI - Gemini 2.5 Flash Lite)
    ├── Biomarker Analysis
    ├── Four Pillars Analysis
    └── Supplements Analysis
         ↓
JSON Validation & Output
```

### Technology Stack

- **Frontend:** Streamlit 1.50.0
- **AI Model:** Google Vertex AI - Gemini 2.5 Flash Lite
- **File Processing:** PyMuPDF, python-docx, pandas, openpyxl
- **Validation:** jsonschema
- **Cloud:** Google Cloud Platform

---

## 📚 Documentation

- **[product.md](product.md)** - Comprehensive product documentation
- **[claude.md](claude.md)** - AI development tracking log
- **[changelog.md](changelog.md)** - Version history and changes

---

## 🔒 Privacy & Security

- ✅ No persistent storage of health data
- ✅ HIPAA-compliant Google Cloud infrastructure
- ✅ Encrypted credential management
- ✅ No third-party analytics or tracking
- ✅ Local file processing

**Important:** This application is for educational purposes. Always consult a licensed healthcare provider for medical decisions.

---

## 🛣️ Roadmap

### Phase 1: Foundation Enhancement (Q2 2026)
- [ ] Refactor shared code into utilities module
- [ ] Add comprehensive test suite
- [ ] Implement file size validation
- [ ] Add type hints throughout codebase

### Phase 2: Feature Expansion (Q3 2026)
- [ ] User authentication and profiles
- [ ] Data persistence and history tracking
- [ ] Trend visualization (charts/graphs)
- [ ] PDF report generation

### Phase 3: Advanced Intelligence (Q4 2026)
- [ ] Predictive health modeling
- [ ] Wearable device integration
- [ ] Optional cycle tracking and hormonal insights
- [ ] Medication interaction checking

### Phase 4: Platform Expansion (2027)
- [ ] Mobile application (iOS/Android)
- [ ] Practitioner dashboard
- [ ] Telehealth integration

See [product.md](product.md) for detailed roadmap.

---

## 📦 Project Structure

```
ai-health-analyser/
├── app.py                  # Standard health analyzer
├── app2.py                 # Prompt testing version
├── monthly_report.py       # Monthly health reporter
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── product.md             # Product documentation
├── claude.md              # AI development log
├── changelog.md           # Version history
└── .streamlit/
    └── secrets.toml       # Google Cloud credentials (not in repo)
```

---

## 🤝 Contributing

This is currently a personal project. Feedback and suggestions are welcome!

### Reporting Issues
- Check existing issues first
- Provide detailed description
- Include steps to reproduce
- Share relevant error messages

---

## 📝 License

Proprietary - All rights reserved by Ganesh Shinde.

---

## 👤 Author

**Ganesh Shinde**

- Created: March 2026
- Purpose: Personal health analysis tool
- Originally built for: Previous company (personal IP retained)

---

## 🙏 Acknowledgments

- Google Cloud Platform & Vertex AI
- Streamlit for rapid UI development
- Python community for excellent libraries
- Functional medicine and precision health movement

---

## 📧 Support

For questions, issues, or feedback:
- Review the [documentation](product.md)
- Check the [changelog](changelog.md)
- Open an issue on GitHub

---

## ⚠️ Disclaimer

**Medical Disclaimer:** HealthAI is provided for informational and educational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease or health condition. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it because of information provided by this application.

**AI Disclaimer:** Results generated by AI models may contain errors or inaccuracies. Always verify recommendations with qualified healthcare professionals.

---

## 📊 Version

**Current Version:** 1.0.0
**Release Date:** March 28, 2026
**Status:** Production Ready (MVP)

See [changelog.md](changelog.md) for version history.

---

## 🔗 Quick Links

- [Product Documentation](product.md) - Detailed feature guide
- [Development Log](claude.md) - AI development tracking
- [Version History](changelog.md) - Complete changelog
- [Google Cloud Console](https://console.cloud.google.com) - Manage credentials
- [Streamlit Docs](https://docs.streamlit.io) - Framework documentation

---

**Built with ❤️ for precision health and personalized wellness**

*Last Updated: March 28, 2026*
