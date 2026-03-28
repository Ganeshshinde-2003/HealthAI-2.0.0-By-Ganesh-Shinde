"""
Vertex AI Client for HealthAI

Handles all interactions with Google Vertex AI and Gemini models.
"""

import json
import time
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
from google.oauth2 import service_account
from typing import Tuple, Optional

from config import AIConfig, SafetyConfig, GCPConfig, ValidationConfig
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
                 credentials: Optional[service_account.Credentials] = None,
                 max_output_tokens: int = AIConfig.MAX_OUTPUT_TOKENS_STANDARD):
        """
        Initialize the HealthAI client.

        Args:
            project_id: Google Cloud project ID (from Streamlit secrets if None)
            location: GCP region (defaults to us-central1)
            credentials: Service account credentials (from Streamlit secrets if None)
            max_output_tokens: Maximum tokens for model output

        Raises:
            Exception: If Vertex AI initialization fails
        """
        self.project_id = project_id or st.secrets.get("PROJECT_ID")
        self.location = location or st.secrets.get("LOCATION", GCPConfig.DEFAULT_LOCATION)
        self.max_output_tokens = max_output_tokens

        # Initialize credentials
        if credentials is None:
            credentials = self._load_credentials_from_secrets()

        # Initialize Vertex AI
        try:
            vertexai.init(project=self.project_id, location=self.location, credentials=credentials)
            st.success("✅ HealthAI initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize HealthAI. Please check your configuration.\n\nError: {e}")
            raise

        # Configure model
        self.model = self._create_model()

    def _load_credentials_from_secrets(self) -> service_account.Credentials:
        """Load Google Cloud credentials from Streamlit secrets."""
        credentials_json_string = st.secrets.get("google_credentials")

        if not credentials_json_string:
            st.error("Google Cloud credentials not found in Streamlit secrets. Please configure 'google_credentials'.")
            st.stop()

        credentials_dict = json.loads(credentials_json_string)
        return service_account.Credentials.from_service_account_info(credentials_dict)

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

        Example:
            >>> client = HealthAIClient()
            >>> data, raw = client.generate_content("Analyze this...", schema)
        """
        raw_response_for_debugging = ""

        for attempt in range(max_retries):
            if attempt > 0:
                st.info(f"Attempt {attempt + 1} is ongoing...")
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
                        st.warning(f"{ValidationConfig.VALIDATION_ERROR}: {err_msg}")
                else:
                    # No schema validation, return parsed data
                    return data, raw_response_for_debugging

            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed (Invalid JSON). Retrying...")
                    time.sleep(AIConfig.RETRY_DELAY_SECONDS)
                else:
                    st.error(f"Attempt {attempt + 1} failed. {ValidationConfig.JSON_DECODE_ERROR.format(max_retries=max_retries)}: {e}")
                    st.code(raw_response_for_debugging, language='json')
                    raise Exception(f"{ValidationConfig.JSON_DECODE_ERROR.format(max_retries=max_retries)}: {e}")

            except Exception as e:
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed (Unexpected error: {e}). Retrying...")
                    time.sleep(AIConfig.RETRY_DELAY_SECONDS)
                else:
                    st.error(f"Attempt {attempt + 1} failed. An unexpected error occurred after {max_retries} attempts: {e}")
                    raise

        raise Exception("Max retries reached without a successful response.")


def initialize_vertex_ai() -> HealthAIClient:
    """
    Initialize Vertex AI client from Streamlit secrets.

    This is a convenience function for backwards compatibility.

    Returns:
        HealthAIClient: Initialized client instance

    Example:
        >>> client = initialize_vertex_ai()
        >>> data, raw = client.generate_content(prompt, schema)
    """
    return HealthAIClient()
