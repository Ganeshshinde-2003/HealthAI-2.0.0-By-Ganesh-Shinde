"""
HealthAI Storage Module

LocalStorage integration using streamlit-local-storage library.
Provides seamless browser localStorage integration for persistent user data.

Version: 2.0.0
Author: Ganesh Shinde
"""

import streamlit as st
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

try:
    from streamlit_local_storage import LocalStorage
except ImportError:
    st.error("Please install streamlit-local-storage: pip install streamlit-local-storage")
    st.stop()


class HealthAIStorage:
    """Manages persistent storage of user data and analyses using streamlit-local-storage."""

    def __init__(self):
        """Initialize storage manager with localStorage bridge."""
        self.storage_key_analyses = "healthai_analyses"
        self.storage_key_user_data = "healthai_user_data"
        self.storage_key_settings = "healthai_settings"

        # Initialize session state first
        if 'storage_initialized' not in st.session_state:
            st.session_state.storage_initialized = False
            st.session_state.stored_analyses = []
            st.session_state.user_data = {}
            st.session_state.storage_counter = 0

        # Initialize LocalStorage with unique key
        self.local_storage = LocalStorage()

    def initialize_storage(self):
        """Initialize storage and load existing data from localStorage."""
        if not st.session_state.storage_initialized:
            # Try to load data from localStorage automatically
            # Note: This may not work on first page load due to Streamlit's execution model
            self.load_from_local_storage()
            st.session_state.storage_initialized = True

    def manual_load_from_storage(self) -> bool:
        """
        Manually trigger loading from localStorage.
        Call this from a button click to ensure data loads.

        Returns:
            bool: True if data was loaded successfully
        """
        return self.load_from_local_storage()

    def load_from_local_storage(self) -> bool:
        """
        Load data from browser localStorage into session state.

        Returns:
            bool: True if data was loaded successfully
        """
        try:
            # Get data from localStorage
            analyses_json = self.local_storage.getItem(self.storage_key_analyses)

            if analyses_json:
                # Parse JSON string
                analyses = json.loads(analyses_json)

                if isinstance(analyses, list) and len(analyses) > 0:
                    st.session_state.stored_analyses = analyses
                    return True

            return False

        except Exception as e:
            # Silent fail - no data in localStorage is not an error
            return False

    def save_analysis_result(
        self,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        analysis_type: str = "standard"
    ) -> bool:
        """
        Save complete analysis (input + output) to session state and localStorage.

        Args:
            input_data: Dictionary containing input files/text
            output_data: Dictionary containing analysis results
            analysis_type: Type of analysis ("standard" or "monthly")

        Returns:
            bool: True if saved successfully
        """
        try:
            # Create analysis record
            analysis_record = {
                "analysis_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "type": analysis_type,
                "input_data": input_data,
                "output_data": output_data
            }

            # Add to session state (insert at beginning)
            st.session_state.stored_analyses.insert(0, analysis_record)

            # Keep only last 10 analyses
            if len(st.session_state.stored_analyses) > 10:
                st.session_state.stored_analyses = st.session_state.stored_analyses[:10]

            # Save to localStorage
            self._save_to_local_storage()

            return True

        except Exception as e:
            st.error(f"Error saving analysis: {e}")
            return False

    def _save_to_local_storage(self) -> bool:
        """
        Save session state data to browser localStorage.

        Returns:
            bool: True if saved successfully
        """
        try:
            # Convert to JSON string
            analyses_json = json.dumps(st.session_state.stored_analyses)

            # Increment counter for unique keys
            st.session_state.storage_counter += 1
            counter = st.session_state.storage_counter

            # Save to localStorage
            # Note: Each setItem creates its own component, so we need unique keys
            self.local_storage.setItem(
                self.storage_key_analyses,
                analyses_json,
                key=f"save_analyses_{counter}"
            )

            # Save metadata with unique component keys
            self.local_storage.setItem(
                'healthai_has_data',
                'true',
                key=f"save_has_data_{counter}"
            )

            self.local_storage.setItem(
                'healthai_last_save',
                datetime.now().isoformat(),
                key=f"save_last_save_{counter}"
            )

            return True

        except Exception as e:
            st.error(f"Error saving to localStorage: {e}")
            return False

    def get_latest_analysis(self, analysis_type: Optional[str] = None) -> Optional[Dict]:
        """
        Retrieve the most recent analysis from session state.

        Args:
            analysis_type: Filter by type ("standard" or "monthly"), None for any

        Returns:
            Dict containing analysis data or None
        """
        try:
            analyses = st.session_state.stored_analyses

            if not analyses:
                return None

            if analysis_type:
                filtered = [a for a in analyses if a.get("type") == analysis_type]
                return filtered[0] if filtered else None

            return analyses[0]

        except Exception as e:
            return None

    def get_all_analyses(self, analysis_type: Optional[str] = None) -> List[Dict]:
        """
        Retrieve all stored analyses.

        Args:
            analysis_type: Filter by type, None for all

        Returns:
            List of analysis dictionaries
        """
        try:
            analyses = st.session_state.stored_analyses

            if not analyses:
                return []

            if analysis_type:
                return [a for a in analyses if a.get("type") == analysis_type]

            return analyses

        except Exception as e:
            return []

    def check_storage_exists(self) -> bool:
        """
        Check if any analyses exist in session state.

        Returns:
            bool: True if data exists
        """
        return len(st.session_state.stored_analyses) > 0

    def clear_storage(self) -> bool:
        """
        Clear all stored data from session state and localStorage.

        Returns:
            bool: True if cleared successfully
        """
        try:
            # Clear session state
            st.session_state.stored_analyses = []
            st.session_state.user_data = {}

            # Increment counter for unique key
            st.session_state.storage_counter += 1
            counter = st.session_state.storage_counter

            # Clear localStorage with unique key
            self.local_storage.deleteAll(key=f"clear_all_{counter}")

            return True

        except Exception as e:
            st.error(f"Error clearing storage: {e}")
            return False

    def export_all_data(self) -> str:
        """
        Export all stored data as JSON string.

        Returns:
            str: JSON string of all data
        """
        try:
            export_data = {
                "export_date": datetime.now().isoformat(),
                "version": "2.0.0",
                "analyses": st.session_state.stored_analyses,
                "user_data": st.session_state.user_data
            }

            return json.dumps(export_data, indent=2)

        except Exception as e:
            st.error(f"Error exporting data: {e}")
            return "{}"

    def import_data(self, json_string: str) -> bool:
        """
        Import data from JSON string.

        Args:
            json_string: JSON string containing exported data

        Returns:
            bool: True if import successful
        """
        try:
            data = json.loads(json_string)

            # Validate structure
            if "analyses" in data:
                st.session_state.stored_analyses = data["analyses"]

            if "user_data" in data:
                st.session_state.user_data = data["user_data"]

            # Save to localStorage
            self._save_to_local_storage()

            return True

        except Exception as e:
            st.error(f"Error importing data: {e}")
            return False

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about stored data.

        Returns:
            Dict with storage statistics
        """
        analyses = st.session_state.stored_analyses

        standard_count = len([a for a in analyses if a.get("type") == "standard"])
        monthly_count = len([a for a in analyses if a.get("type") == "monthly"])

        latest = analyses[0] if analyses else None
        latest_date = latest["timestamp"] if latest else None

        return {
            "total_analyses": len(analyses),
            "standard_analyses": standard_count,
            "monthly_analyses": monthly_count,
            "latest_analysis_date": latest_date,
            "storage_initialized": st.session_state.storage_initialized
        }

    def generate_data_hash(self, text: str) -> str:
        """
        Generate SHA256 hash of input text for comparison.

        Args:
            text: Input text to hash

        Returns:
            str: Hexadecimal hash string
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
