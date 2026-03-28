"""
HealthAI - Display Utilities (Streamlit-Native Version)

Beautiful visual rendering of health analysis results.
Uses Streamlit native components for better compatibility.

Version: 2.1.0
Author: Ganesh Shinde
"""

import streamlit as st
import re
from typing import Dict, Any, List


# ==========================================
# Text Highlighting Helpers
# ==========================================

def parse_highlights(text: str) -> str:
    """
    Parse C1[text]C1 and C2[text]C2 markers into simple colored text.
    Uses minimal HTML for better Streamlit compatibility.
    """
    if not text:
        return ""

    # Convert C1 markers (primary highlights)
    text = re.sub(
        r'\*\*C1\[(.*?)\]C1\*\*',
        r'**:red[\1]**',
        text
    )

    # Convert C2 markers (secondary highlights)
    text = re.sub(
        r'\*\*C2\[(.*?)\]C2\*\*',
        r'**:blue[\1]**',
        text
    )

    return text


# ==========================================
# Biomarker Display Components
# ==========================================

def display_biomarker_card(biomarker: Dict[str, Any]):
    """Display a single biomarker using Streamlit native components."""

    status = biomarker.get("status", "optimal")
    name = biomarker.get("name", "Unknown")
    status_label = biomarker.get("status_label", status.title())
    result = biomarker.get("result", "N/A")
    range_val = biomarker.get("range", "N/A")
    why_matters = biomarker.get("why_it_matters", "")
    cycle_impact = biomarker.get("cycle_impact", "")

    # Status emoji and color
    if status == "optimal":
        emoji = "✅"
        container_type = "success"
    elif status == "keep_in_mind":
        emoji = "⚠️"
        container_type = "warning"
    else:  # attention_needed
        emoji = "🔴"
        container_type = "error"

    # Use Streamlit containers
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {emoji} {name}")
        with col2:
            if status == "optimal":
                st.success(status_label, icon="✅")
            elif status == "keep_in_mind":
                st.warning(status_label, icon="⚠️")
            else:
                st.error(status_label, icon="🔴")

        col_result, col_range = st.columns(2)
        with col_result:
            st.metric(label="Your Result", value=result)
        with col_range:
            st.metric(label="Reference Range", value=range_val)

        if why_matters:
            st.markdown(parse_highlights(why_matters))

        if cycle_impact:
            st.info(f"🔄 **Cycle Impact:** {parse_highlights(cycle_impact)}", icon="🔄")

        st.markdown("---")


def display_lab_analysis(lab_data: Dict[str, Any]):
    """Display complete lab analysis section."""

    if not lab_data:
        st.info("No lab analysis data available.")
        return

    st.header("🔬 Lab Analysis Results")

    # Overall Summary
    if lab_data.get("overall_summary"):
        st.markdown("### 📋 Overall Summary")
        st.info(parse_highlights(lab_data['overall_summary']), icon="📋")

    # Biomarker Summary Metrics
    if lab_data.get("biomarker_categories_summary"):
        summary = lab_data["biomarker_categories_summary"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="📊 Total Tested",
                value=lab_data.get("biomarkers_tested_count", 0)
            )

        with col2:
            st.metric(
                label="✅ Optimal",
                value=summary.get("optimal_count", 0)
            )

        with col3:
            st.metric(
                label="⚠️ Keep in Mind",
                value=summary.get("keep_in_mind_count", 0)
            )

        with col4:
            st.metric(
                label="🔴 Attention Needed",
                value=summary.get("attention_needed_count", 0)
            )

        st.markdown("---")

    # Detailed Biomarkers
    if lab_data.get("detailed_biomarkers"):
        st.markdown("### 🧪 Detailed Biomarker Analysis")

        # Organize by status
        optimal = [b for b in lab_data["detailed_biomarkers"] if b.get("status") == "optimal"]
        keep_in_mind = [b for b in lab_data["detailed_biomarkers"] if b.get("status") == "keep_in_mind"]
        attention_needed = [b for b in lab_data["detailed_biomarkers"] if b.get("status") == "attention_needed"]

        # Display attention needed first
        if attention_needed:
            st.markdown("#### 🔴 Needs Attention")
            for biomarker in attention_needed:
                display_biomarker_card(biomarker)

        # Then keep in mind
        if keep_in_mind:
            st.markdown("#### ⚠️ Keep in Mind")
            for biomarker in keep_in_mind:
                display_biomarker_card(biomarker)

        # Finally optimal (in expander to save space)
        if optimal:
            with st.expander(f"✅ Optimal Results ({len(optimal)} biomarkers)", expanded=False):
                for biomarker in optimal:
                    display_biomarker_card(biomarker)

    # Crucial biomarkers to measure
    if lab_data.get("crucial_biomarkers_to_measure"):
        st.markdown("### 🎯 Recommended Additional Tests")
        for item in lab_data["crucial_biomarkers_to_measure"]:
            st.info(f"**{item.get('name')}**: {parse_highlights(item.get('importance', ''))}", icon="🔍")

    # Health recommendations
    if lab_data.get("health_recommendation_summary"):
        st.markdown("### 💡 Key Recommendations")
        for rec in lab_data["health_recommendation_summary"]:
            st.success(parse_highlights(rec), icon="✨")


# ==========================================
# Four Pillars Display Components
# ==========================================

def display_pillar_score(pillar: Dict[str, Any]):
    """Display a single pillar with score visualization."""

    name = pillar.get("name", "Unknown Pillar")
    score = pillar.get("score", 0)

    # Emoji mapping
    emoji_map = {
        "Eat Well": "🥗",
        "Sleep Well": "😴",
        "Move Well": "🏃",
        "Recover Well": "🧘"
    }

    emoji = emoji_map.get(name, "💪")

    with st.container():
        # Header with score
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {emoji} {name}")
        with col2:
            if score >= 8:
                st.success(f"{score}/10", icon="🌟")
            elif score >= 5:
                st.warning(f"{score}/10", icon="⚡")
            else:
                st.error(f"{score}/10", icon="⚠️")

        # Progress bar
        st.progress(score / 10)

        # Score rationale
        if pillar.get("score_rationale"):
            st.markdown("**Why this score:**")
            for rationale in pillar["score_rationale"]:
                st.markdown(f"- {parse_highlights(rationale)}")

        # Why it matters
        if pillar.get("why_it_matters"):
            st.info(f"**Why it matters:** {parse_highlights(pillar['why_it_matters'])}", icon="💡")

        # Science explanation
        if pillar.get("science_based_explanation"):
            st.markdown(f"**🔬 Science:** {parse_highlights(pillar['science_based_explanation'])}")

        # Root cause correlation
        if pillar.get("root_cause_correlation"):
            st.markdown(f"**🎯 Root Cause Connection:** {parse_highlights(pillar['root_cause_correlation'])}")

        # Additional guidance (expandable)
        if pillar.get("additional_guidance"):
            guidance = pillar["additional_guidance"]

            with st.expander(f"📚 Detailed Guidance for {name}", expanded=False):
                if guidance.get("description"):
                    st.info(parse_highlights(guidance["description"]), icon="ℹ️")

                # Display structure (varies by pillar)
                if guidance.get("structure"):
                    structure = guidance["structure"]

                    for key, items in structure.items():
                        # Format the key nicely
                        display_key = key.replace("_", " ").title()
                        st.markdown(f"**{display_key}:**")

                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict):
                                    name_val = item.get("name", "")
                                    desc = item.get("description", "")
                                    if name_val and desc:
                                        st.markdown(f"- **{name_val}**: {parse_highlights(desc)}")
                                    elif name_val:
                                        st.markdown(f"- {parse_highlights(name_val)}")
                                else:
                                    st.markdown(f"- {parse_highlights(str(item))}")

        st.markdown("---")


def display_four_pillars(pillars_data: Dict[str, Any]):
    """Display complete Four Pillars section."""

    if not pillars_data:
        st.info("No Four Pillars data available.")
        return

    st.header("💪 Four Pillars of Health")

    # Introduction
    if pillars_data.get("introduction"):
        st.info(parse_highlights(pillars_data['introduction']), icon="💪")

    # Display each pillar
    if pillars_data.get("pillars"):
        for pillar in pillars_data["pillars"]:
            display_pillar_score(pillar)


# ==========================================
# Supplements Display Components
# ==========================================

def display_supplement_card(supplement: Dict[str, Any]):
    """Display a single supplement recommendation."""

    name = supplement.get('name', 'Unknown Supplement')
    rationale = supplement.get('rationale', '')
    expected_outcomes = supplement.get('expected_outcomes', '')
    dosage_timing = supplement.get('dosage_and_timing', '')
    cyclical = supplement.get('situational_cyclical_considerations', '')

    with st.container():
        st.markdown(f"### 💊 {name}")

        if rationale:
            st.markdown(f"**Why:** {parse_highlights(rationale)}")

        if expected_outcomes:
            st.success(f"**Expected Benefits:** {parse_highlights(expected_outcomes)}", icon="✨")

        if dosage_timing:
            st.info(f"**📋 Dosage & Timing:** {parse_highlights(dosage_timing)}", icon="📋")

        if cyclical:
            st.warning(f"**🔄 Cyclical Considerations:** {parse_highlights(cyclical)}", icon="🔄")

        st.markdown("---")


def display_supplements(supplements_data: Dict[str, Any]):
    """Display complete supplements section."""

    if not supplements_data:
        st.info("No supplement recommendations available.")
        return

    st.header("💊 Supplement Recommendations")

    # Description
    if supplements_data.get("description"):
        st.info(parse_highlights(supplements_data['description']), icon="💊")

    # Recommendations
    if supplements_data.get("structure", {}).get("recommendations"):
        for supplement in supplements_data["structure"]["recommendations"]:
            display_supplement_card(supplement)

    # Conclusion
    if supplements_data.get("structure", {}).get("conclusion"):
        st.success(parse_highlights(supplements_data["structure"]["conclusion"]), icon="✅")


# ==========================================
# Complete Analysis Display
# ==========================================

def display_analysis_results(analysis_data: Dict[str, Any]):
    """
    Main function to display all analysis results beautifully.

    Parameters:
        analysis_data: Complete JSON response from AI
    """

    if not analysis_data:
        st.warning("No analysis data to display.")
        return

    # Success message
    st.success("✨ Your personalized health analysis is ready!", icon="🎉")

    st.markdown("---")

    # Lab Analysis Section
    if analysis_data.get("lab_analysis"):
        display_lab_analysis(analysis_data["lab_analysis"])
        st.markdown("---")

    # Four Pillars Section
    if analysis_data.get("four_pillars"):
        display_four_pillars(analysis_data["four_pillars"])
        st.markdown("---")

    # Supplements Section
    if analysis_data.get("supplements"):
        display_supplements(analysis_data["supplements"])


# ==========================================
# Monthly Report Display Components
# ==========================================

def display_monthly_overview(overview_data: Dict[str, Any]):
    """Display monthly overview summary section."""

    if not overview_data:
        return

    st.header("📊 Monthly Health Overview")

    # Main summary
    if overview_data.get("summary"):
        st.info(parse_highlights(overview_data["summary"]), icon="📋")

    # Top symptoms
    if overview_data.get("top_symptoms"):
        st.markdown("### 🔍 Top Symptoms This Month")
        cols = st.columns(min(len(overview_data["top_symptoms"]), 3))
        for idx, symptom in enumerate(overview_data["top_symptoms"]):
            with cols[idx % 3]:
                st.warning(symptom, icon="⚠️")

    # Health reflection
    if overview_data.get("health_reflection"):
        st.markdown("### 💭 Health Reflection")
        st.success(parse_highlights(overview_data["health_reflection"]), icon="💡")


def display_hormonal_balance(balance_data: Dict[str, Any]):
    """Display hormonal balance insight section."""

    if not balance_data:
        return

    st.header("⚖️ Hormonal Balance Insight")

    # Score or message
    if balance_data.get("score_or_message"):
        st.info(parse_highlights(balance_data["score_or_message"]), icon="⚖️")

    col1, col2 = st.columns(2)

    # Tied to logs
    with col1:
        if balance_data.get("tied_to_logs"):
            st.markdown("**📝 Related to Your Logs:**")
            for log in balance_data["tied_to_logs"]:
                st.markdown(f"- {parse_highlights(log)}")

    # Likely root causes
    with col2:
        if balance_data.get("likely_root_causes"):
            st.markdown("**🎯 Likely Root Causes:**")
            for cause in balance_data["likely_root_causes"]:
                st.markdown(f"- {parse_highlights(cause)}")


def display_logged_pattern(pillar_name: str, pattern_data: Dict[str, Any], emoji: str):
    """Display a single logged pattern for a pillar."""

    with st.container():
        st.markdown(f"### {emoji} {pillar_name}")

        # Metrics
        if pattern_data.get("metrics"):
            metrics = pattern_data["metrics"]

            # Create columns based on available metrics
            metric_cols = st.columns(len(metrics))
            for idx, (key, value) in enumerate(metrics.items()):
                with metric_cols[idx]:
                    # Format the metric name nicely
                    metric_name = key.replace("_", " ").title()
                    # Round if it's a float
                    if isinstance(value, float):
                        value = round(value, 1)
                    st.metric(label=metric_name, value=value)

        # Create tabs for different sections
        tabs = []
        tab_names = []

        if pattern_data.get("did_well"):
            tab_names.append("✅ Did Well")
        if pattern_data.get("areas_to_improve"):
            tab_names.append("📈 Improve")
        if pattern_data.get("recommendations"):
            tab_names.append("💡 Tips")
        if pattern_data.get("Guidance"):
            tab_names.append("📚 Guidance")

        if tab_names:
            tabs = st.tabs(tab_names)
            tab_idx = 0

            # Did well
            if pattern_data.get("did_well"):
                with tabs[tab_idx]:
                    for item in pattern_data["did_well"]:
                        st.success(f"✓ {item}", icon="✅")
                tab_idx += 1

            # Areas to improve
            if pattern_data.get("areas_to_improve"):
                with tabs[tab_idx]:
                    for item in pattern_data["areas_to_improve"]:
                        st.warning(f"→ {item}", icon="📈")
                tab_idx += 1

            # Recommendations
            if pattern_data.get("recommendations"):
                with tabs[tab_idx]:
                    for item in pattern_data["recommendations"]:
                        st.info(parse_highlights(item), icon="💡")
                tab_idx += 1

            # Guidance
            if pattern_data.get("Guidance"):
                with tabs[tab_idx]:
                    for item in pattern_data["Guidance"]:
                        st.markdown(f"- {parse_highlights(item)}")

        st.markdown("---")


def display_logged_patterns(patterns_data: Dict[str, Any]):
    """Display all four pillars logged patterns."""

    if not patterns_data:
        return

    st.header("📈 Monthly Pattern Analysis")

    # Emoji mapping
    emoji_map = {
        "eat_well": "🥗",
        "sleep_well": "😴",
        "move_well": "🏃",
        "recover_well": "🧘"
    }

    # Display each pillar
    for pillar_key, emoji in emoji_map.items():
        if patterns_data.get(pillar_key):
            pillar_name = pillar_key.replace("_", " ").title()
            display_logged_pattern(pillar_name, patterns_data[pillar_key], emoji)


def display_root_cause_tags(tags_data: List[Dict[str, Any]]):
    """Display root cause tags."""

    if not tags_data:
        return

    st.header("🎯 Root Cause Analysis")

    for tag_item in tags_data:
        tag = tag_item.get("tag", "")
        explanation = tag_item.get("explanation", "")

        if tag and explanation:
            with st.expander(f"🏷️ {tag}", expanded=False):
                st.markdown(parse_highlights(explanation))


def display_actionable_next_steps(steps_data: Dict[str, Any]):
    """Display actionable next steps section."""

    if not steps_data:
        return

    st.header("🎯 Your Action Plan")

    # Create tabs for different categories
    tab_names = []
    if steps_data.get("food_to_enjoy") or steps_data.get("food_to_limit"):
        tab_names.append("🥗 Nutrition")
    if steps_data.get("movements"):
        tab_names.append("🏃 Movement")
    if steps_data.get("rest_and_recovery"):
        tab_names.append("🧘 Recovery")
    if steps_data.get("daily_habits"):
        tab_names.append("📅 Habits")
    if steps_data.get("behavior_goals"):
        tab_names.append("🎯 Goals")

    if tab_names:
        tabs = st.tabs(tab_names)
        tab_idx = 0

        # Nutrition tab
        if steps_data.get("food_to_enjoy") or steps_data.get("food_to_limit"):
            with tabs[tab_idx]:
                col1, col2 = st.columns(2)

                with col1:
                    if steps_data.get("food_to_enjoy"):
                        st.markdown("**✅ Foods to Enjoy:**")
                        for food in steps_data["food_to_enjoy"]:
                            st.success(parse_highlights(food), icon="✅")

                with col2:
                    if steps_data.get("food_to_limit"):
                        st.markdown("**⚠️ Foods to Limit:**")
                        for food in steps_data["food_to_limit"]:
                            st.warning(parse_highlights(food), icon="⚠️")
            tab_idx += 1

        # Movement tab
        if steps_data.get("movements"):
            with tabs[tab_idx]:
                for movement in steps_data["movements"]:
                    st.info(parse_highlights(movement), icon="🏃")
            tab_idx += 1

        # Recovery tab
        if steps_data.get("rest_and_recovery"):
            with tabs[tab_idx]:
                for recovery in steps_data["rest_and_recovery"]:
                    st.info(parse_highlights(recovery), icon="🧘")
            tab_idx += 1

        # Habits tab
        if steps_data.get("daily_habits"):
            with tabs[tab_idx]:
                for habit in steps_data["daily_habits"]:
                    st.info(parse_highlights(habit), icon="📅")
            tab_idx += 1

        # Goals tab
        if steps_data.get("behavior_goals"):
            with tabs[tab_idx]:
                for goal in steps_data["behavior_goals"]:
                    st.success(parse_highlights(goal), icon="🎯")

    # Encouragement message
    if steps_data.get("encouragement_message"):
        st.success(parse_highlights(steps_data["encouragement_message"]), icon="🌟")


def display_radar_chart(radar_data: Dict[str, Any]):
    """Display radar chart data and key behaviors."""

    if not radar_data:
        return

    st.header("📊 Your Health Radar")

    # Label and caption
    if radar_data.get("label"):
        st.subheader(radar_data["label"])

    if radar_data.get("caption"):
        st.info(parse_highlights(radar_data["caption"]), icon="📊")

    # Scores
    if radar_data.get("scores"):
        scores = radar_data["scores"]

        st.markdown("### 📈 Your Scores")

        emoji_map = {
            "eat_well": "🥗",
            "sleep_well": "😴",
            "move_well": "🏃",
            "recover_well": "🧘"
        }

        cols = st.columns(4)
        for idx, (pillar, score) in enumerate(scores.items()):
            pillar_name = pillar.replace("_", " ").title()
            emoji = emoji_map.get(pillar, "💪")

            with cols[idx]:
                st.metric(
                    label=f"{emoji} {pillar_name}",
                    value=f"{score}/10"
                )
                # Progress bar
                st.progress(score / 10)

    # Key behaviors
    if radar_data.get("key_behaviors"):
        st.markdown("### 🔑 Key Behaviors")

        behaviors = radar_data["key_behaviors"]
        emoji_map = {
            "eat_well": "🥗",
            "sleep_well": "😴",
            "move_well": "🏃",
            "recover_well": "🧘"
        }

        for pillar, behavior_list in behaviors.items():
            if behavior_list:
                pillar_name = pillar.replace("_", " ").title()
                emoji = emoji_map.get(pillar, "💪")

                with st.expander(f"{emoji} {pillar_name} Behaviors", expanded=False):
                    for behavior in behavior_list:
                        st.markdown(f"- {parse_highlights(behavior)}")


def display_monthly_report(report_data: Dict[str, Any]):
    """
    Main function to display monthly health report beautifully.

    Parameters:
        report_data: Complete JSON response from AI for monthly report
    """

    if not report_data:
        st.warning("No monthly report data to display.")
        return

    # Success message
    st.success("✨ Your monthly health report is ready!", icon="🎉")

    st.markdown("---")

    # Monthly Overview
    if report_data.get("monthly_overview_summary"):
        display_monthly_overview(report_data["monthly_overview_summary"])
        st.markdown("---")

    # Hormonal Balance
    if report_data.get("hormonal_balance_insight"):
        display_hormonal_balance(report_data["hormonal_balance_insight"])
        st.markdown("---")

    # Radar Chart
    if report_data.get("radar_chart_data"):
        display_radar_chart(report_data["radar_chart_data"])
        st.markdown("---")

    # Logged Patterns
    if report_data.get("logged_patterns"):
        display_logged_patterns(report_data["logged_patterns"])
        st.markdown("---")

    # Root Cause Tags
    if report_data.get("root_cause_tags"):
        display_root_cause_tags(report_data["root_cause_tags"])
        st.markdown("---")

    # Actionable Next Steps
    if report_data.get("actionable_next_steps"):
        display_actionable_next_steps(report_data["actionable_next_steps"])
