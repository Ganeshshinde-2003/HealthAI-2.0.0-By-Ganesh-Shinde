"""
HealthAI - Monthly Health Reporter

Generates comprehensive monthly health trend reports with radar chart visualization.
Analyzes daily logs, weekly assessments, and lab reports for longitudinal insights.

Version: 2.0.0 (Refactored)
Author: Ganesh Shinde
"""

import streamlit as st
import json

# Import configuration
from config import UIConfig, AIConfig

# Import utilities
from utils import (
    extract_text_from_file,
    HealthAIClient,
    build_monthly_report_prompt,
    display_monthly_report
)


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title=UIConfig.PAGE_TITLE_MONTHLY,
    page_icon=UIConfig.PAGE_ICON_MONTHLY,
    layout=UIConfig.LAYOUT
)


# ==========================================
# Initialize AI Client
# ==========================================

try:
    # Use smaller token limit for monthly reports
    ai_client = HealthAIClient(max_output_tokens=AIConfig.MAX_OUTPUT_TOKENS_MONTHLY)
except Exception as e:
    st.error(f"Failed to initialize AI client: {e}")
    st.stop()


# ==========================================
# Main Application
# ==========================================

def main():
    """Main application function."""

    st.title(UIConfig.HEADER_MAIN_MONTHLY)
    st.write("Upload your monthly health tracking data for comprehensive trend analysis and personalized insights.")

    # ====================
    # Monthly Tracking Guide (Expandable)
    # ====================
    with st.expander("📚 **Monthly Tracking Guide & Examples** - Click here to see what to upload!", expanded=False):
        st.markdown("""
        ### 📊 Daily Health Logs (Required)

        Track these daily for best monthly insights:

        **Essential Daily Metrics:**
        - 😴 **Sleep:** Hours, quality (1-5), bedtime/wake time
        - 🍽️ **Meals:** What you ate, timing, how you felt
        - 🏃 **Movement:** Exercise type, duration, intensity
        - 🧘 **Recovery:** Stress level, meditation, relaxation
        - 💭 **Symptoms:** Mood, energy (1-5), any symptoms
        - ⚖️ **Balance:** What helped your health, what hurt it
        - 📅 **Optional:** Cycle tracking (if applicable)

        **Example Daily Log Format (Excel/CSV):**
        ```
        Date     | Category   | Details        | Feeling   | Earning Balance    | Losing Balance
        3/15/26  | Sleep      | 7.5h soundly   | Refreshed | Consistent bedtime | -
        3/15/26  | Eat Well   | Oatmeal 8am    | Good      | Whole foods        | -
        3/15/26  | Move Well  | 30min yoga     | Energized | Movement           | -
        3/16/26  | Sleep      | 5.5h restless  | Tired     | -                  | Late screen time
        ```

        ---

        ### 📝 Weekly Self-Assessments (Optional)

        Weekly check-ins help identify patterns:

        **What to Track:**
        - Overall stress level (1-10)
        - Energy trends
        - Sleep quality average
        - Main symptoms
        - Wins & challenges

        **Example Weekly Check-in:**
        ```
        Week of March 15-21, 2026
        Stress: 7/10 (work deadline)
        Energy: Improved mid-week
        Wins: Exercised 4 days, meal prepped
        Challenges: Stress eating Thursday
        ```

        ---

        ### 📋 Previous Lab Report (Optional)

        Upload your most recent lab results to see how biomarkers relate to your daily patterns.

        ---

        **💡 Tips for Success:**
        - Track for 21+ days for best trends
        - Be honest about "bad" days too
        - Note cycle phase if applicable
        - Include context (why you felt that way)
        - Track consistently for patterns
        """)

    st.markdown("---")

    # ====================
    # File Upload Section
    # ====================
    previous_lab_report = st.file_uploader(
        "📋 Previous Lab Report (optional)",
        type=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"],
        help="Upload your most recent lab report to provide context for your monthly health trends. This helps us understand how your biomarkers relate to your daily symptoms and lifestyle patterns."
    )
    daily_logs = st.file_uploader(
        "📊 Daily Health Logs (required)",
        type=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"],
        help="Upload your daily tracking data including: symptoms (mood, energy, pain), food intake (meals, timing), sleep (hours, quality), exercise (type, duration), and recovery activities (meditation, stress levels). Can be an Excel spreadsheet, CSV file, or document with your daily notes."
    )
    weekly_assessments = st.file_uploader(
        "📝 Weekly Self-Assessments (optional)",
        type=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"],
        help="Upload your weekly check-ins or reflections on: overall stress levels, symptom patterns, effort put into health goals, challenges faced, or wins achieved. This can be journal entries, questionnaire responses, or any weekly notes."
    )

    # ====================
    # Process Files
    # ====================
    raw_lab_report_text = extract_text_from_file(previous_lab_report) if previous_lab_report else ""
    raw_daily_logs_text = extract_text_from_file(daily_logs)
    raw_weekly_assessments_text = extract_text_from_file(weekly_assessments) if weekly_assessments else ""

    # ====================
    # Validation
    # ====================
    if not daily_logs:
        st.info("📊 Please upload your Daily Health Logs to generate your monthly report. This helps us track your health trends over time.")
        st.stop()

    # ====================
    # Error Handling
    # ====================
    if raw_daily_logs_text.startswith("[Error"):
        st.error(f"Error processing Daily Logs: {raw_daily_logs_text}")
        st.stop()

    if raw_lab_report_text.startswith("[Error"):
        st.warning(f"Warning: Problem with Previous Lab Report: {raw_lab_report_text}")
        st.write("Continuing analysis without previous lab report data.")
        raw_lab_report_text = ""

    if raw_weekly_assessments_text.startswith("[Error"):
        st.warning(f"Warning: Problem with Weekly Self-Assessments: {raw_weekly_assessments_text}")
        st.write("Continuing analysis without weekly self-assessment data.")
        raw_weekly_assessments_text = ""

    # ====================
    # Analysis Button
    # ====================
    if st.button(UIConfig.BUTTON_MONTHLY, type="primary"):
        with st.status(UIConfig.MONTHLY_INITIATING, expanded=True) as status_message_box:
            status_message_box.write("⚙️ Preparing data for AI analysis...")

            try:
                # Prepare data sections for the prompt
                previous_lab_report_section = (
                    f"The user's initial health analysis from a prior lab report:\n{raw_lab_report_text}\n"
                    if raw_lab_report_text
                    else "No prior lab report data provided.\n"
                )
                daily_logs_section = f"The user's daily logs on symptoms and lifestyle (eat/sleep/move/recover):\n{raw_daily_logs_text}\n"
                weekly_assessments_section = (
                    f"Weekly self-assessments (e.g., stress, symptoms, effort):\n{raw_weekly_assessments_text}\n"
                    if raw_weekly_assessments_text
                    else "No weekly self-assessment data provided.\n"
                )

                # Build prompt using utility function
                prompt = build_monthly_report_prompt(
                    previous_lab_report_section,
                    daily_logs_section,
                    weekly_assessments_section
                )

                status_message_box.write("🧠 Sending data to HealthAI AI...")

                # Generate analysis
                analysis_data, _ = ai_client.generate_content(prompt)

                # ====================
                # Display Results
                # ====================
                if analysis_data:
                    status_message_box.update(label=UIConfig.MONTHLY_COMPLETE, state="complete")

                    # Beautiful visual display
                    display_monthly_report(analysis_data)

                    st.markdown("---")

                    # Download buttons
                    st.subheader("📥 Download Your Report")
                    col1, col2 = st.columns(2)

                    with col1:
                        # JSON Download
                        plain_json_string = json.dumps(analysis_data, indent=2)
                        st.download_button(
                            label="📄 Download JSON",
                            data=plain_json_string,
                            file_name="healthai_monthly_report.json",
                            mime="application/json",
                            help="Download your monthly report as a JSON file for your records."
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
                        st.json(analysis_data, expanded=True)
                        st.markdown("**Copy JSON Text:**")
                        st.text_area(
                            "Select and copy:",
                            plain_json_string,
                            height=300,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                else:
                    status_message_box.error("❌ No analysis data could be generated.")

            except Exception as e:
                status_message_box.error(f"❌ An error occurred during report generation: {e}")
                st.error("Please check your input files and ensure HealthAI is correctly configured.")


if __name__ == "__main__":
    main()
