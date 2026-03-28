"""
Configuration file for HealthAI application.
Centralizes all configuration constants and settings.
"""

# ==========================================
# AI Model Configuration
# ==========================================

class AIConfig:
    """Configuration for HealthAI and Gemini model."""

    # Model Selection
    MODEL_NAME = "gemini-2.5-flash-lite"

    # Generation Configuration
    TEMPERATURE = 0.2  # Low for deterministic JSON output
    TOP_P = 0.95
    TOP_K = 64
    MAX_OUTPUT_TOKENS_STANDARD = 65535  # For standard analysis
    MAX_OUTPUT_TOKENS_MONTHLY = 8192    # For monthly reports
    RESPONSE_MIME_TYPE = "application/json"

    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2
    INITIAL_RETRY_DELAY = 1


# ==========================================
# File Processing Configuration
# ==========================================

class FileConfig:
    """Configuration for file upload and processing."""

    # Supported File Types
    SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]

    # File Size Limits (in bytes)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Text Extraction Settings
    TEXT_ENCODING = "utf-8"
    ENCODING_ERROR_HANDLING = "ignore"


# ==========================================
# Safety Settings
# ==========================================

class SafetyConfig:
    """Safety settings for AI model harm categories."""

    # Using strings that will be converted to enums in ai_client.py
    HARASSMENT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    HATE_SPEECH_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    SEXUALLY_EXPLICIT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"
    DANGEROUS_CONTENT_THRESHOLD = "BLOCK_MEDIUM_AND_ABOVE"


# ==========================================
# Google Cloud Configuration
# ==========================================

class GCPConfig:
    """Google Cloud Platform configuration."""

    # Default location for HealthAI
    DEFAULT_LOCATION = "us-central1"

    # These will be loaded from Streamlit secrets
    # PROJECT_ID - from st.secrets.get("PROJECT_ID")
    # LOCATION - from st.secrets.get("LOCATION", DEFAULT_LOCATION)
    # google_credentials - from st.secrets.get("google_credentials")


# ==========================================
# UI Configuration
# ==========================================

class UIConfig:
    """Streamlit UI configuration."""

    # Page Configuration
    PAGE_TITLE_ANALYZER = "HealthAI Health Analyzer - HIPAA by HealthAI - VP1"
    PAGE_TITLE_ANALYZER_TEST = "HealthAI Health Analyzer - HIPAA by HealthAI - VP1"
    PAGE_TITLE_MONTHLY = "HealthAI Monthly Health Reporter - HIPAA by HealthAI"
    PAGE_ICON_ANALYZER = "🌿"
    PAGE_ICON_MONTHLY = "🗓️"
    LAYOUT = "wide"

    # Status Messages
    ANALYSIS_INITIATING = "Initiating HealthAI Analysis..."
    ANALYSIS_COMPLETE = "HealthAI Analysis Complete!"
    MONTHLY_INITIATING = "Generating monthly report..."
    MONTHLY_COMPLETE = "Monthly Report Generated!"

    # Headers
    HEADER_MAIN_ANALYZER = "🌿 Your Personal AI Health Assistant – HIPAA Secure by HealthAI"
    HEADER_MAIN_ANALYZER_TEST = "🌿 Your Personal AI Health Assistant – HIPAA Secure by HealthAI"
    HEADER_MAIN_MONTHLY = "HealthAI Monthly Health Reporter – HIPAA Secure by HealthAI"
    HEADER_RESULTS = "🔬 Your Personalized HealthAI Analysis (Interactive JSON):"
    HEADER_RESULTS_MONTHLY = "✨ Your Personalized HealthAI Monthly Health Report:"
    HEADER_COPY_JSON = "📋 Copy Full JSON Output (Plain Text):"

    # Button Labels
    BUTTON_ANALYZE = "Analyze My Data ✨"
    BUTTON_MONTHLY = "Generate Monthly Report ✨"


# ==========================================
# Application Metadata
# ==========================================

class AppMetadata:
    """Application metadata and versioning."""

    APP_NAME = "HealthAI"
    VERSION = "1.0.0"
    AUTHOR = "Ganesh Shinde"
    DESCRIPTION = "AI-Powered Health Analysis Platform"

    # AI Attribution
    AI_ASSISTANT_NAME = "HealthAI Assistant"
    AI_ASSISTANT_MONTHLY_NAME = "HealthAI Monthly Health Report Assistant"


# ==========================================
# Prompt File Paths
# ==========================================

class PromptPaths:
    """Paths to prompt template files."""

    BASE_DIR = "prompts"
    SCHEMAS_DIR = "prompts/schemas"

    # Prompt Templates
    BASE_PROMPT = f"{BASE_DIR}/base_prompt.txt"
    BIOMARKER_INSTRUCTIONS = f"{BASE_DIR}/biomarker_instructions.txt"
    FOUR_PILLARS_INSTRUCTIONS = f"{BASE_DIR}/four_pillars_instructions.txt"
    SUPPLEMENTS_INSTRUCTIONS = f"{BASE_DIR}/supplements_instructions.txt"
    MONTHLY_REPORT_INSTRUCTIONS = f"{BASE_DIR}/monthly_report_instructions.txt"

    # JSON Schemas
    BIOMARKER_SCHEMA = f"{SCHEMAS_DIR}/biomarkers.json"
    FOUR_PILLARS_SCHEMA = f"{SCHEMAS_DIR}/four_pillars.json"
    SUPPLEMENTS_SCHEMA = f"{SCHEMAS_DIR}/supplements.json"
    MONTHLY_REPORT_SCHEMA = f"{SCHEMAS_DIR}/monthly_report.json"


# ==========================================
# Validation Configuration
# ==========================================

class ValidationConfig:
    """Configuration for JSON validation."""

    # Schema validation settings
    VALIDATE_SCHEMAS = True
    STRICT_VALIDATION = True

    # Error messages
    EMPTY_RESPONSE_ERROR = "Model returned an empty response."
    JSON_DECODE_ERROR = "Failed to get valid JSON after {max_retries} attempts"
    VALIDATION_ERROR = "JSON validation failed"


# ==========================================
# Export All Configs
# ==========================================

__all__ = [
    'AIConfig',
    'FileConfig',
    'SafetyConfig',
    'GCPConfig',
    'UIConfig',
    'AppMetadata',
    'PromptPaths',
    'ValidationConfig'
]
