"""
HealthAI - Standard Health Analyzer (Refactored)

This is the refactored version using the new modular structure.
Clean, maintainable, and follows best practices.

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
    build_biomarker_prompt,
    build_four_pillars_prompt,
    build_supplements_prompt,
    load_json_schema,
    display_analysis_results
)


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title=UIConfig.PAGE_TITLE_ANALYZER,
    page_icon=UIConfig.PAGE_ICON_ANALYZER,
    layout=UIConfig.LAYOUT
)


# ==========================================
# Initialize AI Client
# ==========================================

# Initialize HealthAI client (handles credentials automatically)
try:
    ai_client = HealthAIClient()
except Exception as e:
    st.error(f"Failed to initialize AI client: {e}")
    st.stop()


# ==========================================
# Load JSON Schemas
# ==========================================

schema_biomarkers = load_json_schema('biomarkers.json')
schema_4pillars = load_json_schema('four_pillars.json')
schema_supplements = load_json_schema('supplements.json')


# ==========================================
# Main Application
# ==========================================

def main():
    """Main application function."""

    # Display header
    st.title(UIConfig.HEADER_MAIN_ANALYZER)
    st.write("Upload your health data for personalized AI-powered analysis.")

    # ====================
    # Upload Guide & Examples (Expandable)
    # ====================
    with st.expander("📚 **Upload Guide & Examples** - Click here to see what to upload!", expanded=False):
        guide_tab1, guide_tab2 = st.tabs(["🔬 Lab Reports", "📝 Health Data"])

        with guide_tab1:
            st.markdown("""
            ### What Lab Reports to Upload

            **We analyze 50+ biomarkers including:**
            - 🩸 **Hormones:** Estradiol, Progesterone, Testosterone, DHEA-S, Cortisol, LH, FSH
            - 🦴 **Thyroid:** TSH, Free T3, Free T4, Thyroid Antibodies
            - 💊 **Vitamins:** Vitamin D, B12, Folate, Iron, Ferritin
            - 🩺 **Metabolic:** Glucose, HbA1c, Insulin, Lipid Panel
            - 🔥 **Inflammatory:** CRP, ESR

            **Example Lab Report Format:**
            ```
            TSH                 4.310 uIU/mL    (Ref: 0.450-4.500)
            Estradiol           85 pg/mL        (Ref: 12-166)
            Vitamin D (25-OH)   28 ng/mL        (Ref: 30-100) **LOW**
            ```

            **Accepted Formats:** PDF, Word, Excel, CSV, Plain Text (Max 10MB per file)
            """)

        with guide_tab2:
            st.markdown("""
            ### What Health Data to Include (Optional)

            **💡 The more context you provide, the better your recommendations!**

            **Include any of these:**
            - ✅ Current symptoms (fatigue, mood, sleep, digestion)
            - ✅ Health goals you want to achieve
            - ✅ Current medications & supplements
            - ✅ Menstrual cycle information
            - ✅ Lifestyle (diet, exercise, stress, sleep)
            - ✅ Medical history & family history
            - ✅ Specific concerns or questions

            **Example Health Data:**
            ```
            SYMPTOMS: Constant fatigue, brain fog, difficulty sleeping
            GOALS: Improve energy levels, better sleep quality
            LIFESTYLE: Skip breakfast, coffee 3x/day, gym 3x/week
            MEDICATIONS: Multivitamin, Vitamin D 2000IU, Magnesium 200mg
            CYCLE INFO (if applicable): 28-day cycle, currently day 13
            QUESTIONS: Could thyroid or vitamin deficiency be causing fatigue?
            ```

            **Format:** Any text document, Word, or PDF with your health information
            """)

    st.markdown("---")

    # File upload section
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
        st.info("📋 Please upload at least one lab report to begin your personalized health analysis.")
        st.stop()

    # Analysis button
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

        # Analysis status
        with st.status(UIConfig.ANALYSIS_INITIATING, expanded=True) as status_message_box:
            status_message_box.write("⚙️ Preparing data for analysis...")

            # ====================
            # Part 1: Biomarkers
            # ====================
            status_message_box.write("🔬 Analyzing Biomarkers...")
            biomarker_prompt = build_biomarker_prompt(
                raw_health_assessment_input,
                lab_report_section_formatted
            )

            try:
                biomarker_data_raw, _ = ai_client.generate_content(
                    biomarker_prompt,
                    schema_biomarkers
                )
                if biomarker_data_raw:
                    final_combined_output.update(biomarker_data_raw)
                status_message_box.write("✅ Biomarker analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze biomarkers: {e}")

            # ====================
            # Part 2: Four Pillars
            # ====================
            status_message_box.write("💪 Moving to Four Pillars (Eat, Sleep, Move, Recover) analysis...")
            four_pillars_prompt = build_four_pillars_prompt(
                raw_health_assessment_input,
                lab_report_section_formatted
            )

            try:
                four_pillars_data_raw, _ = ai_client.generate_content(
                    four_pillars_prompt,
                    schema_4pillars
                )
                if four_pillars_data_raw:
                    final_combined_output.update(four_pillars_data_raw)
                status_message_box.write("✅ Four Pillars analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze four pillars: {e}")

            # ====================
            # Part 3: Supplements
            # ====================
            status_message_box.write("💊 Moving to Supplements analysis...")
            supplements_prompt = build_supplements_prompt(
                raw_health_assessment_input,
                lab_report_section_formatted
            )

            try:
                supplements_data_raw, _ = ai_client.generate_content(
                    supplements_prompt,
                    schema_supplements
                )
                if supplements_data_raw:
                    final_combined_output.update(supplements_data_raw)
                status_message_box.write("✅ Supplements analysis complete.")
            except Exception as e:
                status_message_box.error(f"Failed to analyze supplements and action items: {e}")

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

                # Beautiful visual display
                display_analysis_results(final_combined_output)

                st.markdown("---")

                # Download buttons
                st.subheader("📥 Download Your Report")
                col1, col2 = st.columns(2)

                with col1:
                    # JSON Download
                    plain_json_string = json.dumps(final_combined_output, indent=2)
                    st.download_button(
                        label="📄 Download JSON",
                        data=plain_json_string,
                        file_name="healthai_analysis.json",
                        mime="application/json",
                        help="Download your analysis as a JSON file for your records or to use with other tools."
                    )

                with col2:
                    # PDF Download (placeholder for now)
                    st.button(
                        "📑 Download PDF Report",
                        disabled=True,
                        help="PDF generation coming soon! For now, you can print this page as PDF using your browser (Ctrl/Cmd + P)."
                    )

                st.info("💡 **Tip**: Use your browser's Print function (Ctrl/Cmd + P) to save this page as PDF for now.", icon="ℹ️")

                # Expandable JSON section for developers
                with st.expander("🔍 View Raw JSON Data (for developers)", expanded=False):
                    st.json(final_combined_output, expanded=True)
                    st.markdown("**Copy JSON Text:**")
                    st.text_area(
                        "Select and copy:",
                        plain_json_string,
                        height=300,
                        disabled=True,
                        label_visibility="collapsed"
                    )
            else:
                status_message_box.error("❌ No analysis data could be generated. Please check the inputs and ensure HealthAI is correctly configured.")


if __name__ == "__main__":
    main()
