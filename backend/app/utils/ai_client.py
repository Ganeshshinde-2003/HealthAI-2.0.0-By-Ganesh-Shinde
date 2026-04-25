"""
Vertex AI Client for HealthAI Backend
Handles all interactions with Google Vertex AI and Gemini models.
"""

import json
import time
import os
import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
from google.oauth2 import service_account
from typing import Tuple, Optional
from config.config import AIConfig, SafetyConfig, ValidationConfig
from .validators import clean_json_string, validate_json


class HealthAIClient:
    """
    Client for interacting with Google Vertex AI Gemini models.

    This class handles:
    - Vertex AI initialization
    - Model instantiation
    - Content generation with retry logic
    - Error handling and validation
    """

    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None,
                 credentials_path: Optional[str] = None,
                 max_output_tokens: int = AIConfig.MAX_OUTPUT_TOKENS_STANDARD):
        """
        Initialize the HealthAI client.

        Args:
            project_id: Google Cloud project ID (from env if None)
            location: GCP region (defaults to us-central1)
            credentials_path: Path to service account JSON (from env if None)
            max_output_tokens: Maximum tokens for model output

        Raises:
            Exception: If Vertex AI initialization fails
        """
        # Read from environment variables (matching secrets.toml format)
        self.project_id = project_id or os.environ.get('PROJECT_ID') or os.environ.get('GCP_PROJECT_ID')
        self.location = location or os.environ.get('LOCATION') or os.environ.get('GCP_LOCATION', 'us-central1')
        self.max_output_tokens = max_output_tokens

        if not self.project_id:
            raise ValueError("PROJECT_ID must be set in environment or passed as parameter")

        # Initialize credentials
        credentials = None

        # Try to load credentials from JSON string (like secrets.toml)
        google_credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if google_credentials_json:
            try:
                credentials_dict = json.loads(google_credentials_json)
                credentials = service_account.Credentials.from_service_account_info(credentials_dict)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse GOOGLE_CREDENTIALS_JSON: {e}")

        # Fallback to file path if JSON string not available
        if not credentials:
            if credentials_path:
                credentials = service_account.Credentials.from_service_account_file(credentials_path)
            else:
                creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
                if creds_path and os.path.exists(creds_path):
                    credentials = service_account.Credentials.from_service_account_file(creds_path)

        # Initialize Vertex AI
        try:
            vertexai.init(project=self.project_id, location=self.location, credentials=credentials)
            print(f"✅ HealthAI initialized successfully for project: {self.project_id}")
        except Exception as e:
            print(f"❌ Failed to initialize HealthAI: {e}")
            raise

        # Configure model
        self.model = self._create_model()

    def _create_model(self) -> GenerativeModel:
        """Create and configure the Gemini model."""
        generation_config = {
            "temperature": AIConfig.TEMPERATURE,
            "top_p": AIConfig.TOP_P,
            "top_k": AIConfig.TOP_K,
            "max_output_tokens": self.max_output_tokens,
            "response_mime_type": AIConfig.RESPONSE_MIME_TYPE
        }

        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        return GenerativeModel(
            AIConfig.MODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    def generate_content(self, prompt: str, schema: Optional[dict] = None,
                        max_retries: int = AIConfig.MAX_RETRIES) -> Tuple[dict, str]:
        """
        Generate content using the Gemini model with retry logic.

        Args:
            prompt: The prompt to send to the model
            schema: Optional JSON schema for validation
            max_retries: Maximum number of retry attempts

        Returns:
            Tuple[dict, str]: (parsed_data, raw_response)
                - parsed_data: Dictionary containing the parsed JSON response
                - raw_response: Raw string response from the model

        Raises:
            Exception: If all retry attempts fail or validation fails
        """
        raw_response_for_debugging = ""

        for attempt in range(max_retries):
            if attempt > 0:
                print(f"Retry attempt {attempt + 1}...")
                time.sleep(AIConfig.RETRY_DELAY_SECONDS)

            try:
                # Call the model
                response = self.model.generate_content(prompt)
                full_response_text = response.text
                raw_response_for_debugging = full_response_text

                if not full_response_text:
                    raise ValueError(ValidationConfig.EMPTY_RESPONSE_ERROR)

                # Clean and parse JSON
                cleaned_json_string = clean_json_string(full_response_text)
                data = json.loads(cleaned_json_string)

                # Validate against schema if provided
                if schema and ValidationConfig.VALIDATE_SCHEMAS:
                    is_valid, err_msg = validate_json(data, schema)
                    if is_valid:
                        return data, raw_response_for_debugging
                    else:
                        print(f"Validation warning: {err_msg}")
                        if attempt == max_retries - 1:
                            # Last attempt, return anyway
                            return data, raw_response_for_debugging
                else:
                    # No schema validation, return parsed data
                    return data, raw_response_for_debugging

            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed (Invalid JSON). Retrying...")
                    time.sleep(AIConfig.RETRY_DELAY_SECONDS)
                else:
                    error_msg = f"{ValidationConfig.JSON_DECODE_ERROR.format(max_retries=max_retries)}: {e}"
                    print(f"Error: {error_msg}")
                    print(f"Raw response: {raw_response_for_debugging[:500]}...")
                    raise Exception(error_msg)

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed (Error: {e}). Retrying...")
                    time.sleep(AIConfig.RETRY_DELAY_SECONDS)
                else:
                    error_msg = f"Error after {max_retries} attempts: {e}"
                    print(f"Error: {error_msg}")
                    raise Exception(error_msg)

        raise Exception("Max retries reached without a successful response.")


def initialize_vertex_ai() -> HealthAIClient:
    """
    Initialize Vertex AI client from environment variables.

    This is a convenience function for backwards compatibility.

    Returns:
        HealthAIClient: Initialized client instance
    """
    return HealthAIClient()
