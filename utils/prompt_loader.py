"""
Prompt Loading Utilities for HealthAI

Handles loading of prompt templates and JSON schemas from files.
"""

import json
import os
from typing import Dict


def load_prompt_template(filename: str) -> str:
    """
    Load a prompt template from the prompts directory.

    Args:
        filename: Name of the prompt file (e.g., 'base_prompt.txt')

    Returns:
        str: Contents of the prompt template

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    filepath = os.path.join('prompts', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_json_schema(filename: str) -> Dict:
    """
    Load a JSON schema from the prompts/schemas directory.

    Args:
        filename: Name of the schema file (e.g., 'biomarkers.json')

    Returns:
        Dict: Parsed JSON schema as a dictionary

    Raises:
        FileNotFoundError: If the schema file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    filepath = os.path.join('prompts', 'schemas', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_biomarker_prompt(health_assessment_text: str, lab_report_text: str) -> str:
    """
    Build the complete biomarker analysis prompt.

    Args:
        health_assessment_text: User's health assessment text
        lab_report_text: User's lab report text (formatted)

    Returns:
        str: Complete prompt ready for AI model
    """
    base_prompt = load_prompt_template('base_prompt.txt')
    biomarker_instructions = load_prompt_template('biomarker_instructions.txt')
    biomarker_schema = load_json_schema('biomarkers.json')

    # Format base prompt with user data
    formatted_base = base_prompt.format(
        health_assessment_text=health_assessment_text,
        lab_report_section_placeholder=lab_report_text
    )

    # Combine with specific instructions and schema
    schema_json_str = json.dumps(biomarker_schema, indent=2)
    return f"{formatted_base}\n\n{biomarker_instructions}\n\n{schema_json_str}"


def build_four_pillars_prompt(health_assessment_text: str, lab_report_text: str) -> str:
    """
    Build the complete four pillars analysis prompt.

    Args:
        health_assessment_text: User's health assessment text
        lab_report_text: User's lab report text (formatted)

    Returns:
        str: Complete prompt ready for AI model
    """
    base_prompt = load_prompt_template('base_prompt.txt')
    pillars_instructions = load_prompt_template('four_pillars_instructions.txt')
    pillars_schema = load_json_schema('four_pillars.json')

    formatted_base = base_prompt.format(
        health_assessment_text=health_assessment_text,
        lab_report_section_placeholder=lab_report_text
    )

    schema_json_str = json.dumps(pillars_schema, indent=2)
    return f"{formatted_base}\n\n{pillars_instructions}\n\n{schema_json_str}"


def build_supplements_prompt(health_assessment_text: str, lab_report_text: str) -> str:
    """
    Build the complete supplements analysis prompt.

    Args:
        health_assessment_text: User's health assessment text
        lab_report_text: User's lab report text (formatted)

    Returns:
        str: Complete prompt ready for AI model
    """
    base_prompt = load_prompt_template('base_prompt.txt')
    supplements_instructions = load_prompt_template('supplements_instructions.txt')
    supplements_schema = load_json_schema('supplements.json')

    formatted_base = base_prompt.format(
        health_assessment_text=health_assessment_text,
        lab_report_section_placeholder=lab_report_text
    )

    schema_json_str = json.dumps(supplements_schema, indent=2)
    return f"{formatted_base}\n\n{supplements_instructions}\n\n{schema_json_str}"


def build_monthly_report_prompt(previous_lab_report_data: str, daily_logs_data: str,
                                weekly_assessments_data: str) -> str:
    """
    Build the complete monthly report prompt.

    Args:
        previous_lab_report_data: Previous lab report text (formatted)
        daily_logs_data: Daily logs text (formatted)
        weekly_assessments_data: Weekly assessments text (formatted)

    Returns:
        str: Complete prompt ready for AI model
    """
    monthly_instructions = load_prompt_template('monthly_report_instructions.txt')
    monthly_schema = load_json_schema('monthly_report.json')

    formatted_instructions = monthly_instructions.format(
        previous_lab_report_data=previous_lab_report_data,
        daily_logs_data=daily_logs_data,
        weekly_assessments_data=weekly_assessments_data
    )

    schema_json_str = json.dumps(monthly_schema, indent=2)
    return f"{formatted_instructions}\n\n{schema_json_str}"


__all__ = [
    'load_prompt_template',
    'load_json_schema',
    'build_biomarker_prompt',
    'build_four_pillars_prompt',
    'build_supplements_prompt',
    'build_monthly_report_prompt'
]
