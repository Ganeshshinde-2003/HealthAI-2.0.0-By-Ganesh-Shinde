"""
JSON Validation Utilities for HealthAI

Handles JSON cleaning and schema validation.
"""

import re
import json
import jsonschema
from typing import Tuple


def clean_json_string(json_string: str) -> str:
    """
    Removes markdown code blocks and fixes common JSON errors.

    Args:
        json_string: Raw JSON string potentially containing markdown or errors

    Returns:
        str: Cleaned JSON string

    Fixes Applied:
        - Removes markdown code blocks (```json and ```)
        - Removes illegal trailing commas
        - Strips leading/trailing whitespace
    """
    if not isinstance(json_string, str):
        return json_string

    stripped_string = json_string.strip()

    # Remove markdown code blocks
    if stripped_string.startswith('```json'):
        stripped_string = stripped_string[len('```json'):].lstrip()
    elif stripped_string.startswith('```'):
        stripped_string = stripped_string[len('```'):].lstrip()

    if stripped_string.endswith('```'):
        stripped_string = stripped_string[:-len('```')].rstrip()

    # Alternative regex approach for code blocks
    stripped_string = re.sub(r'^```json\s*|```\s*$', '', stripped_string, flags=re.MULTILINE)

    # Remove trailing commas within JSON objects and arrays
    stripped_string = re.sub(r',\s*}', '}', stripped_string)
    stripped_string = re.sub(r',\s*]', ']', stripped_string)

    return stripped_string


def validate_json(data: dict, schema: dict) -> Tuple[bool, str]:
    """
    Validates JSON data against a JSON schema.

    Args:
        data: Dictionary containing the data to validate
        schema: Dictionary containing the JSON schema

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
            - is_valid: True if validation passed, False otherwise
            - error_message: Error description if validation failed, empty string otherwise

    Example:
        >>> schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        >>> data = {"name": "John"}
        >>> is_valid, error = validate_json(data, schema)
        >>> print(is_valid)
        True
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, e.message
    except Exception as e:
        return False, str(e)


def load_json_schema(schema_path: str) -> dict:
    """
    Loads a JSON schema from a file.

    Args:
        schema_path: Path to the JSON schema file

    Returns:
        dict: Parsed JSON schema

    Raises:
        FileNotFoundError: If schema file doesn't exist
        json.JSONDecodeError: If schema file contains invalid JSON
    """
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_biomarker_count(lab_analysis: dict) -> dict:
    """
    Validates and corrects biomarker counts in lab analysis results.

    Args:
        lab_analysis: Dictionary containing lab analysis data

    Returns:
        dict: Corrected lab analysis data

    Side Effects:
        - Updates biomarkers_tested_count to match actual array length
        - Recalculates category counts (optimal, keep_in_mind, attention_needed)
        - Updates description_text with corrected counts
    """
    if not lab_analysis or "detailed_biomarkers" not in lab_analysis:
        return lab_analysis

    detailed_biomarkers = lab_analysis.get("detailed_biomarkers", [])
    biomarkers_count = len(detailed_biomarkers)

    # Only correct if there's a mismatch
    if lab_analysis.get("biomarkers_tested_count") != biomarkers_count:
        if lab_analysis.get("biomarkers_tested_count") is None or biomarkers_count > 0:
            lab_analysis["biomarkers_tested_count"] = biomarkers_count

            # Recalculate summary counts
            optimal = sum(1 for bm in detailed_biomarkers if bm.get("status") == "optimal")
            keep_in_mind = sum(1 for bm in detailed_biomarkers if bm.get("status") == "keep_in_mind")
            attention = sum(1 for bm in detailed_biomarkers if bm.get("status") == "attention_needed")

            if "biomarker_categories_summary" in lab_analysis:
                lab_analysis["biomarker_categories_summary"]["optimal_count"] = optimal
                lab_analysis["biomarker_categories_summary"]["keep_in_mind_count"] = keep_in_mind
                lab_analysis["biomarker_categories_summary"]["attention_needed_count"] = attention
                lab_analysis["biomarker_categories_summary"]["description_text"] = (
                    f"Out of your total {biomarkers_count} biomarker tests, "
                    f"{optimal} fall within optimal ranges, showing strong health markers. "
                    f"{keep_in_mind} need attention and monitoring to support your well-being. "
                    f"{attention} require urgent action to address potential health concerns. "
                    "This summary prioritizes your key health focus areas clearly."
                )

    return lab_analysis
