"""
HealthAI Chat Agent

Context-aware health chat using user's stored data and analysis results.
Specialized for health and medical questions only.

Version: 2.0.0
Author: Ganesh Shinde
"""

import streamlit as st
from typing import List, Dict, Optional
import json
from .ai_client import HealthAIClient
from .storage import HealthAIStorage


class HealthChatAgent:
    """AI chat agent specialized for health-related queries."""

    def __init__(self):
        """Initialize the chat agent."""
        self.ai_client = HealthAIClient()
        self.storage = HealthAIStorage()

        # Initialize conversation history in session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        if 'user_context' not in st.session_state:
            st.session_state.user_context = None

    def initialize_context(self):
        """Load user's health data and analyses for context."""
        latest_analysis = self.storage.get_latest_analysis()

        if latest_analysis:
            st.session_state.user_context = {
                "has_data": True,
                "analysis_date": latest_analysis.get('timestamp', 'Unknown'),
                "analysis_type": latest_analysis.get('type', 'Unknown'),
                "biomarkers": latest_analysis.get('output_data', {}).get('lab_analysis', {}),
                "four_pillars": latest_analysis.get('output_data', {}).get('four_pillars', {}),
                "supplements": latest_analysis.get('output_data', {}).get('supplements', {}),
            }
        else:
            st.session_state.user_context = {"has_data": False}

    def build_system_prompt(self) -> str:
        """Build system prompt with user context and guidelines."""
        base_prompt = """You are HealthAI Chat, a specialized AI health assistant.

**Your Role:**
- Answer ONLY health and medical-related questions
- Use the user's stored health data and analysis results for personalized responses
- Provide evidence-based, actionable guidance
- Be conversational, friendly, and supportive
- Always include appropriate medical disclaimers when giving advice

**Constraints:**
- REFUSE to answer non-health/non-medical questions politely
- DO NOT diagnose or prescribe medications (suggest consulting healthcare providers)
- DO NOT make up information about the user's data
- ALWAYS reference specific biomarkers/data from their analysis when available
- Keep responses concise and easy to understand (2-4 paragraphs max)

**Medical Disclaimer (include when giving health advice):**
"This is AI-generated guidance for informational purposes only. Always consult with a qualified healthcare provider for medical decisions."
"""

        if st.session_state.user_context and st.session_state.user_context.get('has_data'):
            ctx = st.session_state.user_context

            # Build a summary of user's key health data
            context_summary = f"""

**User's Health Context:**

Analysis Date: {ctx.get('analysis_date', 'Unknown')}
Analysis Type: {ctx.get('analysis_type', 'Unknown')}

"""
            # Add biomarker summary if available
            biomarkers = ctx.get('biomarkers', {})
            if biomarkers:
                context_summary += "\nKey Biomarkers:\n"
                detailed_biomarkers = biomarkers.get('detailed_biomarkers', [])
                for marker in detailed_biomarkers[:5]:  # Show top 5
                    name = marker.get('name', 'Unknown')
                    result = marker.get('result', 'N/A')
                    status = marker.get('status', 'unknown')
                    context_summary += f"- {name}: {result} ({status})\n"

            # Add four pillars scores if available
            pillars = ctx.get('four_pillars', {})
            if pillars and pillars.get('pillars'):
                context_summary += "\nFour Pillars Scores:\n"
                for pillar in pillars['pillars']:
                    name = pillar.get('name', 'Unknown')
                    score = pillar.get('score', 'N/A')
                    context_summary += f"- {name}: {score}/10\n"

            context_summary += "\nUse this context to provide personalized, data-driven responses.\n"
            context_summary += "Reference specific biomarkers and scores when answering questions.\n"

            return base_prompt + context_summary
        else:
            no_data_prompt = """

**Note:** User has not uploaded any health data yet. Provide general health guidance only.
Suggest they upload their lab reports or health data to get personalized insights.
"""
            return base_prompt + no_data_prompt

    def is_health_related(self, message: str) -> bool:
        """
        Check if the message is health/medical-related.

        Args:
            message: User's message

        Returns:
            bool: True if health-related
        """
        health_keywords = [
            'health', 'medical', 'symptom', 'biomarker', 'lab', 'test',
            'vitamin', 'supplement', 'hormone', 'thyroid', 'blood', 'doctor',
            'diagnosis', 'treatment', 'medication', 'exercise', 'diet', 'sleep',
            'stress', 'wellness', 'nutrition', 'fitness', 'pain', 'fatigue',
            'energy', 'mood', 'cycle', 'period', 'glucose', 'cholesterol',
            'inflammation', 'gut', 'digestion', 'immunity', 'recovery',
            'cortisol', 'estrogen', 'testosterone', 'progesterone', 'tsh',
            'analysis', 'report', 'result', 'score', 'recommendation',
            'sick', 'ill', 'disease', 'condition', 'chronic', 'acute',
            'food', 'meal', 'eat', 'hungry', 'weight', 'body', 'mental',
            'anxiety', 'depression', 'headache', 'muscle', 'joint', 'bone',
            'hello', 'hi', 'hey', 'thanks', 'help', 'how', 'what', 'can', 'do', 'tell'
        ]

        message_lower = message.lower()
        return any(keyword in message_lower for keyword in health_keywords)

    def chat(self, user_message: str) -> str:
        """
        Process user message and return AI response.

        Args:
            user_message: User's input message

        Returns:
            str: AI's response
        """
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Build system prompt with context
            system_prompt = self.build_system_prompt()

            # Prepare conversation for AI
            # Include last 5 messages for context (to avoid token limits)
            recent_history = st.session_state.chat_history[-5:]

            conversation = [
                {"role": "system", "content": system_prompt}
            ] + recent_history

            # Format for AI client
            prompt = self._format_conversation_for_ai(conversation)

            # Get AI response
            response_data, _ = self.ai_client.generate_content(prompt)

            # Extract response text from the data
            if isinstance(response_data, dict):
                # Try to extract the actual text from common response formats
                response = (
                    response_data.get('response') or
                    response_data.get('text') or
                    response_data.get('content') or
                    response_data.get('message') or
                    str(response_data)
                )
            elif isinstance(response_data, str):
                response = response_data
            else:
                response = str(response_data)

            # Add assistant response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })

            return response

        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}. Please try again or rephrase your question."
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            return error_msg

    def _format_conversation_for_ai(self, conversation: List[Dict]) -> str:
        """
        Format conversation history into a prompt string.

        Args:
            conversation: List of message dictionaries

        Returns:
            str: Formatted prompt
        """
        formatted = ""
        for msg in conversation:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                formatted += f"{content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"

        formatted += "Assistant: "
        return formatted

    def reset_conversation(self):
        """Clear conversation history."""
        st.session_state.chat_history = []

    def get_conversation_history(self) -> List[Dict]:
        """
        Get current conversation history.

        Returns:
            List of message dictionaries
        """
        return st.session_state.chat_history

    def export_chat_history(self) -> str:
        """
        Export chat history as JSON string.

        Returns:
            str: JSON string of chat history
        """
        try:
            from datetime import datetime
            export_data = {
                "export_date": datetime.now().isoformat(),
                "messages": st.session_state.chat_history
            }
            return json.dumps(export_data, indent=2)
        except Exception as e:
            return f'{{"error": "{str(e)}"}}'
