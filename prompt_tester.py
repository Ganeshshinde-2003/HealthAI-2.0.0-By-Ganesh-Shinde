"""
HealthAI - Prompt Testing Tool

Interactive prompt editor for testing and optimizing AI prompts.
Allows real-time modification of prompts during analysis.

Version: 2.0.0 (Refactored)
Author: Ganesh Shinde
"""

import streamlit as st
import json

# Import configuration
from config import UIConfig, AppMetadata

# Import utilities
from utils import (
    extract_text_from_file,
    HealthAIClient,
    validate_biomarker_count,
    load_prompt_template,
    load_json_schema
)


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title=UIConfig.PAGE_TITLE_ANALYZER_TEST,
    page_icon=UIConfig.PAGE_ICON_ANALYZER,
    layout=UIConfig.LAYOUT
)


# ==========================================
# Initialize AI Client
# ==========================================

try:
    ai_client = HealthAIClient()
except Exception as e:
    st.error(f"Failed to initialize AI client: {e}")
    st.stop()


# ==========================================
# Load Templates and Schemas
# ==========================================

# Load prompt templates
base_prompt_template = load_prompt_template('base_prompt.txt')
biomarker_instructions_template = load_prompt_template('biomarker_instructions.txt')
pillars_instructions_template = load_prompt_template('four_pillars_instructions.txt')
supplements_instructions_template = load_prompt_template('supplements_instructions.txt')

# Load schemas
schema_biomarkers = load_json_schema('biomarkers.json')
schema_4pillars = load_json_schema('four_pillars.json')
schema_supplements = load_json_schema('supplements.json')


# ==========================================
# Helper Functions
# ==========================================

def escape_braces(s):
    """Escape braces for safe formatting."""
    return s.replace("{", "{{").replace("}", "}}")


def build_prompt_from_editor(base_prompt, specific_instructions, schema_json):
    """Build complete prompt from edited components."""
    schema_str = json.dumps(schema_json, indent=2)
    return f"{base_prompt}\n\n{specific_instructions}\n\n{escape_braces(schema_str)}"


# ==========================================
# Main Application
# ==========================================

def main():
    """Main application function."""

    st.title(UIConfig.HEADER_MAIN_ANALYZER_TEST)
    st.write("Upload your lab report(s) and health assessment files for a personalized analysis.")
    st.info("💡 This version allows you to edit prompts in real-time for testing and optimization.")

    # ====================
    # Upload Guide (Expandable)
    # ====================
    with st.expander("📚 **Upload Guide & Examples** - Click for instructions", expanded=False):
        st.markdown("""
        ### 🔬 Lab Reports

        Upload blood test results with biomarkers like:
        - Hormones, Thyroid, Vitamins, Metabolic markers

        ### 📝 Health Data

        Include: symptoms, goals, lifestyle, medications, cycle info

        *See main app.py for detailed examples!*
        """)

    st.markdown("---")

    # ====================
    # Editable Prompts
    # ====================
    st.subheader("🔧 Prompt Editor")

    with st.expander("Edit Base Prompt (Common instructions)", expanded=False):
        edited_base_prompt = st.text_area(
            "Base Prompt",
            value=base_prompt_template,
            height=300,
            key="edited_base_prompt"
        )

    with st.expander("Edit Biomarker Instructions", expanded=False):
        edited_biomarker_instructions = st.text_area(
            "Biomarker-specific Instructions",
            value=biomarker_instructions_template,
            height=200,
            key="edited_biomarker_instructions"
        )

    with st.expander("Edit Four Pillars Instructions", expanded=False):
        edited_pillars_instructions = st.text_area(
            "Four Pillars-specific Instructions",
            value=pillars_instructions_template,
            height=200,
            key="edited_pillars_instructions"
        )

    with st.expander("Edit Supplements Instructions", expanded=False):
        edited_supplements_instructions = st.text_area(
            "Supplements-specific Instructions",
            value=supplements_instructions_template,
            height=200,
            key="edited_supplements_instructions"
        )

    # ====================
    # File Upload
    # ====================
    st.subheader("📁 Upload Files")

    col1, col2 = st.columns(2)
    with col1:
        lab_report_files = st.file_uploader(
            "📋 Upload Lab Report(s) (required)",
            type=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"],
            accept_multiple_files=True,
            help="Upload your blood test results, hormone panels, or any medical lab reports. We analyze 50+ biomarkers including thyroid, hormones, vitamins, and metabolic markers. Accepted formats: PDF, Word, Excel, CSV, or plain text."
        )
    with col2:
        health_assessment_file = st.file_uploader(
            "📝 Upload Health Data (optional)",
            type=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"],
            help="Upload any health information like: symptoms you're experiencing, health goals, medical history, current medications, lifestyle habits, or concerns. This can be a document you created, doctor's notes, or any text file with your health information."
        )

    # Validation
    if not lab_report_files:
        st.info("📋 Please upload at least one lab report to begin testing prompts.")
        st.stop()

    # ====================
    # Analysis Button
    # ====================
    if st.button(UIConfig.BUTTON_ANALYZE, type="primary"):
        # Process lab reports
        raw_lab_report_inputs = []
        if lab_report_files:
            for file in lab_report_files:
                extracted_text = extract_text_from_file(file)
                if "[Error" in extracted_text or "[Unsupported" in extracted_text:
                    st.warning(f"Problem with Lab Report '{file.name}': {extracted_text}")
                else:
                    raw_lab_report_inputs.append(
                        f"--- Start Lab Report: {file.name} ---\n{extracted_text}\n--- End Lab Report: {file.name} ---"
                    )
        combined_lab_report_text = "\n\n".join(raw_lab_report_inputs)

        # Process health assessment (optional)
        raw_health_assessment_input = ""
        if health_assessment_file:
            raw_health_assessment_input = extract_text_from_file(health_assessment_file)
            if "[Error" in raw_health_assessment_input:
                st.warning(f"Problem processing Health Data: {raw_health_assessment_input}")
                st.write("Continuing analysis with lab reports only.")
                raw_health_assessment_input = ""

        # If no health assessment provided, use placeholder
        if not raw_health_assessment_input:
            raw_health_assessment_input = "No additional health information provided. Analysis based on lab reports only."

        # Format lab report section
        lab_report_section_formatted = f"""
Here is the user's Lab Report text (potentially multiple reports combined):
{combined_lab_report_text}
"""

        # Initialize output
        final_combined_output = {}
        all_raw_responses_for_debugging = {}
        full_prompts_for_debugging = {}

        # Analysis status
        with st.status(UIConfig.ANALYSIS_INITIATING, expanded=True) as status_message_box:
            status_message_box.write("⚙️ Preparing data for analysis...")

            # Get edited prompts
            base_prompt = st.session_state.get("edited_base_prompt", base_prompt_template)
            biomarker_instructions = st.session_state.get("edited_biomarker_instructions", biomarker_instructions_template)
            pillars_instructions = st.session_state.get("edited_pillars_instructions", pillars_instructions_template)
            supplements_instructions = st.session_state.get("edited_supplements_instructions", supplements_instructions_template)

            # ====================
            # Part 1: Biomarkers
            # ====================
            status_message_box.write("🔬 Analyzing Biomarkers...")

            formatted_base = base_prompt.format(
                health_assessment_text=raw_health_assessment_input,
                lab_report_section_placeholder=lab_report_section_formatted
            )
            biomarker_prompt = build_prompt_from_editor(
                formatted_base,
                biomarker_instructions,
                schema_biomarkers
            )
            full_prompts_for_debugging["Biomarkers Analysis Prompt"] = biomarker_prompt

            try:
                biomarker_data_raw, raw_biomarker_response = ai_client.generate_content(
                    biomarker_prompt,
                    schema_biomarkers
                )
                if biomarker_data_raw:
                    final_combined_output.update(biomarker_data_raw)
                all_raw_responses_for_debugging["Biomarkers Raw Response"] = raw_biomarker_response
                status_message_box.write("✅ Biomarker analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze biomarkers: {e}")

            # ====================
            # Part 2: Four Pillars
            # ====================
            status_message_box.write("💪 Moving to Four Pillars analysis...")

            pillars_prompt = build_prompt_from_editor(
                formatted_base,
                pillars_instructions,
                schema_4pillars
            )
            full_prompts_for_debugging["Four Pillars Analysis Prompt"] = pillars_prompt

            try:
                four_pillars_data_raw, raw_four_pillars_response = ai_client.generate_content(
                    pillars_prompt,
                    schema_4pillars
                )
                if four_pillars_data_raw:
                    final_combined_output.update(four_pillars_data_raw)
                all_raw_responses_for_debugging["Four Pillars Raw Response"] = raw_four_pillars_response
                status_message_box.write("✅ Four Pillars analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze four pillars: {e}")

            # ====================
            # Part 3: Supplements
            # ====================
            status_message_box.write("💊 Moving to Supplements analysis...")

            supplements_prompt = build_prompt_from_editor(
                formatted_base,
                supplements_instructions,
                schema_supplements
            )
            full_prompts_for_debugging["Supplements Analysis Prompt"] = supplements_prompt

            try:
                supplements_data_raw, raw_supplements_response = ai_client.generate_content(
                    supplements_prompt,
                    schema_supplements
                )
                if supplements_data_raw:
                    final_combined_output.update(supplements_data_raw)
                all_raw_responses_for_debugging["Supplements Raw Response"] = raw_supplements_response
                status_message_box.write("✅ Supplements analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze supplements: {e}")

            # ====================
            # Post-Processing
            # ====================
            status_message_box.write("✨ Finalizing analysis and preparing report...")

            # Validate and correct biomarker counts
            if "lab_analysis" in final_combined_output and final_combined_output["lab_analysis"]:
                final_combined_output["lab_analysis"] = validate_biomarker_count(
                    final_combined_output["lab_analysis"]
                )

            # ====================
            # Display Results
            # ====================
            if any(final_combined_output.values()):
                status_message_box.update(label=UIConfig.ANALYSIS_COMPLETE, state="complete")

                # Interactive JSON display
                st.header(UIConfig.HEADER_RESULTS)
                st.json(final_combined_output, expanded=True)

                # Copyable plain text
                st.markdown("---")
                st.header(UIConfig.HEADER_COPY_JSON)
                plain_json_string = json.dumps(final_combined_output, indent=2)
                st.text_area(
                    "Select the text below and copy it to your clipboard:",
                    plain_json_string,
                    height=400,
                    disabled=True
                )
            else:
                status_message_box.error("❌ No analysis data could be generated.")

        # ====================
        # Debug Information
        # ====================
        with st.expander("Show All Debug Information (Raw Responses & Prompts)"):
            combined_debug_output = []

            combined_debug_output.append("--- START OF RAW MODEL RESPONSES ---\n\n")
            for part_name, response_text in all_raw_responses_for_debugging.items():
                combined_debug_output.append(f"--- {part_name} ---\n")
                combined_debug_output.append(response_text)
                combined_debug_output.append(f"\n--- END OF {part_name} ---\n\n")

            combined_debug_output.append("\n--- START OF FULL PROMPTS SENT TO AI ---\n\n")
            for prompt_name, prompt_text in full_prompts_for_debugging.items():
                combined_debug_output.append(f"--- {prompt_name} ---\n")
                combined_debug_output.append(prompt_text)
                combined_debug_output.append(f"\n--- END OF {prompt_name} ---\n\n")

            st.code("".join(combined_debug_output), language='text')


if __name__ == "__main__":
    main()
