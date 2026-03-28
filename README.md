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
   streamlit run prompt_tester.py
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

### 3. Prompt Testing Version (`prompt_tester.py`)
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

## 🔒 Privacy & Security

- ✅ No persistent storage of health data
- ✅ HIPAA-compliant Google Cloud infrastructure
- ✅ Encrypted credential management
- ✅ No third-party analytics or tracking
- ✅ Local file processing

**Important:** This application is for educational purposes. Always consult a licensed healthcare provider for medical decisions.

---

## 📦 Project Structure

```
ai-health-analyser/
├── app.py                  # Standard health analyzer
├── monthly_report.py       # Monthly health reporter
├── prompt_tester.py        # Prompt testing version
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── utils/                 # Utility modules
│   ├── ai_client.py       # AI client wrapper
│   ├── display.py         # Display components
│   ├── file_processor.py  # File handling
│   ├── prompt_loader.py   # Prompt management
│   └── validators.py      # JSON validation
├── prompts/               # AI prompt templates
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

- Personal health analysis platform
- Built with passion for precision health and wellness

---

## 🙏 Acknowledgments

- Google Cloud Platform & Vertex AI
- Streamlit for rapid UI development
- Python community for excellent libraries
- Functional medicine and precision health movement

---

## 📧 Support

For questions, issues, or feedback, please open an issue on GitHub.

---

## ⚠️ Disclaimer

**Medical Disclaimer:** HealthAI is provided for informational and educational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease or health condition. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it because of information provided by this application.

**AI Disclaimer:** Results generated by AI models may contain errors or inaccuracies. Always verify recommendations with qualified healthcare professionals.

---

## 📊 Version

**Current Version:** 1.0.0
**Release Date:** March 28, 2026
**Status:** Production Ready (MVP)

---

**Built with ❤️ for precision health and personalized wellness**

*Last Updated: March 28, 2026*
