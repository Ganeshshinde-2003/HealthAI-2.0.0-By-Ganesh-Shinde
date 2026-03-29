"""
HealthAI Utilities Package

This package contains shared utility modules for the HealthAI application.
"""

from .file_processor import extract_text_from_file
from .ai_client import HealthAIClient
from .validators import clean_json_string, validate_json, validate_biomarker_count
from .prompt_loader import (
    load_prompt_template,
    load_json_schema,
    build_biomarker_prompt,
    build_four_pillars_prompt,
    build_supplements_prompt,
    build_monthly_report_prompt
)
from .display import display_analysis_results, display_monthly_report
from .storage import HealthAIStorage
from .chat_agent import HealthChatAgent
from .chat_ui import render_chat_interface

__all__ = [
    'extract_text_from_file',
    'HealthAIClient',
    'clean_json_string',
    'validate_json',
    'validate_biomarker_count',
    'load_prompt_template',
    'load_json_schema',
    'build_biomarker_prompt',
    'build_four_pillars_prompt',
    'build_supplements_prompt',
    'build_monthly_report_prompt',
    'display_analysis_results',
    'display_monthly_report',
    'HealthAIStorage',
    'HealthChatAgent',
    'render_chat_interface'
]

__version__ = '1.0.0'
