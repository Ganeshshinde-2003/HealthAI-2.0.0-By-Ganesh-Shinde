"""
HealthAI - Standard Health Analyzer (Refactored)

This is the refactored version using the new modular structure.
Clean, maintainable, and follows best practices.

Version: 2.0.0 (Refactored)
Author: Ganesh Shinde
"""

import streamlit as st
import json
from datetime import datetime

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
    display_analysis_results,
    HealthAIStorage,
    render_chat_interface
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
# Initialize AI Client & Storage
# ==========================================

# Initialize HealthAI client (handles credentials automatically)
try:
    ai_client = HealthAIClient()
except Exception as e:
    st.error(f"Failed to initialize AI client: {e}")
    st.stop()

# Initialize Storage (automatically loads from localStorage on first run)
storage = HealthAIStorage()
storage.initialize_storage()


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
    # Manual Load Button (if no data in session)
    # ====================
    if not storage.check_storage_exists():
        st.info("💡 Have previous analysis data? Load it from your browser storage.", icon="ℹ️")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Load Previous Data", type="primary", use_container_width=True, key="manual_load_btn"):
                # Trigger manual load
                if storage.manual_load_from_storage():
                    st.success("✅ Data loaded successfully!")
                    st.rerun()
                else:
                    st.warning("No previous data found in browser storage.")

        st.markdown("---")

    # ====================
    # Storage Info Banner
    # ====================
    if storage.check_storage_exists():
        storage_info = storage.get_storage_info()
        st.info(
            f"💾 **{storage_info['total_analyses']} analysis(es) in memory** | "
            f"Last saved: {storage_info['latest_analysis_date'][:10] if storage_info['latest_analysis_date'] else 'N/A'} | "
            f"View below or export from sidebar →",
            icon="ℹ️"
        )

    # ====================
    # Previous Analysis Section (if exists)
    # ====================
    if storage.check_storage_exists():
        latest_analysis = storage.get_latest_analysis("standard")
        if latest_analysis:
            with st.expander("📂 Previous Analysis Found - Click to view", expanded=False):
                timestamp = latest_analysis.get("timestamp", "Unknown date")
                st.success(f"📅 Last analysis: {timestamp}")

                if st.button("👁️ View Previous Results", use_container_width=True, key="view_prev_btn"):
                    st.session_state.show_previous = True

        st.markdown("---")

        # Display previous results in full width (outside columns)
        if st.session_state.get("show_previous", False):
            st.markdown("---")
            st.subheader("📊 Previously Saved Analysis")

            # Close button
            if st.button("✖️ Close Previous Results", key="close_prev_btn"):
                st.session_state.show_previous = False
                st.rerun()

            display_analysis_results(latest_analysis["output_data"])
            st.info("💡 Upload new files below to generate a fresh analysis.")
            st.markdown("---")

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

    # ====================
    # Sidebar: Data Management
    # ====================
    with st.sidebar:
        st.markdown("### 💾 Data Management")

        # Import data section
        st.markdown("#### 📥 Import Data")
        import_file = st.file_uploader(
            "Upload previous export",
            type=["json"],
            key="import_data_uploader",
            help="Import a previously exported HealthAI backup file"
        )

        if import_file is not None:
            try:
                import_data = json.load(import_file)
                if storage.import_data(json.dumps(import_data)):
                    st.success("✅ Data imported successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to import data")
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")

        st.markdown("---")

        # Export data section
        if storage.check_storage_exists():
            storage_info = storage.get_storage_info()
            st.markdown("#### 📤 Export Data")
            st.info(f"📊 {storage_info['total_analyses']} stored analyses")

            export_json = storage.export_all_data()
            st.download_button(
                label="⬇️ Download Backup",
                data=export_json,
                file_name=f"healthai_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                help="Download all your data as a JSON file"
            )

            st.markdown("---")

            # Clear data with confirmation
            if 'confirm_clear' not in st.session_state:
                st.session_state.confirm_clear = False

            if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary", key="clear_all_btn"):
                st.session_state.confirm_clear = True

            if st.session_state.confirm_clear:
                st.warning("⚠️ This will delete all stored analyses!")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Yes, Delete", use_container_width=True, type="primary", key="confirm_yes"):
                        storage.clear_storage()
                        st.session_state.confirm_clear = False
                        st.success("✅ All data cleared!")
                        st.rerun()
                with col_b:
                    if st.button("❌ Cancel", use_container_width=True, key="confirm_no"):
                        st.session_state.confirm_clear = False
                        st.rerun()
        else:
            st.info("💡 No stored data yet.\n\nComplete an analysis to save data automatically.")

        st.markdown("---")
        st.caption("💾 Data is stored in your browser\n🔄 Export to save permanently")

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

    # Render chat interface (always visible)
    render_chat_interface()

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
            status_message_box.write("⚙️ Preparing your data...")

            # ====================
            # Part 1: Biomarkers
            # ====================
            status_message_box.write("🔬 Analyzing your biomarkers...")
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
            status_message_box.write("💪 Analyzing your Four Pillars (Eat, Sleep, Move, Recover)...")
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
            status_message_box.write("💊 Creating your supplement recommendations...")
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

                # Save to localStorage
                status_message_box.write("💾 Saving analysis...")
                save_success = storage.save_analysis_result(
                    input_data={
                        "lab_reports": combined_lab_report_text,
                        "health_assessment": raw_health_assessment_input
                    },
                    output_data=final_combined_output,
                    analysis_type="standard"
                )

                if save_success:
                    st.success("✅ Analysis saved! Your data persists in this browser session.", icon="💾")
            else:
                status_message_box.error("❌ No analysis data could be generated. Please check the inputs and ensure HealthAI is correctly configured.")

        # Display results outside status block to avoid nesting expanders
        if final_combined_output:
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


if __name__ == "__main__":
    main()
